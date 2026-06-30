from flyxion_sim.core import REGISTRY
import flyxion_sim.scene_runner

def test_registry_has_expected_generators():
    assert "rsvp_hypercell" in REGISTRY
    assert "admissibility_boundary_lattice" in REGISTRY
    assert "fiscal_reachability_terrain" in REGISTRY
    assert len(REGISTRY) >= 14
