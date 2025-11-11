import torch, torch.nn as nn
class EBSSC:
    def __init__(self, action_dim=16):
        self.logits = nn.Parameter(torch.randn(action_dim))

    def forward(self):
        return torch.softmax(self.logits, dim=0).detach().cpu().numpy()

    def optimize(self, steps=100, lr=1e-2):
        opt = torch.optim.Adam([self.logits], lr=lr)
        history = []
        for _ in range(steps):
            opt.zero_grad()
            probs = torch.softmax(self.logits, dim=0)
            entropy = - (probs * torch.log(probs+1e-12)).sum()
            loss = entropy
            loss.backward()
            opt.step()
            history.append(float(loss.item()))
        return history

def train(cfg=None):
    eb = EBSSC(action_dim=cfg.ebssc.get('action_dim',16) if cfg else 16)
    hist = eb.optimize(steps=cfg.simulation.steps if cfg else 100)
    return {'loss': hist}
