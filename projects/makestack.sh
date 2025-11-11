#!/usr/bin/env bash
set -e
ROOT="./rsvp_stack"
rm -rf "$ROOT"
mkdir -p "$ROOT"

write() {
  local path="$ROOT/$1"
  mkdir -p "$(dirname "$path")"
  cat > "$path"
}

# pyproject.toml
cat > "$ROOT/pyproject.toml" <<'PYPROJECT'
[build-system]
requires = ["setuptools>=64", "wheel"]
build-backend = "setuptools.build_meta"

[project]
name = "rsvp-stack"
version = "0.1.0"
description = "Modular RSVP cosmology + agency simulation stack with Hydra"
authors = [{name = "Flyxion Research"}]
license = {text = "MIT"}
readme = "README.md"
requires-python = ">=3.9"

dependencies = [
  "hydra-core",
  "omegaconf",
  "torch",
  "jax[cpu] ; platform_system!='Windows'",
  "flax",
  "optax",
  "numpy",
  "matplotlib",
  "tqdm",
  "wandb",
  "gradio",
  "streamlit"
]

[project.scripts]
rsvp-run = "rsvp_stack.main:main"
rsvp-train = "rsvp_stack.train:train"
PYPROJECT

# README.md
cat > "$ROOT/README.md" <<'README'
# RSVP Stack (Full)

A modular, plugin-driven research framework for RSVP cosmology + agency.
README

# package layout and core python files
mkdir -p "$ROOT/rsvp_stack"
cat > "$ROOT/rsvp_stack/__init__.py" <<'INIT'
__version__ = "0.1.0"
INIT

# plugins.py
cat > "$ROOT/rsvp_stack/plugins.py" <<'PLUGINS'
import importlib, pkgutil
from typing import Dict, Any
PLUGIN_REGISTRY: Dict[str, Dict[str, Any]] = {}

def load_plugins(package="rsvp_stack.modules"):
    pkg = importlib.import_module(package)
    for _, name, _ in pkgutil.iter_modules(pkg.__path__):
        try:
            mod = importlib.import_module(f"{package}.{name}")
            PLUGIN_REGISTRY[name.lower()] = {"module": mod}
            print(f"[plugin] loaded: {name}")
        except Exception as e:
            print(f"[plugin] failed: {name} -> {e}")
    return PLUGIN_REGISTRY

def list_plugins():
    return list(PLUGIN_REGISTRY.keys())
PLUGINS

# stack.py
cat > "$ROOT/rsvp_stack/stack.py" <<'STACK'
from rsvp_stack.plugins import load_plugins, PLUGIN_REGISTRY, list_plugins
load_plugins()

class RSVPStack:
    def __init__(self, cfg):
        self.cfg = cfg
        self.modules = {}
        backend = cfg.backend

        def grab(name): return PLUGIN_REGISTRY.get(name)
        def grab_backend(base): return PLUGIN_REGISTRY.get(f"{base}_{backend}")

        if cfg.rsvp.enabled: self.modules["rsvp"] = grab_backend("rsvp")
        if cfg.ebssc.enabled: self.modules["ebssc"] = grab_backend("ebssc")
        if cfg.spherepop.enabled: self.modules["spherepop"] = grab("spherepop")
        if cfg.tartan.enabled: self.modules["tartan"] = grab_backend("tartan")
        if cfg.clio.enabled: self.modules["clio"] = grab_backend("clio")

    def run(self):
        print("Detected plugins:", list_plugins())
        results = {}
        for k, plug in self.modules.items():
            if not plug:
                print(f"[skip] {k}")
                continue
            mod = plug["module"]
            print(f"[run] {k}")
            if hasattr(mod, "train"):
                results[k] = mod.train(self.cfg)
            elif hasattr(mod, "run"):
                results[k] = mod.run(self.cfg)
            else:
                results[k] = "loaded"
        return results
STACK

# main.py
cat > "$ROOT/rsvp_stack/main.py" <<'MAIN'
import hydra
from omegaconf import DictConfig
from rsvp_stack.stack import RSVPStack

@hydra.main(version_base=None, config_path="configs", config_name="config")
def main(cfg: DictConfig):
    print(cfg.pretty())
    stack = RSVPStack(cfg)
    results = stack.run()
    print("Completed modules:", list(results.keys()))

if __name__ == "__main__":
    main()
MAIN

# train.py
cat > "$ROOT/rsvp_stack/train.py" <<'TRAIN'
import hydra, wandb
from omegaconf import DictConfig
from rsvp_stack.stack import RSVPStack

@hydra.main(version_base=None, config_path="configs", config_name="config")
def train(cfg: DictConfig):
    wandb.init(project="RSVP-Stack", config=cfg, reinit=True)
    stack = RSVPStack(cfg)
    results = stack.run()
    if 'rsvp' in results and isinstance(results['rsvp'], dict):
        wandb.log({'rsvp_coherence_len': len(results['rsvp'].get('coherence', []))})
    wandb.finish()

if __name__ == "__main__":
    train()
TRAIN

# configs
mkdir -p "$ROOT/rsvp_stack/configs/modules"
mkdir -p "$ROOT/rsvp_stack/configs/presets"
cat > "$ROOT/rsvp_stack/configs/config.yaml" <<'CFG'
defaults:
  - _self_
  - modules/rsvp
  - modules/ebssc
  - modules/spherepop
  - modules/tartan
  - modules/clio
  - presets: minimal

backend: "torch"

logging:
  log_every: 50
  plot_results: false

simulation:
  steps: 200
  grid_size: 64
CFG

cat > "$ROOT/rsvp_stack/configs/modules/rsvp.yaml" <<'RSPY'
rsvp:
  enabled: true
  dt: 0.002
RSPY

cat > "$ROOT/rsvp_stack/configs/modules/ebssc.yaml" <<'EBY'
ebssc:
  enabled: true
EBY

cat > "$ROOT/rsvp_stack/configs/modules/spherepop.yaml" <<'SPY'
spherepop:
  enabled: true
SPY

cat > "$ROOT/rsvp_stack/configs/modules/tartan.yaml" <<'TTY'
tartan:
  enabled: true
TTY

cat > "$ROOT/rsvp_stack/configs/modules/clio.yaml" <<'CLY'
clio:
  enabled: true
CLY

cat > "$ROOT/rsvp_stack/configs/presets/minimal.yaml" <<'MINP'
rsvp.enabled: false
ebssc.enabled: false
spherepop.enabled: false
tartan.enabled: false
clio.enabled: false
MINP

cat > "$ROOT/rsvp_stack/configs/presets/cosmology.yaml" <<'COS'
rsvp.enabled: true
tartan.enabled: true
ebssc.enabled: false
spherepop.enabled: false
clio.enabled: false
COS

cat > "$ROOT/rsvp_stack/configs/presets/agency.yaml" <<'AG'
rsvp.enabled: true
ebssc.enabled: true
spherepop.enabled: true
clio.enabled: true
tartan.enabled: false
AG

# modules (example implementations)
mkdir -p "$ROOT/rsvp_stack/modules"

# rsvp_torch.py
cat > "$ROOT/rsvp_stack/modules/rsvp_torch.py" <<'RT'
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
RT

# ebssc_torch.py
cat > "$ROOT/rsvp_stack/modules/ebssc_torch.py" <<'EBT'
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
EBT

# spherepop.py
cat > "$ROOT/rsvp_stack/modules/spherepop.py" <<'SP'
import numpy as np
def run(cfg=None):
    res = np.random.rand(1000) > 0.9
    return {'merge_rate': float(res.mean())}
def train(cfg=None):
    return run(cfg)
SP

# tartan_torch.py
cat > "$ROOT/rsvp_stack/modules/tartan_torch.py" <<'TT'
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
TT

# clio_torch.py
cat > "$ROOT/rsvp_stack/modules/clio_torch.py" <<'CLIO'
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
CLIO

# registry.py
cat > "$ROOT/rsvp_stack/registry.py" <<'REG'
import json, os
REG_PATH = os.path.expanduser('~/.rsvp_model_registry.json')
def _load():
    if os.path.exists(REG_PATH):
        return json.load(open(REG_PATH))
    return {}
def register(name, meta):
    r = _load()
    r[name] = meta
    json.dump(r, open(REG_PATH,'w'))
def list_models():
    return _load()
REG

# train_harness.py
cat > "$ROOT/rsvp_stack/train_harness.py" <<'HAR'
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
HAR

# benchmarks
cat > "$ROOT/rsvp_stack/benchmarks_run.py" <<'BCH'
from rsvp_stack.modules import rsvp_torch, ebssc_torch
def run():
    print('Running small benchmarks...')
    h = rsvp_torch.train(None)
    print('RSVP history keys:', list(h.keys()))
    e = ebssc_torch.train(None)
    print('EBSSC result keys:', list(e.keys()))
if __name__=='__main__':
    run()
BCH

# lora 
cat > "$ROOT/rsvp_stack/lora.py" <<'LORA'
# rsvp_stack/lora.py
"""
Lightweight, well-documented LoRA implementation (PyTorch).
- LoraLinear: wrapper for nn.Linear with trainable low-rank A/B adapters.
- apply_lora: walk a model and replace selected Linear modules with LoraLinear.
- merge_lora: fold adapters into original weights (for inference).
- unmerge_lora: undo merge, keep adapters separate.
- save_lora / load_lora: persist adapter state_dict only.
API intentionally mirrors PEFT-ish workflow (patch, train adapters, merge).
"""

from typing import Iterable, Tuple, Dict, Optional
import torch
import torch.nn as nn
import copy
import os

# -----------------------------------------------------------------------------
# Core module
# -----------------------------------------------------------------------------
class LoraLinear(nn.Module):
    """
    Low-rank adapter for a Linear layer.
    It keeps a copy of the original weight and adds low-rank update:
      W' = W + alpha / r * (B @ A)
    where A: (r, in_features), B: (out_features, r)
    """
    def __init__(self, orig: nn.Linear, r: int = 4, alpha: float = 16.0, bias: bool = True, dropout: float = 0.0):
        super().__init__()
        self.in_features = orig.in_features
        self.out_features = orig.out_features
        self.r = r
        self.alpha = alpha
        self.scaling = float(alpha) / float(r) if r > 0 else 1.0
        self.use_adapter = (r > 0)
        self.dropout = nn.Dropout(dropout) if dropout and dropout > 0.0 else nn.Identity()

        # keep original weight and bias (frozen by default)
        self.weight = nn.Parameter(orig.weight.data.clone(), requires_grad=False)
        if orig.bias is not None:
            self.bias = nn.Parameter(orig.bias.data.clone(), requires_grad=False)
        else:
            self.bias = None

        # LoRA adapters (trainable)
        if self.use_adapter:
            # A: projects from in_features -> r (we store as r x in)
            self.A = nn.Parameter(torch.randn(self.r, self.in_features) * (1.0 / self.r**0.5))
            # B: projects from r -> out_features (we store as out x r)
            self.B = nn.Parameter(torch.randn(self.out_features, self.r) * 0.01)
        else:
            # placeholders to avoid branching
            self.register_parameter("A", None)
            self.register_parameter("B", None)

        # Whether adapters have been merged into weight
        self.merged = False

    def forward(self, x: torch.Tensor) -> torch.Tensor:
        # x: (..., in_features) or (batch, in_features)
        base = torch.nn.functional.linear(x, self.weight, self.bias)
        if not self.use_adapter:
            return base

        if self.merged:
            # If merged, weight already contains adapter; no double-add
            return base

        # compute LoRA delta: x @ A^T -> (..., r); then @ B^T -> (..., out)
        # Equivalent: linear(x, B @ A) but we compute efficiently
        x_dropped = self.dropout(x)
        # x @ A^T
        mid = torch.matmul(x_dropped, self.A.t())  # (..., r)
        delta = torch.matmul(mid, self.B.t())      # (..., out)
        return base + self.scaling * delta

    def merge(self):
        """Fold adapter into self.weight for inference. Destructive to adapter trainability unless unmerge is used."""
        if not self.use_adapter or self.merged:
            return
        # compute W_delta = (B @ A) * scaling
        W_delta = (self.B @ self.A) * self.scaling  # (out, in)
        # mutate the stored frozen weight param
        with torch.no_grad():
            self.weight.data += W_delta
        self.merged = True

    def unmerge(self):
        """Undo merge: subtract adapter contribution from weight (if merged)."""
        if not self.use_adapter or not self.merged:
            return
        W_delta = (self.B @ self.A) * self.scaling
        with torch.no_grad():
            self.weight.data -= W_delta
        self.merged = False

    def adapter_state_dict(self) -> Dict[str, torch.Tensor]:
        """Return a state dict containing only adapter params (A,B and meta)."""
        if not self.use_adapter:
            return {}
        return {"A": self.A.detach().cpu(), "B": self.B.detach().cpu(), "r": self.r, "alpha": self.alpha}

    def load_adapter_state_dict(self, sd: Dict[str, torch.Tensor]):
        if not self.use_adapter:
            raise RuntimeError("Module was constructed without adapters.")
        self.A.data.copy_(sd["A"].to(self.A.device))
        self.B.data.copy_(sd["B"].to(self.B.device))
        # r and alpha are metadata — no need to override structure

# -----------------------------------------------------------------------------
# Utilities: walk and patch models
# -----------------------------------------------------------------------------
def _is_target_linear_module(name: str, module: nn.Module, target_names: Optional[Iterable[str]]):
    # target_names like ('q','v','k','o','proj','fc','linear')
    if not isinstance(module, nn.Linear):
        return False
    if not target_names:
        return True
    ln = name.lower()
    return any(t in ln for t in target_names)

def apply_lora(
    model: nn.Module,
    r: int = 4,
    alpha: float = 16.0,
    target_modules: Optional[Iterable[str]] = ("q", "k", "v", "o", "proj", "fc", "linear"),
    trainable_bias: bool = False,
    dropout: float = 0.0,
    verbose: bool = True
) -> Tuple[nn.Module, Dict[str, Tuple[str, int]]]:
    """
    Replace Linear modules in model with LoraLinear where the module name matches any substring in target_modules.
    Returns (patched_model, mapping) where mapping maps module path -> (orig_class_name, adapter_count).
    Example:
        model, mapping = apply_lora(model, r=8, alpha=32, target_modules=['q','v','proj'])
    """
    mapping = {}
    # recursive function that traverses attributes
    for module_name, module in list(model.named_modules()):
        # skip root module itself in replacement
        if module_name == "":
            continue
        parent = model
        # find parent container and attribute name
        *path, attr = module_name.split(".")
        for p in path:
            parent = getattr(parent, p)
        child = getattr(parent, attr)
        if _is_target_linear_module(module_name, child, target_modules):
            # create LoraLinear and replace in parent
            lora = LoraLinear(child, r=r, alpha=alpha, bias=(child.bias is not None and trainable_bias), dropout=dropout)
            # keep original parameters frozen (weight and bias in LoraLinear are frozen by default)
            setattr(parent, attr, lora)
            mapping[module_name] = (child.__class__.__name__, r)
            if verbose:
                print(f"[lora] patched {module_name} -> LoraLinear (r={r}, alpha={alpha})")
    return model, mapping

def list_lora_modules(model: nn.Module) -> Dict[str, LoraLinear]:
    return {name: m for name, m in model.named_modules() if isinstance(m, LoraLinear)}

def set_adapter_trainable(model: nn.Module, trainable: bool = True):
    """Toggle requires_grad for adapter params only (A and B)."""
    for name, mod in list_lora_modules(model).items():
        if not mod.use_adapter:
            continue
        mod.A.requires_grad = trainable
        mod.B.requires_grad = trainable

def adapter_parameters(model: nn.Module):
    """Yield adapter params (A and B) for optimizer."""
    for mod in list_lora_modules(model).values():
        if not mod.use_adapter:
            continue
        yield mod.A
        yield mod.B

# -----------------------------------------------------------------------------
# Merge/unmerge helpers and persistence
# -----------------------------------------------------------------------------
def merge_lora(model: nn.Module):
    """Merge all LoraLinear adapters into the base weights (for inference speed)."""
    for name, mod in list_lora_modules(model).items():
        mod.merge()

def unmerge_lora(model: nn.Module):
    """Undo merges to restore adapter separation."""
    for name, mod in list_lora_modules(model).items():
        mod.unmerge()

def save_adapter_state(model: nn.Module, path: str):
    """
    Save adapters (only) to disk as a dict: {module_name: adapter_state_dict}.
    This avoids saving whole model.
    """
    out = {}
    for name, mod in list_lora_modules(model).items():
        out[name] = mod.adapter_state_dict()
    os.makedirs(os.path.dirname(path), exist_ok=True)
    torch.save(out, path)

def load_adapter_state(model: nn.Module, path: str, strict: bool = True):
    """
    Load adapter state dict into the model's LoraLinear modules.
    """
    sd = torch.load(path, map_location='cpu')
    mods = list_lora_modules(model)
    for name, ad in sd.items():
        if name not in mods:
            if strict:
                raise KeyError(f"Adapter target {name} not found in model.")
            else:
                print(f"[lora] warning: {name} not found, skipping")
                continue
        mods[name].load_adapter_state_dict(ad)

# -----------------------------------------------------------------------------
# Convenience: quick-train loop example
# -----------------------------------------------------------------------------
def finetune_with_lora(
    model: nn.Module,
    dataloader,
    loss_fn,
    r: int = 4,
    alpha: float = 16.0,
    target_modules: Optional[Iterable[str]] = None,
    lr: float = 1e-3,
    epochs: int = 1,
    device: Optional[str] = None
):
    model, mapping = apply_lora(model, r=r, alpha=alpha, target_modules=target_modules)
    set_adapter_trainable(model, True)
    opt = torch.optim.Adam(adapter_parameters(model), lr=lr)
    device = device or ("cuda" if torch.cuda.is_available() else "cpu")
    model.to(device)
    model.train()
    for ep in range(epochs):
        for xb, yb in dataloader:
            xb = xb.to(device); yb = yb.to(device)
            opt.zero_grad()
            out = model(xb)
            loss = loss_fn(out, yb)
            loss.backward()
            opt.step()
    return model, mapping

# -----------------------------------------------------------------------------
# Small smoke-test unit (call from scripts/tests)
# -----------------------------------------------------------------------------
def _unit_test():
    # simple linear model
    class SmallModel(nn.Module):
        def __init__(self):
            super().__init__()
            self.fc1 = nn.Linear(16, 32)
            self.fc2 = nn.Linear(32, 8)
        def forward(self, x):
            x = torch.relu(self.fc1(x))
            return self.fc2(x)

    m = SmallModel()
    x = torch.randn(4, 16)
    y0 = m(x).detach()
    m, mapping = apply_lora(m, r=2, alpha=8.0, target_modules=('fc',))
    set_adapter_trainable(m, True)
    # confirm adapter params are present and require grad
    adapters = list_lora_modules(m)
    assert len(adapters) >= 1
    for nm, mod in adapters.items():
        assert mod.A.requires_grad and mod.B.requires_grad
    # forward passes produce same shape
    y1 = m(x)
    assert y1.shape == y0.shape
    # save/load adapters
    import tempfile
    p = tempfile.mktemp(suffix=".pt")
    save_adapter_state(m, p)
    # merge and unmerge
    merge_lora(m)
    unmerge_lora(m)
    # load adapters back
    load_adapter_state(m, p)
    print("LoRA unit test passed.")

if __name__ == "__main__":
    _unit_test()
LORA

# UI: gradio and streamlit
mkdir -p "$ROOT/rsvp_stack/ui"
cat > "$ROOT/rsvp_stack/ui/gradio_app.py" <<'GRADIO'
import gradio as gr
from rsvp_stack.plugins import load_plugins, PLUGIN_REGISTRY
load_plugins()
def list_plugins():
    return '\\n'.join(PLUGIN_REGISTRY.keys())
def run_plugin(name):
    p = PLUGIN_REGISTRY.get(name)
    if not p: return f'plugin {name} not found'
    mod = p['module']
    if hasattr(mod,'run'):
        return str(mod.run(None))
    return 'no run()'
with gr.Blocks() as demo:
    gr.Markdown('# RSVP Stack Plugins')
    pl = gr.Textbox(value=list_plugins(), label='discovered plugins')
    inp = gr.Textbox(label='plugin name')
    btn = gr.Button('Run')
    out = gr.Textbox(label='output')
    btn.click(lambda n: run_plugin(n), inputs=inp, outputs=out)
if __name__=='__main__':
    demo.launch()
GRADIO

cat > "$ROOT/rsvp_stack/ui/streamlit_app.py" <<'STREAM'
import streamlit as st
from rsvp_stack.plugins import load_plugins, list_plugins, PLUGIN_REGISTRY
load_plugins()
st.title('RSVP Stack')
st.write('Detected plugins:', list_plugins())
sel = st.selectbox('plugin', list_plugins())
if st.button('run'):
    mod = PLUGIN_REGISTRY[sel]['module']
    if hasattr(mod,'run'):
        st.write(mod.run(None))
    else:
        st.write('no run()')
STREAM

# Dockerfiles
cat > "$ROOT/Dockerfile" <<'DOCK'
FROM nvidia/cuda:12.2.0-runtime-ubuntu22.04
RUN apt update && apt install -y python3 python3-pip git
WORKDIR /app
COPY . /app
RUN pip3 install --upgrade pip
RUN pip3 install -e .
RUN pip3 install torch torchvision --index-url https://download.pytorch.org/whl/cu121
RUN pip3 install wandb gradio streamlit
CMD ["rsvp-run"]
DOCK

cat > "$ROOT/Dockerfile.tpu" <<'DOCKTPU'
FROM python:3.10-slim
WORKDIR /app
COPY . /app
RUN pip install -e .
RUN pip install jax flax optax
CMD ["rsvp-train"]
DOCKTPU

# zip it
zip -r rsvp_stack_full.zip rsvp_stack pyproject.toml README.md Dockerfile Dockerfile.tpu
echo "Created rsvp_stack_full.zip in $(pwd)"
