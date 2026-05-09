# The Palette of Learning: A Comparative Framework for Cognitive Capacity

# 1. Introduction: The Art of Representation

In his lithograph series *The Bull*, Pablo Picasso demonstrated a profound principle of cognition through artistic reduction.

He began with a detailed, anatomically rich depiction of a bull and gradually stripped it down through successive transformations until only a minimal set of lines remained.

The series captures a fundamental challenge faced by every cognitive system.

Whenever a mind encounters the world, it must decide:

- should it preserve detail,
- or compress experience into abstraction?

This tension defines the architecture of learning itself.

---

# The Master Question of Learning

```text
How do systems decide whether to simplify the world
or add detail to it?
```

The answer depends on representational capacity.

---

# Representational Capacity

Representational Capacity is the relationship between:

- the expressive resources available to a system,
- and the total history of experiences the system must encode.

Capacity is therefore not a static quantity.

It is a relative condition governing the geometry of learning.

The “palette” available to a learner determines:

- whether experiences are compressed,
- preserved,
- expanded,
- or transformed.

---

# 2. The Variables of the Learning Equation

Learning can be understood through the interaction of three core variables.

| Term | Teacher’s Definition | Computer Science Analogue |
|---|---|---|
| **Expressivity** | The total size of the system’s imagination | Number of parameters `(θ)` or model complexity |
| **Experiences** | The accumulated history of situations and outcomes | Dataset size `(n)` |
| **Capacity** | Remaining expressive breathing room | Parameter-to-data ratio `(θ / n)` |

---

# The Inverse Relationship

Capacity changes dynamically.

It increases when:

- expressive resources grow,
- or experience volume decreases.

It shrinks when experience accumulates faster than expressivity.

---

# The Shrinking Mind

Natural systems generally operate under fixed expressivity.

Biological architecture changes slowly relative to experience accumulation.

This creates variable capacity dynamics.

A child initially possesses enormous excess capacity relative to their tiny world.

As vocabulary, social complexity, and sensory experience accumulate, the same biological substrate must encode vastly more information.

Relative capacity therefore shrinks over developmental time.

A learner may transition from:

```text
Excess Capacity → Sufficient Capacity → Constrained Capacity
```

without losing any biological structure at all.

Only the ratio changes.

---

# 3. Comparative Framework: The Three Capacity Regimes

# 1. Constrained Capacity — The Sketch

## Definition

The system lacks sufficient resources to memorize its history.

---

## Behavior

Compression becomes mandatory.

The learner must discard detail in order to preserve stable general structure.

---

## Artistic Analogy

A minimalist sketch.

The representation preserves “bull-ness” while discarding texture, shadow, and nuance.

---

## Resulting Representation

A simplified abstraction dominated by general rules.

---

# 2. Sufficient Capacity — The Interpolation Threshold

## Definition

The system possesses exactly enough resources to memorize prior experience.

---

## Behavior

This regime is maximally unstable.

The learner interpolates history perfectly but becomes hypersensitive to noise and fluctuation.

---

## Artistic Analogy

An expressionist reconstruction that perfectly captures a scene under one condition but collapses under slight perturbation.

---

## Resulting Representation

An exact but brittle reconstruction of experience.

---

# 3. Excess Capacity — The Hyper-Realist

## Definition

The system possesses substantially more resources than required for memorization.

---

## Behavior

The learner expands detail rather than compressing it.

Representations become richer than the raw experiences themselves.

---

## Artistic Analogy

A hyper-realist painting.

The system captures every local detail while preserving surprising global smoothness.

---

## Resulting Representation

An overparameterized but stable representation.

---

# Restriction Biases vs. Soft Inductive Biases

The style of the final “painting” depends on the internal geometry of the learner.

---

## Restriction Biases

Constrained systems possess hard limitations.

They are physically unable to represent complexity and must therefore simplify.

---

## Soft Inductive Biases

Excess systems possess many possible solutions.

They rely on optimization preferences:

- smoothness,
- minimum norm,
- and stable interpolation geometry.

---

# Example: U-Shaped Development

Children frequently display transitions such as:

```text
went → goed → went
```

This reflects movement across capacity regimes.

Initially:

- the child memorizes the exception,
- operating in an excess or sufficient regime.

As vocabulary grows:

- relative capacity shrinks,
- compression dominates,
- and the generalized rule overwhelms the exception.

Eventually:

- expressive structure catches up,
- restoring the exceptional form.

---

# 4. The Paradox of Knowledge: Generalization and Double Descent

Traditional learning theory assumed:

```text
To generalize, you must forget.
```

This assumption is incomplete.

---

# The Classical Bias–Variance Tradeoff

Traditional statistics predicts:

- low complexity → underfitting,
- moderate complexity → optimal generalization,
- high complexity → catastrophic overfitting.

This produces the classical U-curve.

---

# The Double Descent Revision

Overparameterized systems violate the classical curve.

Generalization error initially rises toward the interpolation threshold.

But after sufficient capacity is exceeded, error decreases again.

This is the Second Descent regime.

---

# Comparative Dynamics

| Regime | Training Error | Generalization Error |
|---|---|---|
| **Constrained** | High | Gradually decreases |
| **Sufficient** | Zero | Peaks catastrophically |
| **Excess** | Zero | Decreases again |

---

# Benign Overfitting

In excess systems, overfitting becomes computationally useful.

The learner possesses enough freedom to:

- interpolate all data points,
- while preserving smooth global structure.

---

# Minimum-Norm Geometry

Excess systems gravitate toward minimum-norm solutions.

The optimization objective becomes:

:contentReference[oaicite:0]{index=0}

The learner therefore selects the smoothest stable representation among many possible exact interpolations.

This additional freedom stabilizes rather than destabilizes learning.

---

# 5. Diagnostic Signatures: Detecting Capacity Regimes in the Wild

Capacity regimes can be diagnosed behaviorally.

Three major signatures are especially informative.

---

# 1. The Memory Test

## Signature of Sufficient or Excess Capacity

Brady et al. (2008) demonstrated that humans recognized 2,500 objects with approximately 80% accuracy after only brief exposure.

This level of episodic retention is inconsistent with purely constrained compression architectures.

---

# 2. The Experience Paradox

## Signature of Excess Capacity

Adding more experience can sometimes reduce performance.

This occurs because growing data volume consumes the representational slack responsible for smooth interpolation.

The learner drifts back toward the unstable interpolation threshold.

This phenomenon appears experimentally as perceptual deterioration.

---

# 3. Complexity and Noise Sensitivity

## Signature of Sufficient or Excess Capacity

Learners frequently preserve unnecessary detail.

Lupyan (2013) demonstrated reliance on superficial geometric cues during categorization tasks even when simpler rules were available.

Excess systems also remain highly sensitive to noise because they attempt to fit every fluctuation.

Constrained systems simply ignore many perturbations entirely.

---

# Final Synthesis

Learning is not merely the elimination of information.

It is the negotiation between:

- expressive structure,
- accumulated history,
- and the geometry of admissible representation.

Sometimes intelligence emerges through simplification.

But sometimes the path to robust understanding requires enough capacity to preserve detail without collapse.

Wisdom may not always come from reducing the world into a sketch.

Sometimes it comes from having enough representational abundance to paint the entire canvas.
