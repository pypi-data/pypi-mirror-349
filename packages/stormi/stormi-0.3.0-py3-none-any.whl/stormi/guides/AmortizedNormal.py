from functools import partial

import jax
import jax.numpy as jnp
import numpyro
import numpyro.distributions as dist
import optax
from numpyro.handlers import block, seed
from numpyro.infer import SVI, Trace_ELBO
from numpyro.infer.autoguide import AutoGuideList, AutoNormal


def warm_up_guide(
    model,
    model_input: dict,
    predict_detection_l_c: bool = False,
    predict_detection_y_c: bool = False,
    n_steps: int = 100,
    seed: int = 0,
) -> dict:
    """
    Warm‐start the amortization network so that at iteration 0, t_c ~ its prior.

    Internally:
      - Defines a tiny “prior‐only” model that only samples t_c ~ TruncatedNormal(prior_time,…).
      - Uses SVI with **only** the amortized guide (no AutoNormal global part).
      - Runs `n_steps` of Adam(1e-3) on that prior‐only objective.
      - Returns the learned `numpyro.param` dict for the amortization network.

    Parameters
    ----------
    model
        Your full NumPyro model (only needed to inspect signature).
    model_input
        Output of `prepare_model_input(...)`, must contain keys:
          - "data": jnp.ndarray, shape (n_cells, n_genes, n_mods)
          - "prior_time": jnp.ndarray, shape (n_cells,)
          - "prior_timespan": float
          - "T_limits": tuple (low, high)
    predict_detection_l_c
        Whether your amortized guide also predicts `detection_l_c`.
    n_steps
        How many warm‐up gradient steps to take.
    seed
        RNG seed for reproducibility.

    Returns
    -------
    warmup_params : dict
        A `name→array` mapping of **only** those NN parameters in the amortized guide,
        ready to pass to `AmortizedNormal(..., init_net_params=warmup_params)`.
    """
    # 1) build the pure‐amortized guide
    from stormi.guides.AmortizedNormal import amortized_guide  # your existing function

    amortized_fn = partial(
        amortized_guide,
        predict_detection_l_c=predict_detection_l_c,
        predict_detection_y_c=predict_detection_y_c,
        init_net_params=None,  # start from scratch
    )

    # 2) define a minimal prior‐only model
    def prior_only_t_model(data, prior_time, T_limits, prior_time_sd):
        n_cells = prior_time.shape[0]
        with numpyro.plate("cells", n_cells):
            numpyro.sample(
                "t_c",
                dist.TruncatedNormal(
                    loc=prior_time,
                    scale=prior_time_sd,
                    low=T_limits[0],
                    high=T_limits[1],
                ),
            )

    # 3) extract constants
    data = model_input["data"]
    prior_time = model_input["prior_time"]  # (n_cells,)
    T_limits = model_input["T_limits"]  # (low, high)
    prior_time_sd = model_input["prior_timespan"] / 6.0

    # 4) set up SVI
    optimizer = optax.adam(learning_rate=1e-3)
    svi = SVI(prior_only_t_model, amortized_fn, optimizer, loss=Trace_ELBO())

    # 5) init
    rng = jax.random.PRNGKey(seed)
    state = svi.init(
        rng,
        data=data,
        prior_time=prior_time,
        T_limits=T_limits,
        prior_time_sd=prior_time_sd,
    )

    # 6) warm‐up loop
    for _ in range(n_steps):
        rng, subkey = jax.random.split(rng)
        state, _ = svi.update(
            state,
            data=data,
            prior_time=prior_time,
            T_limits=T_limits,
            prior_time_sd=prior_time_sd,
        )

    # 7) return only the NN params
    return svi.get_params(state)


################################################################################
# 1) Shared forward pass function: _amortized_network
################################################################################


def _amortized_network(params_dict: dict, data_array: jnp.ndarray):
    """
    Performs the forward pass of the neural network for the amortized guide,
    returning loc/scale for 't_c', optionally followed by loc/scale for
    'detection_y_c', and optionally by loc/scale for 'detection_l_c'.
    """

    def normalize_by_total_counts(data_2d):
        total_counts = jnp.sum(data_2d, axis=1, keepdims=True)
        return data_2d / (total_counts + 1e-8)

    n_cells, n_genes, n_mods = data_array.shape
    d_in = n_genes * n_mods

    data_2d = data_array.reshape((n_cells, d_in))
    data_2d_log1p = jnp.log1p(normalize_by_total_counts(data_2d))

    # Shared layers for t_c
    V_shared = params_dict["V_shared"]
    c_shared = params_dict["c_shared"]
    hidden_shared = jax.nn.elu(
        jnp.einsum("cd,dh->ch", data_2d_log1p, V_shared) + c_shared
    )

    # t_c branch
    V_t_c = params_dict["V_t_c"]
    c_t_c = params_dict["c_t_c"]
    V_out_t_c = params_dict["V_out_t_c"]
    c_out_t_c = params_dict["c_out_t_c"]
    hidden_t_c = jax.nn.elu(jnp.einsum("ch,hm->cm", hidden_shared, V_t_c) + c_t_c)
    out_t_c = jnp.einsum("cm,mo->co", hidden_t_c, V_out_t_c) + c_out_t_c
    loc_t_c = out_t_c[:, 0]
    scale_t_c = jax.nn.softplus(out_t_c[:, 1]) + 1e-3

    # start building the output tuple
    outputs = [loc_t_c, scale_t_c]

    # detection_y_c branch (optional)
    if "V_det" in params_dict:
        V_det = params_dict["V_det"]
        c_det = params_dict["c_det"]
        V_out_det = params_dict["V_out_det"]
        c_out_det = params_dict["c_out_det"]
        hidden_det = jax.nn.elu(jnp.einsum("ch,hm->cm", hidden_shared, V_det) + c_det)
        out_det = jnp.einsum("cm,mo->co", hidden_det, V_out_det) + c_out_det
        loc_det = out_det[:, 0]
        scale_det = jax.nn.softplus(out_det[:, 1]) + 1e-3
        outputs += [loc_det, scale_det]

    # detection_l_c branch (optional)
    if "V_det_l" in params_dict:
        V_det_l = params_dict["V_det_l"]
        c_det_l = params_dict["c_det_l"]
        V_out_det_l = params_dict["V_out_det_l"]
        c_out_det_l = params_dict["c_out_det_l"]
        hidden_det_l = jax.nn.elu(
            jnp.einsum("ch,hm->cm", hidden_shared, V_det_l) + c_det_l
        )
        out_det_l = jnp.einsum("cm,mo->co", hidden_det_l, V_out_det_l) + c_out_det_l
        loc_det_l = out_det_l[:, 0]
        scale_det_l = jax.nn.softplus(out_det_l[:, 1]) + 1e-3
        outputs += [loc_det_l, scale_det_l]

    return tuple(outputs)


################################################################################
# 2) The amortized_guide function
################################################################################


def amortized_guide(
    *args,
    predict_detection_l_c: bool = True,
    predict_detection_y_c: bool = True,
    init_net_params: dict = None,
    **kwargs,
):
    """
    Amortized guide for 't_c', optionally 'detection_y_c', and optionally 'detection_l_c',
    with optional warm-start of NN parameters via init_net_params.
    """

    # 1) Retrieve data
    data = kwargs.get("data", None)
    if data is None and args:
        data = args[0]
    if data is None:
        raise ValueError(
            "amortized_guide expects 'data' as a keyword or first positional argument!"
        )

    # 2) Data shape
    n_cells, n_genes, n_mods = data.shape
    d_in = n_genes * n_mods

    # 3) Network dimensions
    hidden_dim_shared = 256
    hidden_dim_t_c = 128
    hidden_dim_det = 128
    out_dim = 2  # (loc, scale)

    # 4) Helpers for parameter initialization
    def default_init(rng, shape):
        return jax.random.normal(jax.lax.stop_gradient(rng), shape) * 0.01

    def make_param(name, shape, rng):
        if init_net_params and name in init_net_params:
            return init_net_params[name]
        return default_init(rng, shape)

    # 5) Define NN parameters via numpyro.param
    V_shared = numpyro.param(
        "V_shared",
        make_param("V_shared", (d_in, hidden_dim_shared), jax.random.PRNGKey(1)),
    )
    c_shared = numpyro.param(
        "c_shared", make_param("c_shared", (hidden_dim_shared,), jax.random.PRNGKey(1))
    )

    V_t_c = numpyro.param(
        "V_t_c",
        make_param("V_t_c", (hidden_dim_shared, hidden_dim_t_c), jax.random.PRNGKey(2)),
    )
    c_t_c = numpyro.param(
        "c_t_c", make_param("c_t_c", (hidden_dim_t_c,), jax.random.PRNGKey(2))
    )
    V_out_t_c = numpyro.param(
        "V_out_t_c",
        make_param("V_out_t_c", (hidden_dim_t_c, out_dim), jax.random.PRNGKey(3)),
    )
    c_out_t_c = numpyro.param(
        "c_out_t_c", make_param("c_out_t_c", (out_dim,), jax.random.PRNGKey(3))
    )

    net_params = {
        "V_shared": V_shared,
        "c_shared": c_shared,
        "V_t_c": V_t_c,
        "c_t_c": c_t_c,
        "V_out_t_c": V_out_t_c,
        "c_out_t_c": c_out_t_c,
    }

    if predict_detection_y_c:
        V_det = numpyro.param(
            "V_det",
            make_param(
                "V_det", (hidden_dim_shared, hidden_dim_det), jax.random.PRNGKey(4)
            ),
        )
        c_det = numpyro.param(
            "c_det", make_param("c_det", (hidden_dim_det,), jax.random.PRNGKey(4))
        )
        V_out_det = numpyro.param(
            "V_out_det",
            make_param("V_out_det", (hidden_dim_det, out_dim), jax.random.PRNGKey(5)),
        )
        c_out_det = numpyro.param(
            "c_out_det", make_param("c_out_det", (out_dim,), jax.random.PRNGKey(5))
        )
        net_params.update(
            {
                "V_det": V_det,
                "c_det": c_det,
                "V_out_det": V_out_det,
                "c_out_det": c_out_det,
            }
        )

    # 6) Optional detection_l_c branch
    if predict_detection_l_c:
        V_det_l = numpyro.param(
            "V_det_l",
            make_param(
                "V_det_l", (hidden_dim_shared, hidden_dim_det), jax.random.PRNGKey(6)
            ),
        )
        c_det_l = numpyro.param(
            "c_det_l", make_param("c_det_l", (hidden_dim_det,), jax.random.PRNGKey(6))
        )
        V_out_det_l = numpyro.param(
            "V_out_det_l",
            make_param("V_out_det_l", (hidden_dim_det, out_dim), jax.random.PRNGKey(7)),
        )
        c_out_det_l = numpyro.param(
            "c_out_det_l", make_param("c_out_det_l", (out_dim,), jax.random.PRNGKey(7))
        )
        net_params.update(
            {
                "V_det_l": V_det_l,
                "c_det_l": c_det_l,
                "V_out_det_l": V_out_det_l,
                "c_out_det_l": c_out_det_l,
            }
        )

    # 7) Forward pass: always returns at least (loc_t_c, scale_t_c),
    outputs = _amortized_network(net_params, data)

    # Unpack the minimal always-present pair
    loc_t_c, scale_t_c, *rest = outputs

    # Now build a list of (name, distribution) in exactly the order we want
    names = ["t_c"]
    dists = [dist.Normal(loc_t_c, scale_t_c)]

    # `rest` will be [loc_y, scale_y, loc_l, scale_l] (or shorter)
    idx = 0
    if predict_detection_y_c:
        loc_y, scale_y = rest[idx], rest[idx + 1]
        names.append("detection_y_c")
        dists.append(
            dist.TransformedDistribution(
                dist.Normal(loc_y, scale_y), dist.transforms.ExpTransform()
            )
        )
        idx += 2
    if predict_detection_l_c:
        loc_l, scale_l = rest[idx], rest[idx + 1]
        names.append("detection_l_c")
        dists.append(
            dist.TransformedDistribution(
                dist.Normal(loc_l, scale_l), dist.transforms.ExpTransform()
            )
        )
        idx += 2

    # 8) Single plate + loop
    with numpyro.plate("cells", n_cells):
        for name, site_dist in zip(names, dists):
            numpyro.sample(name, site_dist)

    return {}


################################################################################
# 3) Extraction helper functions
################################################################################


def extract_global_posterior_mean(guide, svi_state, svi):
    """
    Extract posterior means for global parameters from the AutoNormal sub-guide.
    This function uses the AutoNormal sub-guide's built-in transformation (via its median method).
    """
    auto_guide = guide._guides[0]  # AutoNormal sub-guide (global parameters)
    params = svi.get_params(svi_state)
    return auto_guide.median(params)


def extract_local_posterior_mean(guide, svi_state, svi, data):
    """
    Extract posterior means for local variables (from the amortized guide):
      - t_c mean = loc_t_c (Normal)
      - detection_y_c mean = exp(loc_det) (ExpTransform)
      - detection_l_c mean = exp(loc_det_l) (if available)
    """
    params = svi.get_params(svi_state)
    needed_keys = [
        "V_shared",
        "c_shared",
        "V_t_c",
        "c_t_c",
        "V_out_t_c",
        "c_out_t_c",
        "V_det",
        "c_det",
        "V_out_det",
        "c_out_det",
    ]
    # Add keys for detection_l_c if available.
    if "V_det_l" in params:
        needed_keys.extend(["V_det_l", "c_det_l", "V_out_det_l", "c_out_det_l"])

    for k in needed_keys:
        if k not in params:
            raise ValueError(
                f"Missing param '{k}' in SVI state, cannot extract local posterior means."
            )

    net_params = {k: params[k] for k in needed_keys}

    outputs = _amortized_network(net_params, data)
    if len(outputs) == 6:
        loc_t_c, scale_t_c, loc_det, scale_det, loc_det_l, scale_det_l = outputs
    else:
        loc_t_c, scale_t_c, loc_det, scale_det = outputs

    t_c_mean = loc_t_c
    detection_y_c_mean = jnp.exp(loc_det)

    result = {"t_c": t_c_mean, "detection_y_c": detection_y_c_mean}
    if len(outputs) == 6:
        detection_l_c_mean = jnp.exp(loc_det_l)
        result["detection_l_c"] = detection_l_c_mean

    return result


def extract_posterior_means(guide, svi_state, svi, data):
    """
    Convenience wrapper returning (global_means, local_means).
    """
    global_means = extract_global_posterior_mean(guide, svi_state, svi)
    local_means = extract_local_posterior_mean(guide, svi_state, svi, data)
    return global_means, local_means


################################################################################
# 4) The AmortizedNormal class
################################################################################


class AmortizedNormal:
    def __init__(
        self,
        model,
        predict_detection_l_c: bool = True,
        predict_detection_y_c: bool = True,
        init_net_params: dict = None,  # ← add this
        init_loc_fn=None,
    ):
        """
        A guide that hides t_c, detection_y_c (and optionally detection_l_c)
        from AutoNormal, delegating them to the amortized_guide function.
        """
        self.model = model
        self.predict_detection_l_c = predict_detection_l_c
        self.predict_detection_y_c = predict_detection_y_c  # ← also track y-c option
        self.init_net_params = init_net_params  # ← store it
        self.guide_list = AutoGuideList(model)

        # seed model for deterministic site ordering
        seeded_model = seed(model, rng_seed=0)

        # which sites to hide from the global AutoNormal
        hide_list = [
            "K_rh",
            "t_c",
            "detection_y_c",
            "T_c",
            "predictions",
            "mu",
            "d_cr",
            "mu_atac",
            "predictions_rearranged",
            "alpha_cg",
            "additive_term",
            "normalizing_term",
            "P_rh",
            "K_rh_vector",
        ]
        if predict_detection_l_c:
            hide_list.append("detection_l_c")

        blocked_model = block(seeded_model, hide=hide_list)
        auto_normal_guide = AutoNormal(blocked_model, init_loc_fn=init_loc_fn)
        self.guide_list.append(auto_normal_guide)

        # now append *our* amortized guide, passing through all three flags
        self.guide_list.append(
            partial(
                amortized_guide,
                predict_detection_l_c=self.predict_detection_l_c,
                predict_detection_y_c=self.predict_detection_y_c,
                init_net_params=self.init_net_params,  # ← pass it in
            )
        )

    def __call__(self, *args, **kwargs):
        return self.guide_list(*args, **kwargs)

    def quantiles(self, params, quantiles):
        return self.guide_list.quantiles(params, quantiles)

    def median(self, params):
        return self.guide_list.median(params)

    def sample_posterior(self, rng_key, params, sample_shape=()):
        return self.guide_list.sample_posterior(rng_key, params, sample_shape)

    def get_posterior(self, params):
        return self.guide_list.get_posterior(params)

    # ---- Additional convenience methods for extraction ----
    def extract_global_means(self, svi_state, svi):
        return extract_global_posterior_mean(self.guide_list, svi_state, svi)

    def extract_local_means(self, svi_state, svi, data):
        return extract_local_posterior_mean(self.guide_list, svi_state, svi, data)

    def extract_all_means(self, svi_state, svi, data):
        return extract_posterior_means(self.guide_list, svi_state, svi, data)
