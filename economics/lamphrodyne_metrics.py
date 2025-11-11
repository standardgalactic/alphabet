# Toy simulation of Lamphrodyne Network (discrete-time, Python)
# - N nodes, discrete timesteps
# - Fields: v (vector agency), Phi (scalar potential), S (entropy)
# - Adjacency A (symmetric), reciprocity R tracked
# - Local-first amplification, diffusion of Phi and S, caps on amplification
# - Outputs: phi concentration index, agency retention, reciprocity growth, entropy gradient over time
#
# Run: this cell executes a simulation and plots key metrics.
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd

np.random.seed(1)

# Parameters
N = 400  # number of nodes
T = 250  # timesteps
p_edge = 0.02  # initial edge probability
gamma_v = 0.08   # natural decay of agency
amp_cap = 0.12   # cap on per-step amplification from neighbors
kappa = 0.05     # Phi diffusion toward mean
beta_C = 0.02    # cooperative contribution amplitude
mu_E = 0.2       # penalize extraction (higher -> less extraction allowed)
D_S = 0.1        # entropy diffusion coeff
lambda_v = 0.03  # agency reduces local entropy
noise_eta = 0.03 # creative injection rate (probability of injection)
credit_decay = 0.001  # minimal credit decay rate (not used as token here)

# Initialization
A = (np.random.rand(N, N) < p_edge).astype(float)
A = np.triu(A, 1)
A = A + A.T  # symmetric adjacency
# normalize adjacency rows (so flows are bounded)
row_sums = A.sum(axis=1, keepdims=True)
row_sums[row_sums == 0] = 1.0
A = A / row_sums

v = np.random.rand(N) * 0.02  # small initial agency
Phi = np.ones(N) * 1.0        # uniform starting scalar potential
S = np.random.rand(N) * 0.5 + 0.5  # moderate initial entropy

# Reciprocity / interaction history: R_xy tracks mutual interactions strength
R = np.zeros((N, N))
interactions = np.zeros((N, N))  # per-step interactions (for updating R)

# Metrics storage
phi_conc = np.zeros(T)
agency_ret = np.zeros(T)
reciprocity_med = np.zeros(T)
entropy_grad = np.zeros(T)

# Helper functions
def phi_concentration_index(Phi):
    top = int(max(1, np.ceil(0.01 * len(Phi))))  # top 1%
    sorted_idx = np.argsort(Phi)[::-1]
    top_sum = Phi[sorted_idx[:top]].sum()
    return top_sum / Phi.sum()

def agency_retention(v, eps=0.02):
    return np.sum(v > eps) / len(v)

def entropy_gradient_metric(S, A):
    # approximate gradient as sum over edges |S_i - S_j| * A_ij normalized
    diffs = np.abs(S[:, None] - S[None, :]) * A
    return diffs.sum() / A.sum()

# Simulation loop
for t in range(T):
    # 1) Random creative injections: some nodes produce content -> bump v
    creators = np.random.rand(N) < noise_eta
    v += creators.astype(float) * (0.02 + 0.03 * np.random.rand(N))
    
    # 2) Neighbor amplification (local-first): each node gains from neighbors weighted by reciprocity
    # Compute neighbor signal = sum_y A_xy * v_y * f(R_xy)
    # Use f(R) = 1 + tanh(R_mean) to favor reciprocal edges modestly
    R_mean = R.mean(axis=1) + 1e-9
    fR = 1.0 + np.tanh(R_mean)
    neighbor_signal = (A * v[None, :]).sum(axis=1) * fR
    # Cap amplification per node
    neighbor_signal = np.minimum(neighbor_signal, amp_cap)
    v = v * (1 - gamma_v) + neighbor_signal
    
    # 3) Update interactions based on recent neighbor_signal (simulate replies, saves)
    # We'll use a stochastic mapping where higher neighbor_signal encourages two-way interactions
    prob_interact = np.clip((neighbor_signal / (amp_cap + 1e-9)) * 0.2, 0, 0.9)
    interactions = (np.random.rand(N, N) < prob_interact[:, None]).astype(float)
    # make interactions symmetric probabilistically to simulate reciprocity appearance
    interactions = np.triu(interactions, 1)
    interactions = interactions + interactions.T
    # update R as running exponential average
    R = 0.97 * R + 0.03 * interactions
    
    # 4) Phi diffusion toward mean and cooperative contribution minus extraction penalty
    Phi_mean = Phi.mean()
    cooperative = beta_C * (v / (v.mean() + 1e-9))  # normalized cooperative contribution
    extraction = mu_E * np.random.rand(N) * 0.002  # small stochastic extraction attempts
    # penalize extraction more strongly when node has low reciprocity
    recip_strength = np.clip(R.mean(axis=1), 0, 1)
    extraction = extraction * (1 - recip_strength)  # those with low reciprocity more likely exploited
    Phi = Phi - kappa * (Phi - Phi_mean) + cooperative - extraction
    # keep Phi bounded and non-negative
    Phi = np.clip(Phi, 0.1, 10.0)
    
    # 5) Entropy diffusion and agency reduction effect
    # discrete Laplacian approximation: S_new = S + D_S*(A*S - S) - lambda_v * |v| + noise
    neighbor_S = (A * S[None, :]).sum(axis=1)
    S = S + D_S * (neighbor_S - S) - lambda_v * np.abs(v) + 0.01 * np.random.randn(N)
    S = np.clip(S, 0.01, 10.0)
    
    # 6) Affinity update: small adjustment toward reciprocity, penalize edges that increase central Phi concentration
    # compute centrality proxy: node Phi relative to mean
    phi_centrality = (Phi - Phi_mean) / (Phi_mean + 1e-9)
    # update A towards R but shrink edges connected to very central nodes
    A_target = R.mean(axis=1)[:, None] * R.mean(axis=0)[None, :]
    # normalize target rows
    row_s = A_target.sum(axis=1, keepdims=True)
    row_s[row_s == 0] = 1.0
    A_target = A_target / row_s
    # penalize connections to very central nodes
    penal = 1.0 - np.clip(phi_centrality, 0, 0.5)  # if central, penal <1
    A = 0.95 * A + 0.05 * (A_target * penal[:, None])
    # renormalize rows
    row_sums = A.sum(axis=1, keepdims=True)
    row_sums[row_sums == 0] = 1.0
    A = A / row_sums
    
    # Ensure v and S don't explode
    v = np.clip(v, 0.0, 2.0)
    
    # Collect metrics
    phi_conc[t] = phi_concentration_index(Phi)
    agency_ret[t] = agency_retention(v, eps=0.03)
    reciprocity_med[t] = np.median(R[R > 0]) if np.any(R > 0) else 0.0
    entropy_grad[t] = entropy_gradient_metric(S, A)

# Build DataFrame of metrics
df = pd.DataFrame({
    "t": np.arange(T),
    "phi_conc": phi_conc,
    "agency_ret": agency_ret,
    "reciprocity_med": reciprocity_med,
    "entropy_grad": entropy_grad
})

# Plot metrics (each in its own figure as required)
plt.figure(figsize=(8,3.5))
plt.plot(df["t"].values, df["phi_conc"].values)
plt.title("Phi Concentration Index (top 1% share of Phi)")
plt.xlabel("Timestep")
plt.ylabel("C_phi")
plt.grid(True)
plt.tight_layout()
plt.show()

plt.figure(figsize=(8,3.5))
plt.plot(df["t"].values, df["agency_ret"].values)
plt.title("Agency Retention (fraction of nodes with v > 0.03)")
plt.xlabel("Timestep")
plt.ylabel("Agency retention")
plt.grid(True)
plt.tight_layout()
plt.show()

plt.figure(figsize=(8,3.5))
plt.plot(df["t"].values, df["reciprocity_med"].values)
plt.title("Median Reciprocity (R) over nonzero edges")
plt.xlabel("Timestep")
plt.ylabel("Reciprocity (median)")
plt.grid(True)
plt.tight_layout()
plt.show()

plt.figure(figsize=(8,3.5))
plt.plot(df["t"].values, df["entropy_grad"].values)
plt.title("Entropy Gradient Metric (smaller is smoother)")
plt.xlabel("Timestep")
plt.ylabel("Entropy gradient")
plt.grid(True)
plt.tight_layout()
plt.show()
# Display final snapshot of distributions (summary)
summary = pd.DataFrame({
    "metric": ["Phi_mean", "Phi_std", "v_mean", "v_std", "S_mean", "S_std"],
    "value": [Phi.mean(), Phi.std(), v.mean(), v.std(), S.mean(), S.std()]
})

# Safe display for Jupyter or plain Python
try:
    import caas_jupyter_tools as cjt
    cjt.display_dataframe_to_user("Lamphrodyne Simulation Summary", summary)
    cjt.display_dataframe_to_user("Lamphrodyne Metrics Timeseries (first 50 rows)", df.head(50))
except ModuleNotFoundError:
    print("\nLamphrodyne Simulation Summary:\n", summary)
    print("\nLamphrodyne Metrics Timeseries (first 10 rows):\n", df.head(10))

# Save CSVs explicitly next to the script
import os
save_dir = os.path.dirname(os.path.abspath(__file__))
df.to_csv(os.path.join(save_dir, "lamphrodyne_metrics.csv"), index=False)
summary.to_csv(os.path.join(save_dir, "lamphrodyne_summary.csv"), index=False)

print(f"\nSaved metrics to {save_dir}/lamphrodyne_metrics.csv and lamphrodyne_summary.csv")
