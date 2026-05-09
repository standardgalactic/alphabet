# Beyond the Economy of Thought: Challenging the Simplicity Principle through Excess Capacity Learning

# 1. Introduction: The Crisis of the Simplicity Paradigm

For more than a century, cognitive science has been dominated by the simplicity principle.

This paradigm assumes that the human mind fundamentally operates as a compression engine, transforming rich and noisy experience into parsimonious internal representations.

The historical justification for this framework appeared intuitive:

- biological resources are finite,
- environments are overwhelmingly complex,
- and cognition must therefore simplify reality in order to function efficiently.

Within this tradition, memorization was frequently treated as noise retention, while generalization was interpreted as successful abstraction away from irrelevant variance.

Modern developments in machine learning and statistical learning theory increasingly challenge this assumption.

Contemporary overparameterized systems demonstrate that complexity itself may support stable generalization rather than undermine it.

The emerging picture suggests that robust learning can arise not from aggressive compression, but from excess representational capacity.

This creates a profound theoretical tension between two competing frameworks:

| Traditional Compression View | Excess Capacity View |
|---|---|
| Memorization and generalization compete | Memorization and generalization can coexist |
| Complexity produces instability | Complexity can stabilize interpolation |
| Simplicity is necessary for prediction | Overparameterization can improve prediction |
| Variance must be discarded | Variance can be preserved without collapse |

The central claim of this framework is that cognitive behavior depends on representational capacity:

the relationship between a system’s internal expressivity and the amount of experience it must process.

---

## Three Capacity Regimes

### Constrained Capacity

The system lacks sufficient resources to memorize individual experiences.

Compression becomes mandatory.

Unique details are discarded in favor of simplified summaries.

---

### Sufficient Capacity

The system possesses exactly enough resources to memorize prior experiences.

This regime is unstable and hypersensitive to noise.

Small fluctuations produce erratic generalization.

---

### Excess Capacity

The system possesses more representational resources than required for memorization.

This permits:

- expansion of detail,
- complex transformations,
- stable interpolation,
- and simultaneous memorization and generalization.

---

## The Strategic Limitation of the Simplicity Principle

Historically, the economy-of-thought framework acted as a strategic straightjacket for cognitive modeling.

It constrained theoretical development to architectures where:

- memory was treated as interference,
- detail was treated as noise,
- and abstraction was treated as elimination.

The recognition that excess capacity can support robust intelligence requires a fundamental redesign of cognitive theory itself.

---

# 2. Historical Foundations of Constrained Capacity

The simplicity tradition emerged from the assumption that biological limitation defines normative intelligence.

Early theorists transformed metabolic constraints into psychological doctrine.

A “good” representation became synonymous with a simple one.

Variance was treated as distraction.

Invariant structure was treated as truth.

---

# The Tradition of Parsimony vs. the Excess Capacity Revision

| Author | Traditional View of Parsimony | Excess Capacity Revision |
|---|---|---|
| **Mach (1905)** | Thought seeks reduction to leading ideas | Expanded representational richness may improve learning |
| **Koffka (1935)** | Organization tends toward simplicity | Effective organization may violate simplicity |
| **Sherry & Schacter (1987)** | Variance and invariance preservation conflict | One system may preserve both |
| **McClelland & Goddard (1996)** | Structure extraction conflicts with trace storage | Memorization and abstraction can coexist |
| **Chater (1999)** | Simplicity supports prediction | Complex representations may also guide prediction |
| **Gigerenzer (2008)** | Good decisions ignore information | Robust learning may preserve situational richness |
| **Sherman & Turk-Browne (2020)** | Episodic and statistical learning require separate mechanisms | A single mechanism may support both |
| **Frankland et al. (2021)** | Efficiency trades off against decoding accuracy | No fundamental tradeoff may exist |

---

# From Tradeoff to Decoupling

Classical statistical reasoning relied on the bias–variance tradeoff.

Increasing complexity supposedly reduced bias while increasing variance catastrophically.

Excess capacity systems violate this assumption.

The relationship between memorization and generalization becomes decoupled.

Perfect interpolation no longer guarantees collapse.

---

# 3. The Capacity Framework: A New Taxonomy for Cognitive Systems

Representational capacity must be defined relationally rather than absolutely.

Capacity is the ratio between:

- expressivity,
- and accumulated experience.

---

# Technical Ontology

| Concept | Operational Definition |
|---|---|
| **Cognitive System** | A system that learns mappings from situations to outcomes |
| **Situations** | External contexts or inputs |
| **Experiences** | Situations paired with outcomes |
| **Representations** | Internal predictive transformations |
| **Learned Patterns** | Anticipated outcomes derived from representations |
| **Representational Resources** | Biological or computational expressive resources |
| **Expressivity** | The total representational possibilities available |
| **Capacity** | Expressivity relative to experience volume |

---

# The Three Learning Regimes

## 1. Constrained Capacity

```text
p < n
```

The system lacks sufficient expressive resources.

Compression becomes mandatory.

Generalization emerges through hard restriction biases.

---

## 2. Sufficient Capacity

```text
p ≈ n
```

The system exactly interpolates the training data.

This regime is maximally unstable.

Noise propagates globally.

---

## 3. Excess Capacity

```text
p > n
```

Representations become richer than the experiences themselves.

The system utilizes:

- expansion,
- redundancy,
- and convoluted transformations

to stabilize learned structure.

---

# Variable vs. Constant Capacity

Natural systems typically operate under fixed expressivity.

As experience accumulates, capacity regimes shift dynamically.

Perfectly scaling resources with data volume is computationally prohibitive:

```text
Compute ≈ O(n³)
Memory ≈ O(n²)
```

Human cognition is therefore best interpreted as navigation through changing capacity regimes under fixed biological resources.

---

# 4. Decoupling Memorization and Generalization: The Double Descent Phenomenon

The strongest evidence against the simplicity principle is the Double Descent curve.

Traditional statistics predicts a U-shaped relationship between complexity and error.

Overparameterized systems violate this expectation.

---

# The Interpolation Threshold

As complexity increases:

1. bias initially decreases,
2. variance increases,
3. error peaks at interpolation,
4. and then unexpectedly decreases again.

This second reduction in error defines the Second Descent regime.

---

# Benign Overfitting

In excess capacity systems, overfitting becomes computationally useful.

The system discovers minimum-norm solutions capable of:

- perfectly fitting noisy training points,
- while preserving smooth global structure.

---

# Why Excess Capacity Generalizes

## 1. Soft Inductive Biases

Optimization procedures such as stochastic gradient descent guide systems toward specific stable solutions.

Generalization emerges from optimization geometry rather than explicit compression.

---

## 2. Flat Minima

The system prefers broad, stable solutions rather than brittle sharp minima.

This reduces sensitivity to local perturbation.

---

## 3. Neural Collapse

High-dimensional representations collapse into evenly spaced class partitions.

The representation becomes globally smooth despite perfect interpolation.

---

# The Collapse of Dual-Process Assumptions

If one sufficiently expressive system can simultaneously:

- memorize detail,
- and generalize structure,

then separate modules for:

- rules,
- and exceptions

may no longer be theoretically necessary.

---

# 5. Diagnosing the Capacity Regime in Natural Systems

Capacity cannot be inferred from a single behavioral metric.

Diagnosis requires clusters of learning signatures.

---

# Six Key Learning Properties

## 1. High Recognition Ability

Humans retain enormous quantities of episodic detail.

Brady et al. (2008) demonstrated recognition of 2,500 objects with accuracy exceeding 80%.

---

## 2. Detailed Representations

Learners frequently preserve seemingly irrelevant detail.

Lupyan (2013) showed reliance on unnecessary features during categorization.

---

## 3. Learned Patterns as Summaries

Humans extract smooth prototypes from detailed experiences.

Posner & Keele (1968) demonstrated faster recognition for unseen category prototypes than for individual exemplars.

---

## 4. Perceptual Deterioration

Extensive training can reduce performance.

This reflects decreasing relative excess capacity as experience volume grows.

---

## 5. Decreased Smoothness

As excess resources diminish:

- distinctions sharpen,
- but false recognition increases.

Exceptions begin collapsing into generalized categories.

---

## 6. High Noise Sensitivity

Excess systems attempt to model every fluctuation.

This makes them highly sensitive to noisy environments.

---

# 6. Broad Theoretical Implications: Memory, Development, and Clinical Dissociations

The framework offers a unified interpretation of multiple domains traditionally treated independently.

---

# Clinical Dissociations

## Amnesia as Constrained Capacity

Amnesic systems:

- preserve generalized rules,
- but fail to retain episodic detail.

This resembles constrained capacity dynamics.

---

## Parkinson’s Disease as Sufficient Capacity

Parkinsonian learning initially resembles the unstable sufficient regime:

- memorization preserved,
- generalization impaired.

Later adaptation may reflect transition toward constrained processing.

---

# U-Shaped Development

The classic developmental sequence:

```text
went → goed → went
```

can be interpreted as a temporary reduction in relative excess capacity.

Vocabulary growth outpaces expressive resources.

Compression temporarily dominates.

Exceptions disappear until expressivity catches up.

---

# Episodic-to-Gist Transitions

Changes from local episodic memory toward global summary behavior may emerge naturally from decreasing excess capacity over time.

No separate “rule module” is required.

---

# 7. Addressing Criticisms: Parsimony, Biological Constraints, and AI

Critics frequently argue that excess capacity is metabolically inefficient.

This assumption may be incorrect.

---

# Biological Realization

Biological systems already exhibit massive representational expansion.

For example:

```text
cat V1 expansion ratio ≈ 25:1
```

relative to input volume.

The nervous system appears structurally optimized for abundance rather than minimalism.

---

# AI Paradigms

## CNNs

Convolutional Neural Networks frequently operate in the excess regime.

They can memorize random labels while still generalizing on structured tasks.

---

## LLMs

Large Language Models may actually operate in a constrained regime relative to dataset scale.

They memorize only a tiny fraction of total training examples:

```text
≈ 0.2%–1.5%
```

---

# Adversarial Vulnerability

Adversarial attacks emerge naturally within excess systems.

Because the system attempts to fit all deviations, small perturbations may produce disproportionate adjustments.

These are expected consequences of high-fidelity interpolation.

---

# 8. Conclusion: Toward a New Era of Cognitive Modeling

The simplicity principle is no longer sufficient as a normative theory of intelligence.

Complexity, when guided by stable inductive biases, may itself become a source of robustness.

The human mind may be best understood not as a machine for simplification,

but as a system for navigating abundance without collapse.

---

# Future Research Priorities

## 1. Regime-Specific Diagnostics

Develop behavioral markers capable of tracking transitions between:

- constrained,
- sufficient,
- and excess regimes.

---

## 2. Process Mapping

Identify which cognitive functions operate under which capacity conditions.

---

## 3. Biological Foundations

Determine how biological systems realize the soft inductive biases required for benign overfitting.

---

# Final Synthesis

The curse of complexity may have been a theoretical illusion.

Generalization does not necessarily require forgetting.

Compression is not always intelligence.

Sometimes stability emerges because a system possesses enough structure to preserve detail without losing coherence.
