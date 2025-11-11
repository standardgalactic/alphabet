# RSVP Stack

A modular, plugin‑driven research framework for the RSVP cosmology + agency stack.

## Features
- Hydra CLI configuration
- Auto‑discovered plugins (flat `modules/` namespace)
- Torch & JAX backends
- Weights & Biases logging
- GPU/TPU‑ready Docker support
- `pip install` ready
- CLI:
  - `rsvp-run presets=cosmology`
  - `rsvp-train backend=jax`

## Install
```bash
pip install -e .
```

## Run
```bash
rsvp-run
rsvp-train presets=agency backend=torch
```

## Plugins
Drop any `.py` file into `rsvp_stack/modules/` to auto‑register.
