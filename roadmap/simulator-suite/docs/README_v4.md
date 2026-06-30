# Flyxion Simulation Suite v4

v4 refactors the v3.3 Blender still-render suite into a small generator framework. The old scripts are preserved under `legacy_v3/`, while the new version adds a registry, shared scene utilities, JSON configuration, parameter sweeps, metadata sidecars, and a Blender-oriented Dockerfile.

The suite is still concept-first rather than physically exact. It treats RSVP, HYDRA, TARTAN, MEM|8, CLIO, repair theory, admissibility geometry, fiscal reachability, and category-theoretic forms as procedural objects that can be rendered, varied, and archived.

## What changed from v3.3

The main change is architectural. v3.3 executed independent Python files directly inside Blender. v4 gives every object a registered generator with a common function signature:

```python
build(config: RenderConfig, params: dict) -> None
```

The runner initializes the scene once, applies a shared camera/light/render profile, calls the selected generator, saves the `.blend`, and writes a JSON metadata sidecar. This makes one-off renders, batch sweeps, and future animation hooks much easier.

## Generators

Core inherited objects include `rsvp_hypercell`, `tartan_recursive_tile`, `semantic_operator_orbit`, `hydra_persona_dyad`, `hydra_crown`, `xylomorphic_root_brain`, `entropic_vortex_coil`, `categorical_pushout_sculpture`, and `cognitive_phase_portrait`.

New v4 objects include `admissibility_boundary_lattice`, `repair_trace_weaver`, `memory_event_log`, `projection_collapse_chamber`, and `fiscal_reachability_terrain`.

## Usage

Render one object:

```bash
cd v4
./scripts/render_one_v4.sh rsvp_hypercell
```

Render everything:

```bash
cd v4
./scripts/render_all_v4.sh
```

Run a small parameter sweep:

```bash
cd v4
python scripts/render_batch_v4.py configs/batch.example.json
```

Outputs go to `output_v4/`. Logs go to `logs_v4/`. Each render produces a `.blend`, a `.png`, and a `.metadata.json` file.

## Custom parameters

Create a parameter file:

```json
{
  "spark_count": 240,
  "seed": 42
}
```

Then render with:

```bash
PARAMS=params.json ./scripts/render_one_v4.sh rsvp_hypercell
```

## Docker

This project requires Blender, not only normal Python. The earlier scientific Python Dockerfile is therefore not sufficient for this suite. Build the Blender image from inside `v4/`:

```bash
docker build -f Dockerfile.blender -t flyxion-sim-v4 .
docker run --rm -v "$PWD/output_v4:/app/v4/output_v4" flyxion-sim-v4
```

## Design notes

The v4 framework separates three layers: shared scene mechanics in `flyxion_sim/core.py`, registered generators in `flyxion_sim/generators/`, and shell/Python entrypoints in `scripts/`. This keeps the symbolic object library readable while making automated rendering less brittle.
