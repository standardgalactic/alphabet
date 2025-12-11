# Formal Foundations of Spherepop Calculus

## Overview

Spherepop Calculus is a novel formalism designed to address a persistent explanatory gap between abstract cognitive theories—such as linguistic models positing hierarchical and recursive structure—and the dynamic, continuous measurements provided by neuroscience. The calculus provides a minimal, counterfactually complete substrate for cognition by grounding abstract structure not in static representational objects but as invariants of temporally extended event histories.

By doing so, it offers a shared generative mechanism capable of reconciling the discrete, algebraic character of cognitive principles with the noisy, distributed nature of neural dynamics.

Traditional state-based models and contemporary statistical systems, including large language models (LLMs), exhibit structural limitations as explanatory frameworks. State-based approaches collapse generative history into momentary summaries, rendering them incapable of determining lawful reuse. Statistical models operate on surface projections of histories rather than the histories themselves, making them correlational rather than explanatory.

This document provides a rigorous mathematical specification of Spherepop Calculus, detailing its axioms, operators, and formal guarantees.

---

## 1. Event-First Ontology

Spherepop Calculus adopts an event-first ontology. Cognitive systems are defined by constrained spaces of event histories rather than instantaneous states. Explanation is therefore concerned with admissible transformations over histories, not stored representations.

### Core Concepts

- **Construction History**: Identity is path-dependent, defined by an irreversible sequence of events.
- **Irreversibility**: Events cannot be undone without altering system identity.
- **Constraint Accumulation**: Time is the accumulation of irreversible constraints.
- **Replayability**: Memory is the ability to reconstruct a construction history.

### Structural Invariants

Abstract structure is defined as an equivalence class of histories \([H]_\sim\), preserving dependency structure while abstracting away local variability. Intelligence consists in identifying and lawfully transferring these invariants.

---

## 2. Axiomatic Specification of the Spherepop Kernel

### Axiom 2.1 — Authoritative Event Log
A single append-only log \(L\) records all admissible events.

### Axiom 2.2 — Total Causal Order
Events admit a globally consistent causal ordering.

### Axiom 2.3 — Deterministic Replay
Replay of any log prefix deterministically yields semantic configuration \(\Sigma\).

### Axiom 2.4 — Invariant-Preserving Collapse
An equivalence relation \(\sim\) and collapse operator \(D_{pop}\) yield canonical representatives of \([H]_\sim\).

### Axiom 2.5 — Explicit Intervention Semantics
Well-typed interventions act on \(L\) and are either admissible or rejected.

### Axiom 2.6 — View Non-Interference
All views are read-only and cannot modify the log.

---

## 3. Typed Event Algebra

A **Typed Event** is written:

```
Γ ⊢ e : τ ⇒ τ′
```

Histories are sequences of typed events.

### Composition

- **Sequential (◦)**: End-to-end composition
- **Parallel (‖)**: Union of commutative event sets

### Semantic Equivalence

Two histories are equivalent if they induce the same invariant:
\[ H₁ \sim H₂ \iff [H₁]_\sim = [H₂]_\sim \]

---

## 4. Core Operators

### Merge
Geometric union of event regions; associative up to collapse.

### Collapse (Dpop)
Projects regions into canonical invariant representatives.

### Commit
An irreversible kernel event rendering a region indivisible and inaccessible to reassociation.

---

## 5. Formal Results

### Proposition 5.1 — Commit-Enforced Nonassociativity
Irreversible commit prohibits reassociation by construction.

### Theorem 5.2 — Replay Soundness
Successful replay implies admissibility.

### Theorem 5.3 — Replay Completeness
All admissible counterfactuals are decidable via replay.

### Theorem 5.4 — Counterfactual Completeness
Event-first systems with logs, replay, collapse, and intervention semantics are explanatory.

### Theorem 5.5 — Counterfactual Incompleteness of Statistical Models
Surface-only predictors cannot enforce invariants under intervention.

### Theorem 5.6 — State-Projection No-Go Theorem
No non-injective projection from histories to states preserves admissibility.

---

## 6. Conclusion

Spherepop Calculus provides a formally sound, counterfactually complete framework grounded in event histories rather than states. Its operators enforce structural algebra via architectural constraints rather than symbolic rules. The calculus resolves longstanding tensions between abstract cognitive structure and dynamic biological realization, offering a principled foundation for explanation in cognition, language, and intelligence.
