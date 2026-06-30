from __future__ import annotations
import argparse
import importlib
import json
import sys
from pathlib import Path

from .core import RenderConfig, REGISTRY, clear_scene, setup_world, write_metadata

# Import generator modules for registration.
for mod in [
    "rsvp_hypercell_v4", "tartan_recursive_tile_v4", "semantic_operator_orbit_v4",
    "hydra_crown_v4", "xylomorphic_root_brain_v4", "admissibility_boundary_lattice_v4",
    "repair_trace_weaver_v4", "memory_event_log_v4", "projection_collapse_chamber_v4",
    "fiscal_reachability_terrain_v4", "categorical_pushout_sculpture_v4",
    "entropic_vortex_coil_v4", "cognitive_phase_portrait_v4", "hydra_persona_dyad_v4",
]:
    importlib.import_module(f"flyxion_sim.generators.{mod}")

def load_json(path: str | None) -> dict:
    if not path:
        return {}
    return json.loads(Path(path).read_text(encoding="utf-8"))

def main(argv=None) -> int:
    parser = argparse.ArgumentParser(description="Flyxion Simulation Suite v4 scene runner")
    parser.add_argument("--generator", required=True, choices=sorted(REGISTRY))
    parser.add_argument("--config", default=None)
    parser.add_argument("--params", default=None)
    parser.add_argument("--blend-out", default=None)
    parser.add_argument("--metadata-out", default=None)
    args = parser.parse_args(argv)

    config_data = load_json(args.config)
    params_data = load_json(args.params)
    config = RenderConfig(**config_data)
    spec = REGISTRY[args.generator]
    params = {**spec.defaults, **params_data}

    clear_scene()
    setup_world(config)
    spec.builder(config, params)

    if args.metadata_out:
        write_metadata(Path(args.metadata_out), config, args.generator, params)
    if args.blend_out:
        import bpy
        bpy.ops.wm.save_mainfile(filepath=args.blend_out)
    return 0

if __name__ == "__main__":
    if "--" in sys.argv:
        user_args = sys.argv[sys.argv.index("--") + 1:]
    else:
        user_args = sys.argv[1:]
    raise SystemExit(main(user_args))
