# A Constraint-First Theory of Intelligence: Event Histories, Counterfactual Control, and the Architectural Limits of Statistical Models

Contemporary theories of intelligence increasingly rely on abstract structural principles to guide explanation, yet practice in both artificial intelligence and cognitive neuroscience remains dominated by state-based models and correlational criteria. This paper argues for a fundamental reorientation, proposing that intelligence is best understood not as a static representational capacity, but as a process of construction under constraint, grounded in irreversible event histories. On this view, a genuine explanation does not predict a system's state but specifies the counterfactual robustness of its structural invariants—what would remain constant under perturbation. We develop a formal event-based framework where hierarchical structure and abstract operations emerge from the equivalence classes and admissibility constraints of these histories. This framework reinterprets neural dynamics as a form of perceptual control, where the brain acts to stabilize lawful history structures across multiple measurement scales. We then apply this constraint-first theory to contemporary large language models (LLMs). We argue that the statistical, state-based nature of LLMs renders them architecturally incapable of enforcing the structural invariants that define genuine intelligence. By operating solely on the surface projections of language, they lack the authoritative event history and control mechanisms required for counterfactual reasoning, lawful transfer, and structural refusal. Ultimately, they are counterfactually incomplete, a limitation that cannot be overcome by scale alone.

---

## 1. Introduction

The field of artificial intelligence is currently defined by the remarkable predictive performance of large language models (LLMs). These systems demonstrate an unprecedented ability to generate fluent, contextually relevant text, leading to successes on a wide range of benchmarks. Yet, this success is shadowed by a pattern of systematic failures. LLMs struggle to respect higher-order structural constraints, reason causally, and evaluate counterfactual scenarios in a principled way. This tension suggests a fundamental architectural mismatch between these statistical models and the nature of biological intelligence.

This paper advances the thesis that a coherent theory of intelligence requires a shift in ontology, moving from state-based, performance-oriented explanations to an event-first, constraint-based framework. We define intelligence not as a collection of skills or the ability to occupy specific representational states, but as the capacity for construction under constraint. This view emphasizes the primacy of irreversible event histories, the preservation of structural invariants across transformations, and the enforcement of boundaries as a constitutive cognitive act. Intelligence, in this framework, is defined not by what a system can do, but by the constraints it can coherently preserve over time.

## 2. A Theory of Intelligence as Construction Under Constraint

### 2.1 The Primacy of Events Over States

Prevailing computational models of cognition are overwhelmingly state-based. A system's identity at any moment is captured by an internal configuration—a vector of parameters, an activation pattern, or a symbolic representation. However, a state is always a summary that collapses the construction history required to understand its persistence and potential for generalization. Two systems may occupy identical states yet possess radically different capacities for future action if they arrived there via different historical paths.

We propose that the fundamental object of analysis must be the construction history: an ordered, irreversible sequence of events. Each event narrows the space of future admissible constructions, accumulating constraints that define the system's identity. Within this framework, memory is not a form of storage but the replayability of this history—the capacity to reconstruct how a structure came to be.

### 2.2 Abstraction as Invariant Preservation

In a state-based view, abstraction is often treated as representational simplification. In an event-first framework, abstraction is redefined as the identification of structures that remain invariant under a specified family of lawful transformations acting on construction histories.

An abstraction is justified not by its compactness, but by what it survives. It is a commitment to ignore certain distinctions while preserving others, and this commitment is intelligible only when tied to the conditions of its own validity.

### 2.3 Generality as Lawful Transfer

Generality is frequently mistaken for breadth of performance. We propose a more rigorous definition: generality is the capacity for lawful transfer.

A lawful transfer is the transformation of a construction history from one context to another while preserving the invariants required for its validity. A system is general not because it can act everywhere, but because it can reliably distinguish where its constructions apply and where they must be withheld.

### 2.4 The Necessity of Boundaries and Refusal

Modularity is not an engineering convenience but an ontological requirement.

- **Modules** are locally coherent domains, each with its own independent construction history.
- **Interfaces** declare jurisdiction and regulate admissible transformations.

This architecture necessitates **refusal**: the structural non-existence of an admissible transformation between a proposal and preserved invariants. A system that cannot refuse cannot learn without dissolving its own structure.

## 3. The Mechanism of Intelligence: Counterfactual Control and Neural Dynamics

### 3.1 Explanation via Counterfactual Robustness

Explanation requires counterfactual robustness—the properties that remain invariant under intervention. In an event-first framework, causal graphs are abstractions over admissible histories, and explanation specifies which invariants survive graph surgery.

### 3.2 Neural Dynamics as Perceptual Control Systems

Neural systems function as perceptual control systems whose control variables are structural invariants. The brain acts to preserve lawful history structure under perturbation rather than representing symbols.

Projection inconsistencies generate error signals (e.g., N400, P600) that drive adaptive dynamics to restore invariant structure.

### 3.3 ROSE as Multiscale History Projections

ROSE can be reinterpreted as projection maps from a single event history:

- **R**: micro-scale event projections
- **O**: meso-scale compositional schemas
- **S**: stabilized invariant structures
- **E**: macro-scale global coordination

## 4. Architectural Critique of Large Language Models

### 4.1 LLMs as Surface Projection Optimizers

LLMs optimize surface conditional probabilities without access to generative histories or admissibility constraints. They model projections, not processes.

### 4.2 Absence of History Semantics

Without a replayable event log, LLMs cannot evaluate counterfactual admissibility. This absence is architectural, not remediable by scale.

### 4.3 Failure to Enforce Algebraic Invariants

LLMs approximate algebraic constraints statistically but cannot enforce irreversible commitments (e.g., nonassociativity) as inviolable structure.

### 4.4 Why Correlation Is Not Explanation

Correlations between model activations and neural data reflect shared projections, not shared mechanisms. Explanation requires counterfactual competence.

## 5. Conclusion

This work argues for a constraint-first, event-based theory of intelligence. Intelligence is defined by the structural invariants a system can preserve under perturbation, not by predictive success. Statistical models are counterfactually incomplete because they lack authoritative history and control mechanisms. The path forward lies in architectures that ground meaning in replayable construction and enforce lawful refusal.
