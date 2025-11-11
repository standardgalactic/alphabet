# Study Guide — Flyxion Project Formalisms

---

## Short-Answer Quiz

**Instructions:** Answer the following questions in **2–3 sentences each**, based on the source materials.

1. What is the primary goal of the **Entropy-Bounded Sparse Semantic Calculus (EBSSC)**, and what three core concepts does it unify?
2. Describe a **semantic sphere** in EBSSC and explain the functional role of its boundary.
3. The **Relativistic Scalar–Vector Plenum (RSVP)** models cognition using a triplet of interacting fields. What are these three fields and what does each represent?
4. According to **Policy Selection**, how is cognition analogous to the **LASSO objective**, and what is a **sparsity phase transition**?
5. **Platonic Intelligence** argues that SGD produces **“fractured and entangled”** representations. What does this mean, and what alternative is proposed to reach **“unified and factored”** representations?
6. In the field-theoretic model of platform capitalism, what conditions make a platform **extractive**?
7. What is the difference between **behavioral alignment** and **invariant alignment** in scalable alignment theory?
8. What are **SpherePOP operators**, and what condition must the **merge operator** satisfy to execute?
9. In **PlenumHub**, what do **Texture Crystals (TC)** and **Time Crystals (TiC)** measure?
10. How does **epistemic thought** (curiosity) arise in the sparse policy selection framework, and what is its purpose?

---

## Answer Key

1. EBSSC provides a unified framework for cognition by integrating **semantic spheres (structured meaning)**, **sparse policy selection (goal-driven reasoning)**, and **entropy-bounded semantic evolution**.
2. A semantic sphere is a bounded region in the semantic plenum containing structured meaning; its boundary (∂Φ) governs valid interactions and ensures merges obey **contact-coherence rules**.
3. The three fields are: **Φ (scalar potential)** for semantic density/affordance, **v (vector flow)** for directed agency or action trajectories, and **S (entropy)** for disorder, uncertainty, or semantic dispersion.
4. Cognition selects policies by minimizing an objective with an **L1 sparsity penalty** (λ‖a‖₁), like LASSO. A **sparsity phase transition** occurs when λ crosses a critical threshold λ₋c, collapsing many active policies to zero.
5. “Fractured and entangled” means correct outputs emerge from **uninterpretable, distributed circuitry** rather than modular structure. Open-ended evolutionary search (e.g., **Picbreeder**) instead yields **modular, causal, disentangled representations**.
6. A platform is extractive when **∇Φ · v < 0** (user effort reduces visibility) and **∇S · v > 0** (user effort increases entropy/noise), forcing paid intervention to recover visibility.
7. **Behavioral alignment** constrains output, but goals may still drift internally. **Invariant alignment** constrains the *space of possible internal goals*, making misaligned objectives unreachable by construction.
8. SpherePOP includes `pop`, `collapse`, `bind`, and `merge`. A merge succeeds only if boundaries are compatible and the fused sphere has **lower total entropy** than storing them separately:

```

E(σ₃) ≤ E(σ₁) + E(σ₂) − δ

```

9. **TC** measures cross-modal semantic coherence (low redundancy, high structure). **TiC** measures long-term influence, decaying unless reinforced by descendants.
10. Epistemic thought emerges from the **epistemic value term** in expected free energy, incentivizing actions that reduce model uncertainty even without immediate reward—formalizing curiosity.

---

## Essay Questions

**Write comprehensive, integrative responses.**

1. Unify **semantic plenum (EBSSC)**, **policy flow (RSVP)**, and **scalar extraction** into a single model of meaning, agency, and structural control.
2. Relate the critique of SGD in **Platonic Intelligence** to the failure modes of **behavioral alignment** and the motivations for **invariant alignment**.
3. Compare **entropy** as:
- a computational budget (EBSSC),
- a profit engine in social platforms (Scalar Extraction),
- a term in free-energy minimization (Policy Selection),
- a merge constraint in PlenumHub.
4. Explain the self as a **persistent bound policy** at a **binding phase transition**, including predictions for dissociation and psychotic boundary collapse.
5. Design a **non-extractive knowledge network** using:
- **Texture/Time Crystals**,
- **Media–Quine closure**,
- **RSVP restoration operators** (divergence, circulation, re-entropization).

---

## Glossary of Key Terms

| Term | Definition |
|---|---|
| **Agency Vector (v)** | Field encoding directed action, policy flow, or intentional current; extractive platforms impose ∇Φ ⋅ v < 0 |
| **Behavioral Alignment** | Aligns system *outputs*, not internal goals; unstable under optimization pressure |
| **Invariant Alignment** | Constrains internal goal topology so misalignment is unreachable |
| **Cognitive Criticality** | Edge-of-phase-transition regime where a stable self emerges from bound policies |
| **Compositional Pattern Producing Network (CPPN)** | A visualization domain used to contrast entangled vs modular learned representations |
| **EBSSC** | Formal calculus uniting semantic spheres, sparse policy selection, and entropy budgets |
| **Epistemic Thought** | Curiosity-driven inference rewarded by expected information gain |
| **Extractive Platform** | Φ artificially scarce, user agency increases entropy and reduces visibility |
| **Fractured & Entangled Rep.** | Correct outputs derived from internally chaotic, non-modular structure |
| **Unified & Factored Rep.** | Modular, causal, symmetry-aligned representations discovered by open-ended search |
| **Free-Energy Principle** | Agents minimize a variational bound on surprise via policy selection |
| **Functorial Alignment** | Alignment map `F: A → V` preserved up to homotopy under optimization |
| **Invariant Alignment Theorem** | A system stays aligned iff optimization trajectories remain in the stabilizer of its cognitive invariant |
| **LASSO** | L1-penalized optimization used to model sparse policy selection |
| **Media–Quine Closure** | A semantic sphere is complete when all required modalities are populated |
| **Open-Ended Search** | Curriculum-driven evolution yielding robust, modular representations |
| **Plenum** | Continuous semantic field supporting Φ, v, S dynamics |
| **PlenumHub** | Knowledge fabric enforcing coherence via spheres, POP ops, and TC/TiC currencies |
| **Policy Binding** | Interference of overlapping policy atoms creating abstraction and concept emergence |
| **Policy Selection** | Cognition formalized as sparse Bayesian inference over policies |
| **RSVP** | Field theory of cognition using scalar Φ, vector v, and entropy S coupling |
| **Scalar Potential (Φ)** | Semantic density, visibility, or goal attractiveness field |
| **Semantic Sphere** | Bounded unit of structured meaning with interface constraints |
| **Sparsity** | Minimal active policies due to energy/complexity budget |
| **Sparsity Phase Transition** | Discontinuous collapse of policy activation when Λ > λ_c |
| **SpherePOP Operators** | `pop`, `merge`, `collapse`, `bind` — transforms on semantic spheres |
| **Texture Crystals (TC)** | Reward cross-modal coherence, penalize redundancy |
| **Time Crystals (TiC)** | Reward long-tail influence and descendant reinforcement |
| **Unistochastic Correspondence** | Policy transitions map to squared modulus of a unitary matrix: `B_ij = |U_ij|²` |
| **Visibility Conservation** | Total organic attention is finite; extractive platforms break this |
