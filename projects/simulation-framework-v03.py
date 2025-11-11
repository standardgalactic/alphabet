# -------------------------------------------------------------
# RSVP Stack: TPU-Scale 3D Cosmological Simulation (JAX)
# -------------------------------------------------------------
# Features:
#   • 256³ grid on TPU v4 (8 cores)
#   • pmap across 8 TPU cores
#   • 3D FFT via jax.fft
#   • Spectral diffusion + IMEX advection
#   • Entropic redshift from full volume
#   • Memory-efficient sharding
#   • Real-time coherence & agency
#
# Run on Google Cloud TPU v4-8:
#   `python rsvp_tpu.py --tpu=local`
# -------------------------------------------------------------

import jax
import jax.numpy as jnp
from jax import random, jit, pmap, lax, vmap
from jax.experimental import mesh_utils
from jax.sharding import Mesh, PartitionSpec as P, NamedSharding
from jax.lax import with_sharding_constraint
import optax
import numpy as np
import matplotlib.pyplot as plt
from typing import Tuple, Dict
import argparse
import time

# -------------------------------------------------------------
# TPU Configuration
# -------------------------------------------------------------
parser = argparse.ArgumentParser()
parser.add_argument('--grid', type=int, default=256, help='Grid size (256 for TPU v4)')
parser.add_argument('--tpu', type=str, default='local', help='TPU name')
args = parser.parse_args()

N = args.grid  # 256³ = 16M points per field
devices = jax.devices("tpu")
n_devices = len(devices)
print(f"TPU devices: {n_devices} x {jax.devices()[0].platform.upper()}")

# Create mesh and sharding
mesh = mesh_utils.create_device_mesh((n_devices, 1))
sharding = NamedSharding(mesh, P('data', None))

# Global constants
L = 1.0
dx = L / N
dt = 1e-4
T_total = 0.1
steps = int(T_total / dt)
kappa_phi = 1e-3
kappa_v = 1e-3
kappa_s = 1e-3
lambda_s = 0.1
sigma_coeff = 0.1
alpha_S = 0.1

# -------------------------------------------------------------
# 3D Spectral Operators (Sharded)
# -------------------------------------------------------------
def create_spectral_diffusion(kappa, dt):
    kx = 2 * jnp.pi * jnp.fft.fftfreq(N, d=dx)
    ky = kx.copy()
    kz = kx.copy()
    KX, KY, KZ = jnp.meshgrid(kx, ky, kz, indexing='ij')
    K2 = KX**2 + KY**2 + KZ**2 + 1e-12
    return jnp.exp(-kappa * K2 * dt)

diff_phi = create_spectral_diffusion(kappa_phi, dt)
diff_v = create_spectral_diffusion(kappa_v, dt)
diff_s = create_spectral_diffusion(kappa_s, dt)

# Shard diffusion factors
diff_phi = with_sharding_constraint(diff_phi, sharding)
diff_v = with_sharding_constraint(diff_v, sharding)
diff_s = with_sharding_constraint(diff_s, sharding)

# -------------------------------------------------------------
# Initialize Fields (Sharded)
# -------------------------------------------------------------
def init_fields(key):
    subkeys = random.split(key, 4)
    # Gaussian blob at center
    center = N // 2
    sigma = N // 8
    X, Y, Z = jnp.mgrid[0:N, 0:N, 0:N]
    r2 = (X - center)**2 + (Y - center)**2 + (Z - center)**2
    phi = jnp.exp(-r2 / (2 * sigma**2))
    phi = phi / phi.sum() * 1e6  # Total mass ~1e6
    
    vx = random.normal(subkeys[1], (N,N,N)) * 0.01
    vy = random.normal(subkeys[2], (N,N,N)) * 0.01
    vz = random.normal(subkeys[3], (N,N,N)) * 0.01
    S = jnp.ones((N,N,N)) * 0.1
    
    return phi, vx, vy, vz, S

# Replicate across devices
init_key = random.PRNGKey(0)
phi_local, vx_local, vy_local, vz_local, S_local = init_fields(init_key)

# Shard fields
phi = jax.device_put(phi_local, sharding)
vx = jax.device_put(vx_local, sharding)
vy = jax.device_put(vy_local, sharding)
vz = jax.device_put(vz_local, sharding)
S = jax.device_put(S_local, sharding)

# -------------------------------------------------------------
# 3D Advection (Upwind)
# -------------------------------------------------------------
def upwind_3d(field, vel, axis):
    pos = lax.cond(vel > 0,
        lambda f, v, a: (jnp.roll(f, -1, a) - f) / dx,
        lambda f, v, a: (f - jnp.roll(f, 1, a)) / dx,
        field, vel, axis
    )
    return vel * pos

upwind_x = partial(upwind_3d, axis=0)
upwind_y = partial(upwind_3d, axis=1)
upwind_z = partial(upwind_3d, axis=2)

# Vectorized over velocity components
adv_phi_x = vmap(upwind_x, in_axes=(None, 0))(phi, vx)
adv_phi_y = vmap(upwind_y, in_axes=(None, 1))(phi, vy)
adv_phi_z = vmap(upwind_z, in_axes=(None, 2))(phi, vz)
adv_phi = -(adv_phi_x + adv_phi_y + adv_phi_z)

# -------------------------------------------------------------
# 3D Momentum Update
# -------------------------------------------------------------
def grad_central(field, axis):
    return (jnp.roll(field, -1, axis) - jnp.roll(field, 1, axis)) / (2 * dx)

grad_phi_x = grad_central(phi, 0)
grad_phi_y = grad_central(phi, 1)
grad_phi_z = grad_central(phi, 2)

# (v·∇)v terms
def advect_velocity(v_comp, vx, vy, vz, axis):
    grad_x = grad_central(v_comp, 0)
    grad_y = grad_central(v_comp, 1)
    grad_z = grad_central(v_comp, 2)
    return vx * grad_x + vy * grad_y + vz * grad_z

adv_vx = advect_velocity(vx, vx, vy, vz, 0)
adv_vy = advect_velocity(vy, vx, vy, vz, 1)
adv_vz = advect_velocity(vz, vx, vy, vz, 2)

dvx = -adv_vx - grad_phi_x
dvy = -adv_vy - grad_phi_y
dvz = -adv_vz - grad_phi_z

# -------------------------------------------------------------
# Entropy Production
# -------------------------------------------------------------
sigma = sigma_coeff * jnp.abs(grad_phi_x * vx + grad_phi_y * vy + grad_phi_z * vz)

# -------------------------------------------------------------
# Spectral Update (3D FFT)
# -------------------------------------------------------------
def spectral_step(field, rhs, diff):
    field_hat = jnp.fft.fftn(field + dt * rhs)
    return jnp.real(jnp.fft.ifftn(field_hat * diff))

phi_new = spectral_step(phi, adv_phi, diff_phi)
vx_new = spectral_step(vx, dvx, diff_v)
vy_new = spectral_step(vy, dvy, diff_v)
vz_new = spectral_step(vz, dvz, diff_v)
S_new = spectral_step(S, sigma - lambda_s * S, diff_s)
S_new = jnp.clip(S_new, 0.0)

# Enforce entropy budget
total_S = S_new.sum()
S_new = lax.cond(total_S > 1e7, lambda: S_new * 1e7 / total_S, lambda: S_new)

# -------------------------------------------------------------
# Observables (Global Reduce)
# -------------------------------------------------------------
curl_x = grad_central(vz, 1) - grad_central(vy, 2)
curl_y = grad_central(vx, 2) - grad_central(vz, 0)
curl_z = grad_central(vy, 0) - grad_central(vx, 1)
curl_mag = jnp.sqrt(curl_x**2 + curl_y**2 + curl_z**2)

coherence = (phi_new * curl_mag).sum()
dS_mean = (S_new.mean() - S.mean()) / dt
redshift = jnp.exp(alpha_S * dS_mean * (steps * dt)) - 1

# Agency coherence (approximate)
phi_flat = phi_new.flatten()
v_mag = jnp.sqrt(vx_new**2 + vy_new**2 + vz_new**2).flatten()
corr = jnp.corrcoef(jnp.stack([phi_flat, v_mag]))[0,1]
I_approx = 0.5 * jnp.log1p(corr**2)
H_S = -(S_new * jnp.log(S_new + 1e-8)).sum() / (N**3)
gamma = I_approx / (H_S + 1e-8)

# -------------------------------------------------------------
# Full Simulation Loop (JIT + pmap)
# -------------------------------------------------------------
@jit
def rsvp_step_3d(state):
    phi, vx, vy, vz, S = state
    # [All computation above]
    # ... (insert full update logic with sharding constraints)
    return (phi_new, vx_new, vy_new, vz_new, S_new), {
        'coherence': coherence,
        'redshift': redshift,
        'agency': gamma
    }

# pmap across TPU cores
rsvp_step_pmap = pmap(rsvp_step_3d, in_axes=(0,))

# Replicate initial state
state = (phi, vx, vy, vz, S)
state = jax.tree_map(lambda x: jnp.stack([x]*n_devices), state)

# Run
print(f"Running {steps} steps on {n_devices} TPUs...")
start = time.time()
for step in range(steps):
    state, obs = rsvp_step_pmap(state)
    if step % 1000 == 0:
        obs_global = jax.tree_map(lambda x: x.mean(), obs)
        print(f"Step {step}: C={obs_global['coherence']:.2e}, z={obs_global['redshift']:.3f}, Γ={obs_global['agency']:.3f}")
print(f"Simulation complete in {time.time() - start:.1f}s")

# -------------------------------------------------------------
# Post-processing (Gather to host)
# -------------------------------------------------------------
phi_final = state[0][0].block_until_ready()  # First shard
S_final = state[4][0].block_until_ready()

# Save or visualize
np.savez("rsvp_tpu_output.npz", phi=phi_final, S=S_final)
print("3D fields saved to rsvp_tpu_output.npz")

# Plot central slice
plt.figure(figsize=(12,5))
plt.subplot(1,2,1)
plt.imshow(phi_final[N//2], cmap='plasma')
plt.title('Φ (central slice)')
plt.subplot(1,2,2)
plt.imshow(S_final[N//2], cmap='hot')
plt.title('Entropy S')
plt.show()
