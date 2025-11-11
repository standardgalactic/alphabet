import torch, torch.nn.functional as F
class TARTAN:
    def __init__(self,tile_size=8,levels=3):
        self.tile_size=tile_size; self.levels=levels
        self.tiles={l: torch.randn(2**l,2**l,tile_size,tile_size) for l in range(levels)}
    def refine(self):
        for l in range(self.levels-1):
            t=self.tiles[l]
            up=F.interpolate(t.reshape(-1,1,self.tile_size,self.tile_size), scale_factor=2).reshape(*t.shape[:-2], self.tile_size*2, self.tile_size*2)
            self.tiles[l+1]=up + 0.01*torch.randn_like(up)
        return True
def run(cfg=None):
    t=TARTAN(); t.refine(); return {'refined': True}
