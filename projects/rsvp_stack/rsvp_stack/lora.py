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
