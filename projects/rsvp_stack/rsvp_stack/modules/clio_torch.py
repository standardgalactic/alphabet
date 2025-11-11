import torch, torch.nn as nn
class CLIO(nn.Module):
    def __init__(self, latent_dim=32):
        super().__init__()
        self.net = nn.Sequential(nn.Linear(64*64,512), nn.ReLU(), nn.Linear(512,latent_dim))
    def forward(self,x):
        return self.net(x)

def train(cfg=None):
    model = CLIO()
    opt = torch.optim.Adam(model.parameters(), lr=1e-3)
    x = torch.randn(8,64*64)
    for _ in range(10):
        opt.zero_grad()
        out = model(x)
        loss = out.norm()
        loss.backward()
        opt.step()
    return {'final_loss': float(loss.item())}
