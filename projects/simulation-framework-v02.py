# -------------------------------------------------------------
# RSVP Stack Simulation Framework (JAX + Flax)
# -------------------------------------------------------------
# Expert-level JAX implementation with:
#   • JIT compilation
#   • Automatic vectorization (vmap)
#   • Parallel ensemble runs (pmap)
#   • Spectral methods via FFT
#   • Gradient-weighted noise in TARTAN
#   • CLIO with Flax linen
#   • Full differentiability for inverse problems
#
# Dependencies: jax, flax, optax, numpy, matplotlib
# -------------------------------------------------------------

import jax
import jax.numpy as jnp
from jax import random, grad, jit, vmap, pmap, lax
from jax.lax import scan
import flax.linen as nn
import optax
import numpy as np
import matplotlib.pyplot as plt
from typing import Any, Tuple, Dict
from functools import partial

# -------------------------------------------------------------
# 1. RSVP Core PDE Solver (Spectral + IMEX)
# -------------------------------------------------------------
@partial(jit, static_argnums=(1,2,3,4,5,6))
def rsvp_step(
    carry: Tuple[jnp.ndarray, jnp.ndarray, jnp.ndarray, jnp.ndarray],
    t: float,
    kappa_phi: float, kappa_v: float, kappa_s: float,
    lambda_s: float, dt: float, sigma_coeff: float
) -> Tuple[Tuple[jnp.ndarray, ...], Dict]:
    phi, vx, vy, S = carry
    
    N = phi.shape[0]
    dx = 1.0 / N
    kx = 2 * jnp.pi * jnp.fft.fftfreq(N, d=dx)
    ky = kx.copy()
    KX, KY = jnp.meshgrid(kx, ky, indexing='ij')
    K2 = KX**2 + KY**2 + 1e-12
    
    # --- FFT-based diffusion factors ---
    diff_phi = jnp.exp(-kappa_phi * K2 * dt)
    diff_v = jnp.exp(-kappa_v * K2 * dt)
    diff_s = jnp.exp(-kappa_s * K2 * dt)
    
    # --- Advection (upwind, central fallback) ---
    def upwind(field, vel, axis):
        pos = lax.cond(vel > 0,
            lambda: (jnp.roll(field, -1, axis) - field) / dx,
            lambda: (field - jnp.roll(field, 1, axis)) / dx
        )
        return vel * pos
    
    adv_phi_x = vmap(partial(upwind, axis=0), in_axes=(None, 0))(phi, vx)
    adv_phi_y = vmap(partial(upwind, axis=1), in_axes=(None, 1))(phi, vy)
    adv_phi = -(adv_phi_x + adv_phi_y)
    
    # --- Momentum: (v·∇)v + ∇φ ---
    grad_phi_x = (jnp.roll(phi, -1, 0) - jnp.roll(phi, 1, 0)) / (2 * dx)
    grad_phi_y = (jnp.roll(phi, -1, 1) - jnp.roll(phi, 1, 1)) / (2 * dx)
    
    adv_vx = vx * (jnp.roll(vx, -1, 0) - jnp.roll(vx, 1, 0)) / (2 * dx) + \
             vy * (jnp.roll(vx, -1, 1) - jnp.roll(vx, 1, 1)) / (2 * dx)
    adv_vy = vx * (jnp.roll(vy, -1, 0) - jnp.roll(vy, 1, 0)) / (2 * dx) + \
             vy * (jnp.roll(vy, -1, 1) - jnp.roll(vy, 1, 1)) / (2 * dx)
    
    dvx = -adv_vx - grad_phi_x
    dvy = -adv_vy - grad_phi_y
    
    # --- Entropy production ---
    grad_phi_dot_v = grad_phi_x * vx + grad_phi_y * vy
    sigma = sigma_coeff * jnp.abs(grad_phi_dot_v)
    
    # --- Spectral update ---
    def spectral_update(field, rhs, diff):
        field_hat = jnp.fft.fft2(field + dt * rhs)
        return jnp.real(jnp.fft.ifft2(field_hat * diff))
    
    phi_new = spectral_update(phi, adv_phi, diff_phi)
    vx_new = spectral_update(vx, dvx, diff_v)
    vy_new = spectral_update(vy, dvy, diff_v)
    S_new = spectral_update(S, sigma - lambda_s * S, diff_s)
    S_new = jnp.clip(S_new, 0.0)
    
    # Enforce global entropy budget
    total_S = S_new.sum()
    S_new = lax.cond(total_S > 100.0, lambda: S_new * 100.0 / total_S, lambda: S_new)
    
    # Observables
    curl_v = (jnp.roll(vy_new, -1, 0) - jnp.roll(vy_new, 1, 0)) / (2 * dx) - \
             (jnp.roll(vx_new, -1, 1) - jnp.roll(vx_new, 1, 1)) / (2 * dx)
    coherence = (phi_new * jnp.abs(curl_v)).sum()
    
    dS_mean = (S_new.mean() - S.mean()) / dt
    redshift = jnp.exp(0.1 * dS_mean * t) - 1
    
    # Approximate mutual info via correlation
    phi_flat = phi_new.flatten()
    v_mag = jnp.sqrt(vx_new**2 + vy_new**2).flatten()
    corr = jnp.corrcoef(jnp.stack([phi_flat, v_mag]))[0,1]
    I_approx = 0.5 * jnp.log1p(corr**2)
    H_S = -(S_new * jnp.log(S_new + 1e-8)).sum() / (N*N)
    gamma = I_approx / (H_S + 1e-8)
    
    observables = {
        'coherence': coherence,
        'redshift': redshift,
        'entropy': S_new.mean(),
        'agency': gamma
    }
    
    return (phi_new, vx_new, vy_new, S_new), observables

# -------------------------------------------------------------
# 2. EBSSC: Sparse Policy Optimization (Flax)
# -------------------------------------------------------------
class EBSSC(nn.Module):
    action_dim: int = 16
    entropy_weight: float = 1.0
    sparsity_weight: float = 0.1
    
    @nn.compact
    def __call__(self, x):
        logits = nn.Dense(self.action_dim)(x)
        return logits
    
    def loss_fn(self, params, x):
        logits = self.apply(params, x)
        probs = jax.nn.softmax(logits)
        entropy = -(probs * jax.nn.log_softmax(logits)).sum()
        sparsity = (probs > 0.01).sum()
        divergence = 0.0  # Placeholder
        return self.entropy_weight * entropy + self.sparsity_weight * sparsity + divergence

# -------------------------------------------------------------
# 3. Spherepop Monte Carlo (Vectorized)
# -------------------------------------------------------------
spherepop_vmap = vmap(
    lambda key: spherepop_monte_carlo_single(key, theta_closure=1.2, p_max=100.0),
    in_axes=(0,)
)

def spherepop_monte_carlo_single(key, theta_closure, p_max):
    key1, key2, key3 = random.split(key, 3)
    sigma1 = random.uniform(key1, (1,)) * 1.0
    sigma2 = random.uniform(key2, (1,)) * 1.0
    R = random.exponential(key3, (1,)) * 50.0
    merge = (sigma1 + sigma2 > theta_closure) and (R < p_max)
    return {
        'merge': merge[0],
        'permeability': (sigma1 + sigma2)[0],
        'resistance': R[0]
    }

# -------------------------------------------------------------
# 4. TARTAN: Gradient-Weighted Noise Refinement
# -------------------------------------------------------------
def tartan_refine(tile: jnp.ndarray, noise_scale: float = 0.1) -> jnp.ndarray:
    # Upsample
    fine = jax.image.resize(tile, (tile.shape[0]*2, tile.shape[1]*2), method='bilinear')
    
    # Gradient magnitude
    grad_x = jnp.abs(fine[1:, :] - fine[:-1, :])
    grad_y = jnp.abs(fine[:, 1:] - fine[:, :-1])
    grad = jnp.pad(grad_x[:, :-1] + grad_y[:-1, :], ((1,0),(1,0)))
    
    # Gradient-weighted noise
    noise = noise_scale * grad * random.normal(random.PRNGKey(0), fine.shape)
    return jnp.clip(fine + noise, -2.0, 2.0)

tartan_refine_vmap = vmap(tartan_refine, in_axes=(0,))

# -------------------------------------------------------------
# 5. CLIO: Neural Cognitive Descent (Flax)
# -------------------------------------------------------------
class CLIO(nn.Module):
    latent_dim: int = 32
    
    @nn.compact
    def __call__(self, x):
        z = nn.Dense(512)(x)
        z = nn.relu(z)
        z = nn.Dense(self.latent_dim)(z)
        
        phi_logits = nn.Dense(64*64)(z)
        v_flat = nn.Dense(2*64*64)(z)
        
        phi = jax.nn.sigmoid(phi_logits).reshape(-1, 64, 64)
        vx = v_flat[:, :64*64].reshape(-1, 64, 64)
        vy = v_flat[:, 64*64:].reshape(-1, 64, 64)
        return phi, vx, vy

    def loss(self, params, x, S_target):
        phi, vx, vy = self.apply(params, x)
        S = -(phi * jnp.log(phi + 1e-8) + (1-phi) * jnp.log(1-phi + 1e-8)).mean()
        sparsity = (phi > 0.1).float().mean()
        flow = jnp.sqrt(vx**2 + vy**2).mean()
        return S + 0.1 * sparsity - 0.05 * flow

# -------------------------------------------------------------
# 6. Full Expert Simulation (JIT + vmap + pmap)
# -------------------------------------------------------------
@jit
def run_rsvp_ensemble(keys, params):
    def body(carry, t):
        return rsvp_step(carry, t, *params), None
    init = (
        random.normal(keys[0], (64,64)),
        jnp.zeros((64,64)),
        jnp.zeros((64,64)),
        jnp.ones((64,64)) * 0.1
    )
    (phi_f, vx_f, vy_f, S_f), _ = scan(body, init, jnp.arange(0, 1.0, 0.001))
    return phi_f, S_f

# Parallel across devices
run_rsvp_pmap = pmap(run_rsvp_ensemble, in_axes=(0, None))

# -------------------------------------------------------------
# 7. Demo
# -------------------------------------------------------------
if __name__ == "__main__":
    print("=== JAX RSVP Stack (Expert Mode) ===")
    
    # 1. RSVP Ensemble
    keys = random.split(random.PRNGKey(0), 8)
    params = (0.01, 0.01, 0.01, 0.1, 0.001, 0.1)
    phi_ensemble, S_ensemble = run_rsvp_pmap(keys, params)
    print(f"Ensemble coherence: {jnp.mean((phi_ensemble * jnp.abs(jnp.gradient(S_ensemble))).sum(axis=(1,2))):.3f}")
    
    # 2. EBSSC
    model = EBSSC()
    variables = model.init(random.PRNGKey(1), jnp.zeros((1, 10)))
    tx = optax.adam(1e-2)
    state = tx.init(variables)
    
    @jit
    def ebssc_step(variables, state):
        loss, grads = jax.value_and_grad(model.loss_fn)(variables, jnp.zeros((1,10)))
        updates, state = tx.update(grads, state)
        variables = optax.apply_updates(variables, updates)
        return variables, state, loss
    
    for _ in range(100):
        variables, state, loss = ebssc_step(variables, state)
    print(f"EBSSC loss: {loss:.4f}")
    
    # 3. Spherepop
    keys = random.split(random.PRNGKey(2), 10000)
    results = spherepop_vmap(keys)
    merge_rate = jnp.mean(jnp.array([r['merge'] for r in results]))
    print(f"Spherepop merge rate: {merge_rate:.3f}")
    
    # 4. TARTAN
    tile = random.normal(random.PRNGKey(3), (8,8))
    fine_tiles = tartan_refine_vmap(jnp.stack([tile]*4))
    print(f"TARTAN refinement complete: {fine_tiles.shape}")
    
    # 5. CLIO
    clio = CLIO()
    variables = clio.init(random.PRNGKey(4), jnp.randn(1, 64*64))
    tx = optax.adam(1e-3)
    state = tx.init(variables)
    
    @jit
    def clio_step(variables, state, x):
        loss = clio.loss(variables, x, None)
        grads = grad(loss)(variables)
        updates, state = tx.update(grads, state)
        variables = optax.apply_updates(variables, updates)
        return variables, state, loss
    
    x = jnp.randn(1, 64*64)
    for _ in range(100):
        variables, state, loss = clio_step(variables, state, x)
    print(f"CLIO loss: {loss:.4f}")
    
    print("\n=== JAX RSVP Stack Simulation Complete ===")
