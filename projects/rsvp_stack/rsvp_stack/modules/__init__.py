# rsvp_stack/modules/__init__.py
# Expose modules for convenience. Real modules are implemented in separate files.
from . import rsvp_torch, ebssc_torch, spherepop, tartan_torch, clio_torch

# jax modules are optional (only import if jax available)
try:
    from . import rsvp_jax, clio_jax
except Exception:
    pass

