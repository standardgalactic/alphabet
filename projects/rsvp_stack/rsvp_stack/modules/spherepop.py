import numpy as np
def run(cfg=None):
    res = np.random.rand(1000) > 0.9
    return {'merge_rate': float(res.mean())}
def train(cfg=None):
    return run(cfg)
