#!/usr/bin/env bash
set -euo pipefail
ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
GENERATORS=(
  rsvp_hypercell
  tartan_recursive_tile
  semantic_operator_orbit
  hydra_persona_dyad
  hydra_crown
  xylomorphic_root_brain
  entropic_vortex_coil
  categorical_pushout_sculpture
  cognitive_phase_portrait
  admissibility_boundary_lattice
  repair_trace_weaver
  memory_event_log
  projection_collapse_chamber
  fiscal_reachability_terrain
)
for g in "${GENERATORS[@]}"; do "$ROOT_DIR/scripts/render_one_v4.sh" "$g"; done
echo "[v4] All stills rendered."
