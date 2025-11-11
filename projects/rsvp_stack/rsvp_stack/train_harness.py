def get_device(prefer=None):
    try:
        import torch
        if prefer == 'cuda' or (prefer is None and torch.cuda.is_available()):
            return 'cuda'
    except Exception:
        pass
    try:
        import jax
        if any('tpu' in d.platform for d in jax.devices()):
            return 'tpu'
    except Exception:
        pass
    return 'cpu'

def train_loop(module_fn, cfg):
    device = get_device(cfg.get('prefer_device', None)) if isinstance(cfg, dict) else get_device()
    print(f"[harness] device -> {device}")
    return module_fn(cfg)
