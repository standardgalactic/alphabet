# A Computational Framework for Modeling Cognitive Pathologies  
## as Dynamical System Failures in a Semantic Plenum

---

## 1.0 Introduction and Statement of the Problem

Contemporary models of psychiatric and cognitive disorders provide valuable diagnostic taxonomies, yet they lack **first-principles mechanistic explanations** for how such states emerge and persist. Current classification systems tend to treat pathologies as fixed defects, rather than **stable but maladaptive attractor states** within cognitive dynamics.

We propose a new paradigm in which **mental disorders are formalizable dynamical failures** in a unified cognitive substrate. Our model integrates:

1. **Sparse goal-directed policy selection under metabolic constraint**
2. **Meaning represented as an entropy-bounded geometric field**
3. **Thought evolving within a physical dynamical plenum**

> **Central Hypothesis:**  
> Cognitive pathologies are *predictable failure modes* of a unified plenum in which:
> - semantic potential collapses (depression),
> - epistemic drives overpower action (anxiety),
> - or concept-binding undergoes critical phase transitions (psychosis).

This framework advances psychiatry toward a **computational physics of the mind**, replacing descriptive labels with **measurable dynamical equations** governing pathology.

---

## 2.0 Theoretical Foundations

### 2.1 Cognition as Sparse Bayesian Policy Selection

Cognition is framed as **policy inference** minimizing expected free energy:

- Policies are **evaluated for expected surprise reduction**
- Metabolic limits enforce **sparsity via Laplacian / L1 (LASSO) priors**
- Thought is **pruned selection, not exhaustive search**
- Two competing drives govern selection:
  - **Pragmatic** (goal acquisition)
  - **Epistemic** (uncertainty reduction / curiosity)

Healthy cognition balances both drives.

---

### 2.2 Semantics as an Entropy-Bounded Sparse Semantic Calculus (EBSSC)

Concepts are modeled as **semantic spheres** in a bounded entropy field.

Thought evolves via **SpherePOP operators**:

| Operator | Meaning |
|---|---|
| `pop` | expands a concept |
| `merge` | fuses two conceptual spheres |
| `collapse` | prunes a concept |

Each operation consumes an **entropy budget**, preventing representational drift and instability.

---

### 2.3 The Relativistic Scalar-Vector Plenum (RSVP)

Cognition evolves within a coupled physical field:

| Field | Role |
|---|---|
| **Scalar Potential (Φ)** | Meaning, goal affordance landscape |
| **Vector Field (v)** | Policy flow / agentic motion |
| **Entropy Field (S)** | Disorder, uncertainty, thermodynamic cost |

Cognition becomes a **flow through Φ driven by v under entropic constraint S**.

---

## 3.0 Pathologies as Plenum Dysfunctions

### 3.1 Formal Definition of Cognitive Pathology

A pathological cognitive state satisfies:

- **Agency opposition:**  
  `∇Φ · v < 0`  
  (effort moves against meaning gradient)
- **Entropy alignment:**  
  `∇S · v > 0`  
  (actions increase disorder)

These describe **self-reinforcing maladaptive attractors**.

---

### 3.2 Specific Modeled Disorders

#### **Depression: Semantic Potential Collapse**
- `∇Φ → 0` (flat meaning landscape)
- No salience gradient → no goal formation
- Matches **anhedonia, avolition**

#### **Anxiety: Epistemic Overdrive**
- Curiosity dominates pragmatics
- System seeks uncertainty reduction regardless of cost
- Manifests as **rumination, compulsive checking**

#### **Psychosis: Concept-Binding Phase Transition**
Controlled by λ₂ (concept binding cost):

| Regime | Effect | Outcome |
|---|---|---|
| λ₂ → low | Over-binding | delusion, spurious meaning |
| λ₂ → high | Under-binding | literalism, disorganized thought |

---

### 3.3 Representation Quality Determines Stability

Following Kumar (2023):

| Representation Type | Property | Outcome |
|---|---|---|
| **Factored** | modular, orthogonal | resilient cognition |
| **Fractured** | entangled, brittle | pathological attractors likely |

---

## 4.0 Research Objectives

1. **Implement RSVP + EBSSC simulation**
2. **Induce and characterize pathological attractors**
3. **Generate falsifiable clinical predictions**

---

## 5.0 Methodology & Project Plan

### **Phase 1: Implement healthy baseline (Months 1–6)**
- Solve plenum dynamics with **Crank–Nicolson integration**
- Embed **SpherePOP operators as sparse interventions**

### **Phase 2: Induce pathologies (Months 7–15)**
- Sweep parameters:  
  `λ (sparsity), κ (curiosity), λ₂ (binding cost), γ (self persistence)`
- Track:
  - Gini(Φ)
  - ⟨∇Φ · v⟩
  - `dS/dt`

### **Phase 3: Behavioral predictions (Months 16–20)**
Examples include:

| Prediction Type | Claim |
|---|---|
| **Sparsity scaling** | Active policies grow sub-linearly with task complexity |
| **Semantic lightcone** | Concept influence propagates at finite speed |
| **Critical transitions** | Sharp onsets of rumination or delusion |
| **Memory decay** | Exponential, not power-law |

### **Phase 4: Publish + share toolkit (Months 21–24)**  
Open-source release will include:
- Field solvers
- SpherePOP engine
- Pathology phase diagrams
- Clinical test mappings

---

## 6.0 Impact & Significance

| Contribution | Impact |
|---|---|
| **Mechanistic psychiatry** | replaces symptom categories with dynamical laws |
| **New biomarkers** | e.g., plenum viscosity, dS/dt, Gini(Φ) |
| **Therapeutic operators** | restore gradient or break attractor basins |
| **Unified cognition model** | reasoning, curiosity, pathology, self-model arise from same equations |

---

## 7.0 References

1. Barandes, J. A. (2022). *Unistochastic matrices and quantum-classical correspondences.* Entropy, 24(8), 1072.  
2. Donoho, D. L., & Tanner, J. (2009). *Phase transitions in high-dimensional geometry.* PTRS A, 367(1906), 4273–4293.  
3. Friston, K. (2010). *The free-energy principle: A unified brain theory.* Nature Reviews Neuroscience, 11(2), 127–138.  
4. Jaynes, E. T. (1957). *Information theory and statistical mechanics.* Physical Review, 106(4), 620–630.  
5. Kumar, A. (2023). *Towards a Platonic Intelligence with Unified Factored Representations.*  
6. Tibshirani, R. (1996). *Regression shrinkage via the LASSO*, JRSSB, 58(1), 267–288.

---

### *Mind, modeled as matter flowing toward coherence.*

