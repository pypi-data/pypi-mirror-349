# Changelog

## [stormi-v0.3.0](https://github.com/pinellolab/stormi/compare/stormi-v0.2.9...stormi-v0.3.0) (2025-05-22)

### Features

* **AmortizedNormal.py:** Included option to pretrain NN weights to match time prior values before starting full training. ([30b574e](https://github.com/pinellolab/stormi/commit/30b574e8913f2ee02b0377e6fdf939f1eb6286bd))
* **AmortizeNormal:** Added K_rh_vector to hide_list because it is now a deterministic parameter. ([172f4ad](https://github.com/pinellolab/stormi/commit/172f4ad3484c853af05205aaf931b68293f8d1ab))
* **ATAC_RNA.py:** Added option to set prior on time, allowed all TFs to bind to all regions (but with different prior if motif is not present), replaced ATAC Poisson likelihood with NB. ([91069e1](https://github.com/pinellolab/stormi/commit/91069e124b2634e35ef35749ec2bb0896bf45890))
* **models:** Added new models to init file. ([0287063](https://github.com/pinellolab/stormi/commit/0287063f407710cb0268200f0ede15d0158ed13c))
* **models:** New ODE based model that can produce multiple diverging paths from similar initial conditions via highly-nonlinear transcription rate function based on 4-layer neural net. ([9ced532](https://github.com/pinellolab/stormi/commit/9ced5322f1644b2e613c483554ebae93c790d8ef))
* **models:** New SDE based model simulating multiple trajectories. ([d0fe24c](https://github.com/pinellolab/stormi/commit/d0fe24c67f77311bf4d13d32eebc1cbd9fa02067))
* **plotting:** Minor aesthetic changes to plotting functions. ([3c22cc9](https://github.com/pinellolab/stormi/commit/3c22cc97141a006f2b50a86061a72e22bda78bdc))
* **posterior:** New memory efficient extract posterior means function. ([fda5581](https://github.com/pinellolab/stormi/commit/fda55819eba5b0ffc1b372a607dd92cfdf054a74))
* **RNA_1layer.py:** Option to set prior on time and better modelling of experimental batch effects. ([9a96857](https://github.com/pinellolab/stormi/commit/9a96857e645139243bad1d17e29f3a3b70563c99))
* **RNA_ATAC_model:** Changed from Gamma to Lognormal prior for K_rh. Also increased mean from 10 to 100. ([6704850](https://github.com/pinellolab/stormi/commit/6704850fd149fc3f54d6d7f41a12e176b4a2fa44))
* **RNA_ATAC_model:** Simplified Time prior and introduced upper and lower bounds for faster inference. ([fc1af06](https://github.com/pinellolab/stormi/commit/fc1af064fd0f39555f5b5282340f5834d3d7ffee))
* **RNA_ATAC_model:** Temporarily removed ATAC counts from likelihood for easier debugging. ([4a7e0ec](https://github.com/pinellolab/stormi/commit/4a7e0ecd6c6f51755a8dc226b50917be5296b332))
* **RNA_utils:** xtracting prior knowledge of differentiation time and experimental batch identity. ([5d52f85](https://github.com/pinellolab/stormi/commit/5d52f85ba38ba4cb914a7911e1a845d5c81b9c87))
* **tests:** Tests for basic workflow with variational inference. ([ecf7cfa](https://github.com/pinellolab/stormi/commit/ecf7cfa8178d9bc8267b7a9f1c8eee4a88ba7787))
* **train:** Handling of minibatch training when prior time for cells is given. ([ad7df78](https://github.com/pinellolab/stormi/commit/ad7df78eefdb2b135851500cab415d8910ac57d3))

### Bug Fixes

* **posterior:**  jax.tree_map -> jax.tree_util.tree_map ([9df2ad7](https://github.com/pinellolab/stormi/commit/9df2ad71651ecaba39bc8b416075e824c0aae309))
* **preprocessing.py:** resolve bug in precompute_mapping function and replace with simpler function. ([52d5a86](https://github.com/pinellolab/stormi/commit/52d5a867078057851268358d671d34ff6f798f1d))
* **RNA_ATAC_dstate_dt:** fixed wrong indexing ([feaccd2](https://github.com/pinellolab/stormi/commit/feaccd214fa37bb9d8eb61dfc3d53490bc5153dd))
* **RNA_ATAC_model:** Decreased pior biased to put prior predicted counts on more realistic scale. ([9e55764](https://github.com/pinellolab/stormi/commit/9e5576469ebe90f16c5bea2602be0b4db4426b7c))
* **RNA_ATAC_model:** fixed size of kappa and lambda to be only number of TFs ([ddc6d15](https://github.com/pinellolab/stormi/commit/ddc6d1501187b97c40c4a6b06eb641b0d285f976))
* **RNA_ATAC_model:** Removed StudentT distribution in favor of Normal for w_grh, because it's more stable. also decreased variance to put prior predicted counts on more realistic scale. ([f61b058](https://github.com/pinellolab/stormi/commit/f61b058032f22af6299a240a0213f8ccd1ec3554))
* **test_workflow1.py:** Fix training argments to remove pytest error. ([db00dc2](https://github.com/pinellolab/stormi/commit/db00dc26d4fd7583f9d7e897b60f5711afac6a17))
