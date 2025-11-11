import math, torch
class RSVPSolver:
    def __init__(self, grid_size=64, dt=0.002, device=None):
        self.N = grid_size
        self.dt = dt
        self.device = device or (torch.device('cuda') if torch.cuda.is_available() else torch.device('cpu'))
        x = torch.linspace(0,1,self.N, device=self.device)
        self.X, self.Y = torch.meshgrid(x, x, indexing='ij')
        self.phi = torch.exp(-((self.X-0.5)**2+(self.Y-0.5)**2)/(2*(0.125)**2)).to(self.device)
        self.vx = torch.zeros_like(self.phi)
        self.vy = torch.zeros_like(self.phi)
        self.S = torch.ones_like(self.phi) * 0.1
        self.history = {'coherence': [], 'redshift': [], 'entropy': [], 'agency': []}

    def step(self):
        adv = - (self.vx * (self.phi - torch.roll(self.phi,1,0)) + self.vy * (self.phi - torch.roll(self.phi,1,1)))
        self.phi = torch.clamp(self.phi + self.dt * adv, 0.0, 1e9)
        self.phi = (self.phi + torch.roll(self.phi,1,0) + torch.roll(self.phi,1,1)) / 3.0
        self.S = torch.clamp(self.S + 0.01*(torch.abs(self.vx)+torch.abs(self.vy)), 0.0, 10.0)

    def compute_observables(self):
        curl = (torch.roll(self.vy,-1,0)-torch.roll(self.vy,1,0)) - (torch.roll(self.vx,-1,1)-torch.roll(self.vx,1,1))
        coherence = float((self.phi * torch.abs(curl)).sum().item())
        self.history['coherence'].append(coherence)
        return self.history

def train(cfg=None):
    solver = RSVPSolver(grid_size=cfg.simulation.grid_size if cfg else 64, dt=cfg.rsvp.dt if cfg else 0.002)
    steps = cfg.simulation.steps if cfg else 100
    for i in range(steps):
        solver.step()
        if i % 10 == 0:
            solver.compute_observables()
    return solver.history
