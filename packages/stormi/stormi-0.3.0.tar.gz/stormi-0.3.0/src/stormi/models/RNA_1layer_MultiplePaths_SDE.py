from __future__ import annotations

from collections import OrderedDict
from functools import partial
from typing import Any, Callable, Dict, List, Optional

import jax
import jax.numpy as jnp
import numpy as np
import numpyro
import numpyro.distributions as dist
import pandas as pd
from anndata import AnnData
from beartype import beartype
from jax import lax
from numpyro.handlers import scale

from .RNA_utils import sample_prior
from .utils import solve_DE, sort_times_over_all_cells


@beartype
def prepare_model_input(
    adata_rna: AnnData,
    tf_list: List[str],
    n_cells_col: str = "n_cells",
    prior_time_col: Optional[str] = None,
    batch_annotation: Optional[str] = None,
    prior_path_col: Optional[str] = None,
    prior_timespan: Optional[float] = 40,
) -> Dict[str, Any]:
    """
    Prepare RNA input data for the model by extracting spliced and unspliced counts,
    computing transcription factor indices, and extracting cell metadata including batch
    information from adata_rna.obs if provided. In addition, optionally reads a hard prior on path
    assignment from `adata_rna.obs[prior_path_col]`, where integer entries 1..P indicate
    known path membership (converted to 0-based), and other values (None/NaN) are treated
    as unknown (-1) for inference.

    Parameters
    ----------
    adata_rna : AnnData
        AnnData object containing RNA expression data with 'spliced' and 'unspliced' layers.
    tf_list : List[str]
        List of transcription factor names.
    n_cells_col : str, optional
        Column name in `adata_rna.obs` representing the number of cells per metacell
        (default: "n_cells").
    prior_time_col : Optional[str], optional
        Column name in `adata_rna.obs` containing prior pseudotimes; if provided, used
        to center the prior over t_c (default: None).
    batch_annotation : Optional[str], optional
        Column name in `adata_rna.obs` that contains batch information; if provided,
        cells are assigned batch indices based on this column.
    prior_path_col : str, optional
        Column name in `adata_rna.obs` that contains a hard prior assignment (1-based)
        to path indices; missing or invalid entries become -1 (no prior).

    Returns
    -------
    Dict[str, Any]
        Dictionary containing:
          - `data`: JAX array of shape (cells, genes, 2) with stacked unspliced and spliced counts.
          - `M_c`: JAX array of shape (cells, 1, 1) holding the per-cell metacell size.
          - `batch_index`: JAX array of shape (cells,) with batch indices.
          - `tf_indices`: JAX array of TF gene indices.
          - `total_num_cells`: int, number of cells.
          - `n_batch`: int, number of batches.
          - `prior_time`: JAX array of prior times or None.
          - `prior_timespan`: float, span of prior_time or default.
          - `prior_path`: JAX int array of shape (cells,) with –1 or 0-based path ids.
          - `unknown_idx`: Python list of ints, indices of cells with unknown prior.
    """
    # 1) stack raw data
    spliced = np.array(adata_rna.layers["spliced"].toarray(), dtype=np.float32)
    unspliced = np.array(adata_rna.layers["unspliced"].toarray(), dtype=np.float32)
    data = jnp.array(np.stack([unspliced, spliced], axis=-1))

    # 2) metacell sizes
    M_c = jnp.array(
        np.expand_dims(np.expand_dims(adata_rna.obs[n_cells_col].to_numpy(), -1), -1),
        dtype=jnp.float32,
    )
    total_num_cells = int(data.shape[0])

    # 3) prior time
    if prior_time_col is not None:
        prior_time = jnp.array(
            adata_rna.obs[prior_time_col].to_numpy(), dtype=jnp.float32
        )
        prior_timespan = float(prior_time.max() - prior_time.min())
    else:
        prior_time = None

    # 4) batch index
    if batch_annotation is not None:
        batches = adata_rna.obs[batch_annotation].astype(str)
        uniq = batches.unique()
        mapping = {b: i for i, b in enumerate(uniq)}
        batch_index = jnp.array(batches.map(mapping).to_numpy(), dtype=jnp.int32)
    else:
        batch_index = jnp.zeros(total_num_cells, dtype=jnp.int32)
    n_batch = int(jnp.unique(batch_index).shape[0])

    # 5) TF indices
    is_tf = np.isin(adata_rna.var_names, tf_list)
    tf_indices = jnp.array(np.where(is_tf)[0], dtype=jnp.int32)

    # 6) prior path
    if prior_path_col is not None:
        raw_prior = adata_rna.obs[prior_path_col].to_numpy()
        prior_path = np.full(raw_prior.shape, -1, dtype=np.int32)
        for i, v in enumerate(raw_prior):
            if pd.notna(v):
                try:
                    prior_path[i] = int(v) - 1
                except:
                    prior_path[i] = -1
        prior_path = jnp.array(prior_path, dtype=jnp.int32)
    else:
        prior_path = jnp.full((total_num_cells,), -1, dtype=jnp.int32)
    unknown_idx = [int(i) for i, p in enumerate(prior_path) if int(p) < 0]

    # 7) Build Timegrid
    max_dt = 0.1
    if prior_time_col is None:
        T_min = -prior_timespan / 2.0
        T_max = +prior_timespan / 2.0
    else:
        T_min = prior_time.min() - prior_timespan / 6.0
        T_max = prior_time.max() + prior_timespan / 6.0

    n_steps = int(np.ceil((T_max - T_min) / max_dt))
    times_grid = jnp.asarray(T_min + np.arange(n_steps + 1) * max_dt)
    dt = times_grid[1:] - times_grid[:-1]

    return OrderedDict(
        [
            ("data", data),
            ("M_c", M_c),
            ("batch_index", batch_index),
            ("tf_indices", tf_indices),
            ("total_num_cells", total_num_cells),
            ("n_batch", n_batch),
            ("prior_time", prior_time),
            ("prior_timespan", prior_timespan),
            ("prior_path", prior_path),
            ("unknown_idx", unknown_idx),
            ("times_grid", times_grid),
            ("dt", dt),
            ("T_limits", (T_min, T_max)),
            ("max_dt", max_dt),
        ]
    )


def euler_maruyama(
    times_grid: jnp.ndarray,
    dt: jnp.ndarray,
    y0: jnp.ndarray,
    drift_fn,
    diffusion_fn,
    drift_args,
    diff_args,
    eps_grid: jnp.ndarray,
) -> jnp.ndarray:
    """
    Perform Euler–Maruyama integration on a fixed time grid for multiple sample paths.

    Parameters:
    - times_grid (jnp.ndarray): 1D array of time points of length L.
    - dt (jnp.ndarray): 1D array of time step sizes between grid points, length L-1.
    - y0 (jnp.ndarray): Initial state for each path, shape (num_paths, num_genes, 3).
    - drift_fn (Callable): Function computing deterministic drift: f = drift_fn(t, y, drift_args).
    - diffusion_fn (Callable): Function computing stochastic diffusion: g = diffusion_fn(t, y, diff_args).
    - drift_args (Any): Extra arguments to pass to drift_fn.
    - diff_args (Any): Extra arguments to pass to diffusion_fn.
    - eps_grid (jnp.ndarray): Pre-sampled Gaussian noise, shape (num_paths, L-1, num_genes).

    Returns:
    - jnp.ndarray: Simulated state trajectory, shape (L, num_paths, num_genes, 3).
    """
    eps = jnp.swapaxes(eps_grid, 0, 1)

    def body_fn(carry, inputs):
        y_prev, t_prev = carry
        eps_i, dt_i = inputs
        f = drift_fn(t_prev, y_prev, drift_args) * dt_i
        g = diffusion_fn(t_prev, y_prev, diff_args)
        stoch = g * (jnp.sqrt(dt_i)[None, None, None] * eps_i[..., None])
        y_new = y_prev + f + stoch
        return (y_new, t_prev + dt_i), y_new

    (y_last, _), ys = jax.lax.scan(body_fn, (y0, times_grid[0]), (eps, dt))
    return jnp.concatenate([y0[None], ys], axis=0)


def interpolate_solution(
    sol_grid: jnp.ndarray,
    times_grid: jnp.ndarray,
    T_c: jnp.ndarray,
) -> jnp.ndarray:
    """
    Linearly interpolate a precomputed solution grid at specified cell times.

    Parameters:
    - sol_grid (jnp.ndarray): Solution values on a regular time grid, shape (L, num_paths, num_genes, 3).
    - times_grid (jnp.ndarray): 1D array of time points corresponding to sol_grid, length L.
    - T_c (jnp.ndarray): Array of arbitrary times at which to interpolate, shape (num_cells,).

    Returns:
    - jnp.ndarray: Interpolated solution at each time in T_c, shape (num_cells, num_paths, num_genes, 3).
    """
    idx0 = jnp.searchsorted(times_grid, T_c, side="right") - 1
    idx0 = jnp.clip(idx0, 0, sol_grid.shape[0] - 2)
    t0 = times_grid[idx0]
    t1 = times_grid[idx0 + 1]
    sol0 = sol_grid[idx0]
    sol1 = sol_grid[idx0 + 1]
    w = ((T_c - t0) / (t1 - t0))[..., None, None, None]
    return sol0 * (1 - w) + sol1 * w


@beartype
def mlp(
    params: Dict,
    x: Any,
) -> Any:
    """
    One or Multilayer Perceptron (MLP) with residual connections.

    Args:
        params: Dictionary containing neural network parameters (weights and biases).
        x: Input data array.

    Returns:
        Output array after passing through the MLP.
    """

    # First hidden layer with residual connections
    out = jnp.dot(x, params["W"]) + params["b"]
    out = jax.nn.softplus(out)

    return out


def diffusion_fn(t, y, diff_args):
    """
    Compute the diffusion term for the SDE, nonzero only on the protein dimension
    for specified transcription factor genes.

    Parameters:
    - t (float): Current time.
    - y (jnp.ndarray): Current state array, shape (num_paths, num_genes, 3).
    - diff_args (tuple): Tuple containing:
        - sigma_tf (jnp.ndarray): Diffusion strengths for each TF, shape (num_tfs,).
        - tf_indices (array-like): Indices of transcription factor genes.

    Returns:
    - jnp.ndarray: Diffusion contribution, same shape as y.
    """
    sigma_tf, tf_indices = diff_args
    return jnp.zeros_like(y).at[:, tf_indices, 2].set(sigma_tf[None, :])


@beartype
def drift_fn(t, state, args):
    """
    Compute the deterministic drift for the coupled transcription–splicing–protein system.

    Parameters:
    - t (float): Current time.
    - state (jnp.ndarray): Current state, shape (num_paths, num_genes, 3), containing
      unspliced (u), spliced (s), and protein (p) counts.
    - args (tuple): Tuple containing:
        - alpha_0 (jnp.ndarray): Baseline transcription rates, shape (num_genes,).
        - beta_g (jnp.ndarray): Splicing rates per gene, shape (num_genes,).
        - gamma_g (jnp.ndarray): Degradation rates per gene, shape (num_genes,).
        - lamda (jnp.ndarray): Translation rates for TF proteins, shape (num_tfs,).
        - kappa (jnp.ndarray): Protein degradation rates for TFs, shape (num_tfs,).
        - nn_params (dict): Neural network parameters for computing regulation.
        - tf_indices (array-like): Indices of transcription factor genes.
        - T_ON (float): Switch-on time threshold.

    Returns:
    - jnp.ndarray: Time derivative of the state, same shape as state.
    """
    alpha_0, beta_g, gamma_g, lamda, kappa, nn_params, tf_indices = args
    u = jnp.clip(state[..., 0], 0, 1e3)
    s = jnp.clip(state[..., 1], 0, 1e3)
    p = jnp.clip(state[..., 2], 0, 1e3)

    alpha = alpha_0 * jnp.clip(mlp(nn_params, p[:, tf_indices]), 0, 1e3)
    du_dt = alpha - beta_g * u
    ds_dt = beta_g * u - gamma_g * s

    dp_dt = jnp.zeros_like(u)
    dp_dt = dp_dt.at[:, tf_indices].set(
        lamda * s[:, tf_indices] - kappa * p[:, tf_indices]
    )

    return jnp.stack([du_dt, ds_dt, dp_dt], axis=-1)


# Define the complete NumPyro model
@beartype
def model(
    data: Any,
    M_c: Any,
    batch_index: Any,
    tf_indices: Any,
    total_num_cells: int,
    n_batch: int,
    prior_time: Any,
    prior_timespan: Any,
    prior_path: Any,
    unknown_idx: Any,
    times_grid: Any,
    dt: Any,
    T_limits: Any,
    max_dt: Any,
    num_paths: int,
    return_alpha: bool = False,
    Tmax_alpha: float = 50.0,
    Tmax_beta: float = 1.0,
    splicing_rate_alpha_hyp_prior_alpha: float = 20.0,
    splicing_rate_alpha_hyp_prior_mean: float = 5.0,
    splicing_rate_mean_hyp_prior_alpha: float = 10.0,
    splicing_rate_mean_hyp_prior_mean: float = 1.0,
    degradation_rate_alpha_hyp_prior_alpha: float = 20.0,
    degradation_rate_alpha_hyp_prior_mean: float = 5.0,
    degradation_rate_mean_hyp_prior_alpha: float = 10.0,
    degradation_rate_mean_hyp_prior_mean: float = 1.0,
    transcription_rate_alpha_hyp_prior_alpha: float = 20.0,
    transcription_rate_alpha_hyp_prior_mean: float = 2.0,
    transcription_rate_mean_hyp_prior_alpha: float = 10.0,
    transcription_rate_mean_hyp_prior_mean: float = 5.0,
    lambda_alpha: float = 1.0,
    lambda_mean: float = 1.0,
    kappa_alpha: float = 1.0,
    kappa_mean: float = 1.0,
    detection_mean_hyp_prior_alpha: float = 1.0,
    detection_mean_hyp_prior_beta: float = 1.0,
    detection_hyp_prior_alpha: float = 10.0,
    detection_i_prior_alpha: float = 100.0,
    detection_gi_prior_alpha: float = 200.0,
    gene_add_alpha_hyp_prior_alpha: float = 9.0,
    gene_add_alpha_hyp_prior_beta: float = 3.0,
    gene_add_mean_hyp_prior_alpha: float = 1.0,
    gene_add_mean_hyp_prior_beta: float = 100.0,
    stochastic_v_ag_hyp_prior_alpha: float = 9.0,
    stochastic_v_ag_hyp_prior_beta: float = 3.0,
    sde_rng_key=0,
):
    """
    NumPyro model for coupled transcription and splicing dynamics.

    Args:
        data: Observed data array of shape (num_cells, num_genes, num_modalities).
        M_c: Number of cells in each metacell.
        batch_index: Array indicating batch assignments for each cell.
        tf_indices: Indices of genes that are TFs.
        total_num_cells: Number of cells in the full dataset.
        n_batch: Number of batches.
        Tmax_alpha: Alpha parameter for Tmax prior.
        Tmax_beta: Beta parameter for Tmax prior.
        ... (other hyperparameters for priors)
        key: Random number generator key.

    Returns:
        None. Defines the probabilistic model for inference.
    """

    num_cells = int(data.shape[0])
    num_genes = int(data.shape[1])
    num_modalities = int(data.shape[2])
    num_tfs = tf_indices.shape[0]
    batch_size = num_cells
    obs2sample = jax.nn.one_hot(batch_index, num_classes=n_batch)

    # Splicing Rates for mRNA
    α_sa = splicing_rate_alpha_hyp_prior_alpha
    μ_sa = splicing_rate_alpha_hyp_prior_mean
    σ2_sa = μ_sa**2 / α_sa
    σ_sa = jnp.sqrt(jnp.log1p(σ2_sa / μ_sa**2))
    loc_sa = jnp.log(μ_sa) - 0.5 * σ_sa**2
    splicing_alpha = numpyro.sample("splicing_alpha", dist.LogNormal(loc_sa, σ_sa))

    α_sm = splicing_rate_mean_hyp_prior_alpha
    μ_sm = splicing_rate_mean_hyp_prior_mean
    σ2_sm = μ_sm**2 / α_sm
    σ_sm = jnp.sqrt(jnp.log1p(σ2_sm / μ_sm**2))
    loc_sm = jnp.log(μ_sm) - 0.5 * σ_sm**2
    splicing_mean = numpyro.sample("splicing_mean", dist.LogNormal(loc_sm, σ_sm))

    μ_bg = splicing_mean
    σ2_bg = μ_bg**2 / splicing_alpha
    σ_bg = jnp.sqrt(jnp.log1p(σ2_bg / μ_bg**2))
    loc_bg = jnp.log(μ_bg) - 0.5 * σ_bg**2
    beta_g = numpyro.sample(
        "beta_g",
        dist.LogNormal(loc_bg, σ_bg).expand([num_genes]).to_event(1),
    )

    # Degradation Rates for mRNA
    α_da = degradation_rate_alpha_hyp_prior_alpha
    μ_da = degradation_rate_alpha_hyp_prior_mean
    σ2_da = μ_da**2 / α_da
    σ_da = jnp.sqrt(jnp.log1p(σ2_da / μ_da**2))
    loc_da = jnp.log(μ_da) - 0.5 * σ_da**2
    degradation_alpha = numpyro.sample(
        "degradation_alpha", dist.LogNormal(loc_da, σ_da)
    )

    α_dm = degradation_rate_mean_hyp_prior_alpha
    μ_dm = degradation_rate_mean_hyp_prior_mean
    σ2_dm = μ_dm**2 / α_dm
    σ_dm = jnp.sqrt(jnp.log1p(σ2_dm / μ_dm**2))
    loc_dm = jnp.log(μ_dm) - 0.5 * σ_dm**2
    degradation_mean = numpyro.sample("degradation_mean", dist.LogNormal(loc_dm, σ_dm))

    μ_gg = degradation_mean
    σ2_gg = μ_gg**2 / degradation_alpha
    σ_gg = jnp.sqrt(jnp.log1p(σ2_gg / μ_gg**2))
    loc_gg = jnp.log(μ_gg) - 0.5 * σ_gg**2
    gamma_g = numpyro.sample(
        "gamma_g",
        dist.LogNormal(loc_gg, σ_gg).expand([num_genes]).to_event(1),
    )

    # Translation rate for proteins
    α_la = lambda_alpha
    μ_la = lambda_mean
    σ2_la = μ_la**2 / α_la
    σ_la = jnp.sqrt(jnp.log1p(σ2_la / μ_la**2))
    loc_la = jnp.log(μ_la) - 0.5 * σ_la**2
    lamda = numpyro.sample(
        "lambda",
        dist.LogNormal(loc_la, σ_la).expand([num_tfs]).to_event(1),
    )

    # Degradation rate for proteins
    α_ka = kappa_alpha
    μ_ka = kappa_mean
    σ2_ka = μ_ka**2 / α_ka
    σ_ka = jnp.sqrt(jnp.log1p(σ2_ka / μ_ka**2))
    loc_ka = jnp.log(μ_ka) - 0.5 * σ_ka**2
    kappa = numpyro.sample(
        "kappa",
        dist.LogNormal(loc_ka, σ_ka).expand([num_tfs]).to_event(1),
    )

    # Time Parameters
    prior_time_sd = prior_timespan / 6
    if prior_time is None:
        with numpyro.plate("cells", batch_size):
            t_c = numpyro.sample(
                "t_c",
                dist.TruncatedNormal(
                    low=T_limits[0], high=T_limits[1], loc=0, scale=prior_time_sd
                ),
            )
            T_c = numpyro.deterministic("T_c", t_c)
    else:
        T_scaling = numpyro.sample("T_scaling", dist.Beta(2.0, 1.0))
        with numpyro.plate("cells", batch_size):
            t_c = numpyro.sample(
                "t_c",
                dist.TruncatedNormal(
                    loc=prior_time,
                    scale=prior_time_sd,
                    low=T_limits[0],
                    high=T_limits[1],
                ),
            )
            T_c = numpyro.deterministic("T_c", T_scaling * t_c)

    # ============= Expression model =============== #

    # Transcription scale:
    μ_a0, σ2_a0 = 1.0, 1.0
    σ_a0 = jnp.sqrt(jnp.log1p(σ2_a0 / μ_a0**2))
    loc_a0 = jnp.log(μ_a0) - 0.5 * σ_a0**2
    alpha_0 = numpyro.sample(
        "alpha_0",
        dist.LogNormal(loc_a0, σ_a0).expand([num_genes]).to_event(1),
    )

    # Initial Condition
    α_ic2, rate_ic2 = 2.0, 0.5
    μ_ic2, σ2_ic2 = α_ic2 / rate_ic2, α_ic2 / rate_ic2**2
    σ_ic2 = jnp.sqrt(jnp.log1p(σ2_ic2 / μ_ic2**2))
    loc_ic2 = jnp.log(μ_ic2) - 0.5 * σ_ic2**2
    init_center_2d = numpyro.sample(
        "init_center_2d",
        dist.LogNormal(loc_ic2, σ_ic2).expand([num_genes, 2]).to_event(2),
    )

    μ_icf, σ2_icf = μ_ic2, σ2_ic2
    σ_icf = σ_ic2
    loc_icf = loc_ic2
    init_center_tf = numpyro.sample(
        "init_center_tf",
        dist.LogNormal(loc_icf, σ_icf).expand([len(tf_indices)]).to_event(1),
    )

    σ_dev = 0.1
    jitter_2d = numpyro.sample(
        "jitter_2d",
        dist.Normal(0.0, σ_dev).expand([num_paths, num_genes, 2]).to_event(3),
    )
    jitter_tf = numpyro.sample(
        "jitter_tf",
        dist.Normal(0.0, σ_dev).expand([num_paths, len(tf_indices)]).to_event(2),
    )

    initial_state_2d = init_center_2d[None, :, :] + jitter_2d
    third_dim = jnp.zeros((num_paths, num_genes))
    third_dim = third_dim.at[:, tf_indices].set(init_center_tf[None, :] + jitter_tf)
    initial_state = jnp.concatenate([initial_state_2d, third_dim[..., None]], axis=-1)

    numpyro.deterministic("initial_state", initial_state)

    # Neural Net params
    rng = jax.random.PRNGKey(0)
    P = numpyro.param
    in_dim = num_tfs
    out_dim = num_genes
    nn_params = {
        "W": P("W", jax.random.normal(rng, (in_dim, out_dim)) * 0.01),
        "b": P("b", jnp.zeros((out_dim,))),
    }

    # per‐TF diffusion variance:
    # (we should change this to a sparse or containment prior later)
    log_sigma_tf = numpyro.sample(
        "log_sigma_tf",
        dist.Normal(-3.0, 0.01).expand([num_tfs]).to_event(1),
    )
    sigma_tf = jnp.exp(log_sigma_tf)

    ode_args = (alpha_0, beta_g, gamma_g, lamda, kappa, nn_params, tf_indices)
    diff_args = (sigma_tf, tf_indices)

    # —— path_weights —— #
    if prior_path is None:
        one_hot = jnp.zeros((batch_size, num_paths))
        unknown_idx = list(range(batch_size))
    else:
        one_hot = jax.nn.one_hot(prior_path, num_paths)  # (N, K)
        unknown_idx = unknown_idx  # comes in as a Python list

    n_unknown = len(unknown_idx)

    # sample only for unknown cells:
    w_unknown = numpyro.sample(
        "path_weights_unknown",
        dist.Dirichlet(jnp.ones(num_paths)).expand([n_unknown]).to_event(1),
    )

    # paste them back into a full array:
    path_weights = one_hot
    for j, i in enumerate(unknown_idx):
        path_weights = path_weights.at[i].set(w_unknown[j])

    numpyro.deterministic("path_weights", path_weights)  # (N, K)

    # the “importance” of each path:
    path_counts = jnp.sum(path_weights, axis=0)  # shape (num_paths,)

    eps_list = []
    for k in range(num_paths):
        # each path’s noise‐log‐prob is weighted by how many cells sit on that path:
        with scale(scale=path_counts[k]):
            eps_k = numpyro.sample(
                f"eps_grid_{k}",
                dist.Normal(0.0, 1.0).expand([dt.shape[0], num_genes]).to_event(2),
            )
        eps_list.append(eps_k)
    eps_grid = jnp.stack(eps_list, axis=0)

    # integrate once on the grid
    sol_grid = euler_maruyama(
        times_grid,
        dt,
        initial_state,
        drift_fn,
        diffusion_fn,
        ode_args,
        diff_args,
        eps_grid,
    )

    # interpolate each cell at its own time T_c
    sol_at_cells = numpyro.deterministic(
        "sol_at_cells", interpolate_solution(sol_grid, times_grid, T_c)
    )

    # weighted average over paths
    weighted_preds = numpyro.deterministic(
        "predictions_rearranged",
        jnp.sum(sol_at_cells * path_weights[:, :, None, None], axis=1),
    )

    # use weighted_preds[..., :2] as mu_expression downstream
    mu_expression = jnp.clip(weighted_preds[..., :2], a_min=1e-5, a_max=1e5)

    # Detection efficiencies
    α_dme, μ_dme = detection_mean_hyp_prior_alpha, detection_mean_hyp_prior_beta

    detection_mean_y_e = numpyro.sample(
        "detection_mean_y_e",
        dist.Beta(
            jnp.ones((1, 1)) * α_dme,
            jnp.ones((1, 1)) * μ_dme,
            validate_args=True,
        )
        .expand([n_batch, 1])
        .to_event(2),
    )
    beta = (detection_hyp_prior_alpha / (obs2sample @ detection_mean_y_e)).T[0]

    # detection_y_c
    μ_dyc = beta
    σ2_dyc = μ_dyc**2 / detection_hyp_prior_alpha
    σ_dyc = jnp.sqrt(jnp.log1p(σ2_dyc / μ_dyc**2))
    loc_dyc = jnp.log(μ_dyc) - 0.5 * σ_dyc**2
    with numpyro.plate("cells", batch_size):
        detection_y_c = numpyro.sample("detection_y_c", dist.LogNormal(loc_dyc, σ_dyc))

    # detection_y_i
    μ_dyi = detection_i_prior_alpha / detection_i_prior_alpha  # =1
    σ2_dyi = μ_dyi**2 / detection_i_prior_alpha
    σ_dyi = jnp.sqrt(jnp.log1p(σ2_dyi / μ_dyi**2))
    loc_dyi = jnp.log(μ_dyi) - 0.5 * σ_dyi**2
    detection_y_i = numpyro.sample(
        "detection_y_i",
        dist.LogNormal(loc_dyi, σ_dyi).expand([1, 1, 2]).to_event(3),
    )

    # detection_y_gi
    μ_dyg = detection_gi_prior_alpha / detection_gi_prior_alpha  # =1
    σ2_dyg = μ_dyg**2 / detection_gi_prior_alpha
    σ_dyg = jnp.sqrt(jnp.log1p(σ2_dyg / μ_dyg**2))
    loc_dyg = jnp.log(μ_dyg) - 0.5 * σ_dyg**2
    detection_y_gi = numpyro.sample(
        "detection_y_gi",
        dist.LogNormal(loc_dyg, σ_dyg).expand([1, num_genes, 2]).to_event(3),
    )

    # Gene‐specific additive ambient RNA
    α_sag = gene_add_alpha_hyp_prior_alpha
    μ_sag = gene_add_alpha_hyp_prior_beta
    σ2_sag = μ_sag**2 / α_sag
    σ_sag = jnp.sqrt(jnp.log1p(σ2_sag / μ_sag**2))
    loc_sag = jnp.log(μ_sag) - 0.5 * σ_sag**2
    s_g_gene_add_alpha_hyp = numpyro.sample(
        "s_g_gene_add_alpha_hyp",
        dist.LogNormal(loc_sag, σ_sag),
        sample_shape=(2,),
    )
    α_sgm = gene_add_mean_hyp_prior_alpha
    μ_sgm = gene_add_mean_hyp_prior_beta
    σ2_sgm = μ_sgm**2 / α_sgm
    σ_sgm = jnp.sqrt(jnp.log1p(σ2_sgm / μ_sgm**2))
    loc_sgm = jnp.log(μ_sgm) - 0.5 * σ_sgm**2
    s_g_gene_add_mean = numpyro.sample(
        "s_g_gene_add_mean",
        dist.LogNormal(loc_sgm, σ_sgm).expand([n_batch, 1, 2]).to_event(3),
    )

    s_g_gene_add_alpha_e_inv = numpyro.sample(
        "s_g_gene_add_alpha_e_inv",
        dist.Exponential(s_g_gene_add_alpha_hyp).expand([n_batch, 1, 2]).to_event(3),
    )
    s_g_gene_add_alpha_e = 1.0 / s_g_gene_add_alpha_e_inv**2
    s_g_gene_add = numpyro.sample(
        "s_g_gene_add",
        dist.LogNormal(
            jnp.log(s_g_gene_add_alpha_e / s_g_gene_add_mean),
            jnp.sqrt(jnp.log1p(1.0 / s_g_gene_add_alpha_e)),
        )
        .expand([n_batch, num_genes, 2])
        .to_event(3),
    )

    # Overdispersion of NB likelihood:
    α_svh = stochastic_v_ag_hyp_prior_alpha
    μ_svh = stochastic_v_ag_hyp_prior_beta
    σ2_svh = μ_svh**2 / α_svh
    σ_svh = jnp.sqrt(jnp.log1p(σ2_svh / μ_svh**2))
    loc_svh = jnp.log(μ_svh) - 0.5 * σ_svh**2
    stochastic_v_ag_hyp = numpyro.sample(
        "stochastic_v_ag_hyp",
        dist.LogNormal(loc_svh, σ_svh).expand([1, 2]).to_event(2),
    )
    stochastic_v_ag_inv = numpyro.sample(
        "stochastic_v_ag_inv",
        dist.Exponential(stochastic_v_ag_hyp).expand([1, num_genes, 2]).to_event(3),
    )
    stochastic_v_ag = 1.0 / stochastic_v_ag_inv**2

    # Expected expression
    additive_term = numpyro.deterministic(
        "additive_term", jnp.einsum("cb,bgi->cgi", obs2sample, s_g_gene_add)
    )
    normalizing_term = numpyro.deterministic(
        "normalizing_term",
        detection_y_c[:, None, None] * detection_y_i * detection_y_gi * M_c,
    )
    mu = numpyro.deterministic("mu", (mu_expression + additive_term) * normalizing_term)

    # Data likelihood
    concentration = stochastic_v_ag * M_c
    rate = concentration / mu
    scale_factor = total_num_cells / batch_size
    with scale(scale=scale_factor):
        numpyro.sample("data_target", dist.GammaPoisson(concentration, rate), obs=data)
