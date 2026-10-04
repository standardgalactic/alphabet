# The Central Theorem: Epistemic Overlap

This document defines the claim registry and formal statements associated with the Central Theorem. The accompanying mathematical development is given in `theorem.tex`.

Claims are identified by stable `CT-###` identifiers. Formalizations, implementations, tests, and related documents may reference these identifiers without duplicating the claims themselves.

The registry distinguishes mathematical statements from formalizations and implementations. A proof, a machine-checked formalization, and an implementation are different forms of evidence and are recorded separately where relevant.

## 0. Specification structure

The specification consists of the following components:

| Component | Role |
|---|---|
| `SPEC.md` | Claim definitions, identifiers, dependencies, and status |
| `theorem.tex` | Mathematical exposition and proofs |
| Implementation manifests | References from formalizations, implementations, and tests to registered claims |

### Claim manifests

Implementation or formalization files may contain a `MANIFEST:` header listing the `CT-###` identifiers to which they correspond.

The registry in this document defines the valid identifier set. Manifest validation enforces a simple invariant:

> Every `CT-###` identifier declared by a manifest must exist in the claim registry.

The converse is not required. A registered claim may have no implementation manifest, particularly when it is mathematical or expository rather than operational.

The validation script is `.github/claim_manifest_sync.py`. Continuous integration may invoke the same check through `.github/workflows/claim-manifest-sync.yml`.

Git provides revision history, commit identity, timestamps, and content hashes. The manifest mechanism does not duplicate those functions. It records only the semantic correspondence between artifacts and claims.

### Source correspondence

| Source | Relevant material | Claims |
|---|---|---|
| `Admissible Histories.tex` | §§2–5 | CT-001–CT-005 |
| `Never-Predict-Noise.tex` | Tangent-normal decomposition; off-manifold analysis; coherence and curvature | CT-006–CT-009 |
| `Against_Indiscriminate_Visibility.tex` | Assumptions A1–A4; visibility bounds; local stress and scaling arguments | CT-010–CT-014 |
| `resources/admissible-continuation.tex` | Admissible-continuation analysis | CT-000, CT-003 |
| `physics/cosmology/admissible-geometry.tex` | Admissible geometry | CT-006 |

## 1. Central Theorem

### CT-000 — Epistemic Overlap

Let:

- `W` be a set of worlds representing possible system configurations;
- `𝒪` be a set of observations;
- `𝒜` be a set of actions;
- `O : W → 𝒪` be an observation map;
- `Adm : W → 𝒫(𝒜)` assign to each world its set of admissible actions;
- `π : 𝒪 → 𝒜` be a deterministic policy defined on observations.

For an observation `o`, define its observation class

`[o] = { w ∈ W | O(w) = o }`.

A policy is globally admissible when

`∀w ∈ W, π(O(w)) ∈ Adm(w)`.

#### Theorem

Subject to the required choice conditions, a globally admissible observation-based policy exists if and only if every nonempty observation class has at least one action admissible in every world belonging to that class:

`∀o ∈ O(W), ⋂_{w ∈ [o]} Adm(w) ≠ ∅`.

#### Proof

Suppose first that every observation class has a nonempty common admissible-action set. For each observation `o ∈ O(W)`, choose

`a_o ∈ ⋂_{w ∈ [o]} Adm(w)`

and define

`π(o) = a_o`.

Then for every `w ∈ W`,

`π(O(w)) ∈ Adm(w)`,

so `π` is globally admissible.

Conversely, suppose a globally admissible policy `π` exists. For any observation `o ∈ O(W)` and every `w ∈ [o]`,

`π(o) = π(O(w)) ∈ Adm(w)`.

Therefore

`π(o) ∈ ⋂_{w ∈ [o]} Adm(w)`,

so the intersection is nonempty.

The finite or decidable version requires only finite choice. More general formulations require the corresponding choice assumption.

#### Corollary — No Safe Action

If some observation class has empty common admissible-action intersection,

`∃o ∈ O(W) : ⋂_{w ∈ [o]} Adm(w) = ∅`,

then no policy depending only on `o` can guarantee an admissible action in every world represented by that observation.

A useful two-world special case is:

`O(w) = O(w′)`

and

`Adm(w) ∩ Adm(w′) = ∅`.

Under these conditions, no deterministic observation-based policy can be admissible in both worlds.

The obstruction is informational. The observation map has identified worlds for which different actions are required.

### Interpretation

CT-000 separates two questions that are often conflated.

The first is whether an action is admissible in a particular world. The second is whether the information available to an agent is sufficient to select an action guaranteed to be admissible in the actual world.

Even when every individual world admits one or more actions, an observation-based policy may fail to exist because the observation map collapses distinctions relevant to admissibility.

This result supplies the common formal structure used by the claims below. It does not by itself establish the stronger domain-specific interpretations attached to those claims.

## 2. Claim registry

| ID | Claim | Status |
|---|---|---|
| CT-000 | Epistemic Overlap and No-Safe-Action corollary | proved |
| CT-001 | Admissibility is independent of valuation | established within the stated model |
| CT-002 | Prefix closure of admissible histories | established within the stated model |
| CT-003 | Unique continuation under a committed prefix | established within the stated model |
| CT-004 | Persistence of disfavored admissible trajectories | conjectural / qualitative |
| CT-005 | Pruning excludes continuations rather than repairing prior states | established within the stated model |
| CT-006 | Tangent-normal decomposition as a model of admissible transformation | standard geometric result plus modeling assumption |
| CT-007 | Off-manifold generation can increase effective support dimension | conditional |
| CT-008 | Local-chart coherence and tangent-flow interpretation | modeling correspondence |
| CT-009 | Local admissibility does not by itself guarantee global coherence | established as a general caution; geometric form model-dependent |
| CT-010 | Bounded correction cannot guarantee stability under unbounded visibility under A1–A4 | conditional theorem |
| CT-011 | Finite safe envelope under bounded protective capacity | conditional corollary |
| CT-012 | Superlinear risk growth under the specified visibility model | model-dependent |
| CT-013 | Local stress criterion for semantic stability | model-dependent |
| CT-014 | Scaling formulation of visibility-induced instability | model-dependent |
| CT-015 | Admissibility may factor through a minimal decision-relevant history | formalizable structural property |
| CT-016 | Durable adjudication must be distinguished from visible client state | implementation principle |

## 3. Claim statements

### CT-001 — Admissibility and valuation

Let `ℋ` be the set of histories permitted by a system's transition rules, and let

`V : ℋ → ℝ`

be a valuation on those histories.

When admissibility is defined solely by membership in `ℋ`, changing `V` does not change whether a history is admissible:

`h ∈ ℋ`

is independent of the value assigned to `V(h)`.

This distinction separates structural possibility from preference. A permitted history need not be desirable, rewarded, or intended.

Source: `Admissible Histories.tex`, §3.

### CT-002 — Prefix closure

Assume the admissible-history set `ℋ` is prefix-closed. Then

`h = (x₀, …, x_T) ∈ ℋ`

implies

`h_{≤t} ∈ ℋ`

for every `t ≤ T`.

Thus every prefix of an admissible history is itself an admissible partial history.

Prefix closure is an explicit property of the model rather than a property of arbitrary transition systems.

Source: `Admissible Histories.tex`, §2.

### CT-003 — Commitment and unique continuation

Let `p = h_{≤t}` be an admissible prefix. If the transition constraints determine a unique admissible continuation from `p`, then any incompatible extension of `p` is inadmissible.

Formally, if `h` is the unique member of `ℋ` extending `p` through the relevant horizon, then any `h′` sharing `p` but differing from `h` after `t` is not an admissible continuation.

The term *commitment* refers here to the reduction of the admissible continuation set, potentially to a singleton.

Source: `Admissible Histories.tex`, §2.

### CT-004 — Persistence of disfavored admissible trajectories

The motivating model suggests that systems with sparse connectivity, competitive dynamics, and incremental weight adjustment may retain trajectories that are structurally admissible despite receiving unfavorable valuation.

The strong claim that such trajectories are inevitable in every sufficiently complex system is not established here. CT-004 is therefore retained as a qualitative hypothesis requiring a more explicit dynamical model.

Source: `Admissible Histories.tex`, §4.

### CT-005 — Pruning intervention

Let

`D : prefixes → {0,1}`

be a detection rule and define

`ℋ′ = { h ∈ ℋ | D(h_{≤t}) = 0 }`.

The intervention changes the set of permitted continuations by excluding histories selected by `D`. It does not retroactively alter the states already present in a prefix.

Under additional assumptions connecting `D` to a valuation `V`, such pruning may increase the proportion of positively valued histories among the remaining histories. That improvement is conditional on the detector's selectivity and the underlying distribution.

The general structural point is simpler: pruning acts by restricting future continuation.

Source: `Admissible Histories.tex`, §5.

### CT-006 — Tangent and normal components

For a smooth embedded submanifold

`M ⊂ ℝⁿ`

and `x ∈ M`, the ambient tangent space decomposes orthogonally as

`ℝⁿ = T_xM ⊕ N_xM`.

Accordingly, any ambient update vector `v` can be written

`v = v_T + v_N`

with

`v_T ∈ T_xM`

and

`v_N ∈ N_xM`.

The associated admissibility model identifies tangent motion with locally structure-preserving motion and treats a nonzero normal component as departure from the modeled constraint manifold.

The decomposition itself is standard differential geometry. Its interpretation as semantic or computational admissibility is an additional modeling assumption.

Source: `Never-Predict-Noise.tex`, tangent-normal decomposition.

Related discussion: `physics/cosmology/admissible-geometry.tex`.

### CT-007 — Off-manifold generation

Within the geometric model of CT-006, persistent normal components can move generated trajectories away from the modeled admissible manifold.

Under suitable regularity, rank, and measure assumptions, such departures may enlarge the effective support occupied by generated outputs relative to the original `d`-dimensional manifold.

The stronger statement that every generator with a nonzero normal component necessarily produces support of Hausdorff dimension greater than `d` requires additional hypotheses and is not asserted without them.

The term *off-manifold* therefore denotes departure from the modeled constraint surface; it should not be read as a universal mathematical characterization of hallucination.

Source: `Never-Predict-Noise.tex`, off-manifold analysis.

### CT-008 — Local coherence

Suppose a modeled state space is covered by local charts

`φ_i : U_i → ℝ^d`.

A globally coherent representation requires compatible descriptions on chart overlaps. This provides a useful mathematical analogy for systems in which locally computed representations must agree where their domains overlap.

Likewise, projected gradient updates of the form

`x_{t+1} = x_t - η Π_{T_{x_t}M} ∇ℒ(x_t)`

provide a tangent-flow model for locally constrained optimization.

These correspondences are modeling devices. They do not imply that an arbitrary attention mechanism literally implements a sheaf or that an arbitrary Transformer layer performs the displayed tangent-flow update.

Source: `Never-Predict-Noise.tex`, local-chart and tangent-flow discussion.

### CT-009 — Local versus global coherence

Local admissibility does not in general imply global admissibility.

In geometric settings, repeated locally acceptable approximations may accumulate error over a long trajectory. Curvature, discretization, imperfect projection, or inconsistent local descriptions can therefore produce global deviation even when individual steps satisfy a local criterion.

This is the geometric analogue of the distinction expressed by CT-000: local availability of admissible actions is insufficient unless the local choices are mutually compatible under the relevant information and composition structure.

Source: `Never-Predict-Noise.tex`, curvature-accumulation discussion.

### CT-010 — Bounded correction under increasing visibility

Consider a model with visibility `Φ`, interpretive flow `v`, reputational or semantic disorder `S`, and protective capacity `P`.

Assume:

`A1.` Entropy or disorder production satisfies

`∂S/∂t ≥ α|v|² - βC`

for `α > 0`.

`A2.` Flow is bounded below by visibility gradients:

`|v| ≥ c₁|∇Φ|`.

`A3.` Increasing visibility produces unbounded aggregate interaction gradients:

`∫ |∇Φ|² dx → ∞`

in the specified scaling limit.

`A4.` Corrective capacity is bounded:

`C(x,t) ≤ C_max < ∞`.

Under these assumptions, sufficiently increasing visibility eventually makes the positive production term dominate bounded correction. Consequently, a fixed bounded protective envelope cannot be guaranteed for arbitrarily large visibility.

This is a conditional result. Its applicability depends on A1–A4 and on the interpretation of the modeled quantities.

Source: `Against_Indiscriminate_Visibility.tex`, no-go argument.

### CT-011 — Finite safe envelope

Under the assumptions of CT-010 and bounded protective capacity, stability can be guaranteed only over a bounded visibility regime.

Equivalently, the model admits some finite limiting scale beyond which its safety inequality cannot be maintained solely by the bounded corrective mechanism.

This does not imply a universal numerical visibility threshold. The bound depends on the parameters and structure of the model.

Source: `Against_Indiscriminate_Visibility.tex`, finite-envelope corollary.

### CT-012 — Risk growth

Within the visibility model, interaction terms may grow faster than the directly controlled corrective terms. Where the assumed scaling laws produce increasing marginal disorder with visibility, risk is correspondingly superlinear over that regime.

This is a property of the specified model and its scaling assumptions, not a general law that all forms of visibility or communication exhibit superlinear risk.

Source: `Against_Indiscriminate_Visibility.tex`, risk-growth discussion.

### CT-013 — Local stress criterion

The field model decomposes local semantic stress into coherence-preserving and contradiction-producing contributions.

For a region `U`, a sufficient local stability criterion can be expressed schematically as

`|∇·Θ_φ| ≥ |∇·Θ_{S,Φ}|`,

where `Θ_φ` represents the modeled coherence contribution and `Θ_{S,Φ}` the modeled contradiction or visibility-induced contribution.

The criterion belongs to the field model and should be interpreted relative to its definitions rather than as a general physical stress law.

Source: `Against_Indiscriminate_Visibility.tex`, local-stress analysis.

### CT-014 — Scaling formulation

The visibility model can also be expressed in terms of scale dependence. If visibility grows under rescaling as

`Φ_ℓ ~ ℓ^{Δ_Φ}`

with `Δ_Φ > 0`, while the associated disorder term grows more rapidly, a dimensionless stability ratio may decrease with scale.

Under those assumptions, a configuration stable at one scale need not remain stable at arbitrarily larger scales.

The language of relevant operators and renormalization is used here as a mathematical scaling framework. The claim depends on the specified scaling relations and does not assert that visibility is universally a renormalization-group operator in the physical sense.

Source: `Against_Indiscriminate_Visibility.tex`, scaling and renormalization discussion.

### CT-015 — Minimal decision-relevant history

An admissibility decision need not depend on the complete recorded history if the admissibility predicate factors through a smaller state summary.

Let

`q : H → M`

map complete histories to a decision-relevant state `M`.

If there exists

`Adm_M : M → 𝒫(𝒜)`

such that

`Adm(h) = Adm_M(q(h))`

for all relevant histories `h`, then `q(h)` is sufficient for the admissibility decision.

The minimality of such a representation is a separate question. In an implementation it may consist, for example, of the last attested state, a monotone sequence position, and other information required to determine legal continuation.

CT-015 formalizes the distinction between complete provenance and the smaller state required for a particular decision.

Source: `Admissible Histories.tex`, §§2–3.

### CT-016 — Durable adjudication

Visible client state and authoritative adjudication are distinct.

In systems where refusals affect subsequent legal continuation, a refusal must be represented durably if later decisions are to depend on its occurrence. Recording only successful state transitions can otherwise erase information relevant to future admissibility.

A ledger implementation may therefore assign a monotone position to both admissions and refusals while keeping submitted client sequence information distinct from authoritative committed sequence information.

This is an implementation principle motivated by the continuation model rather than an independent mathematical theorem.

Its central invariant is:

> Decisions that alter the set of legal future continuations must survive reconstruction of the authoritative state.

An implementation can test this property by rebuilding state from its durable log and verifying that previously adjudicated events retain the same disposition.

## 4. Status and scope

CT-000 is the central mathematical statement of this specification. Its content is deliberately modest: observation-based control is possible exactly when observational equivalence classes retain a common admissible action.

CT-001–CT-005 specify properties of the admissible-history model. Some are definitions or consequences of explicit assumptions rather than universal propositions about arbitrary dynamical systems.

CT-006–CT-009 provide a geometric formulation of local and global admissibility. Standard geometric facts are distinguished from their use as models of semantic or computational behavior.

CT-010–CT-014 concern a particular visibility-and-correction model. Their conclusions are conditional on the assumptions and scaling relations stated in that model.

CT-015 expresses a factorization property for admissibility decisions. CT-016 records an operational consequence relevant to implementations that reconstruct authoritative state from durable history.

Formal verification of one claim does not automatically verify another claim merely because the claims are conceptually related. Likewise, an implementation that exhibits behavior corresponding to a claim is evidence of implementation correspondence, not a mathematical proof of the general claim.

## 5. Compatibility constraints

Existing formalizations and implementations may use this registry without being treated as complete implementations of the entire specification.

A formalization should identify exactly which `CT-###` statements it establishes. An implementation should identify exactly which claims its behavior is intended to realize or test.

Existing artifacts used for independent experiments or mutation studies need not be modified merely to conform to this specification.

Where an implementation has an established serialized representation, transition rule, or replay invariant, adoption of the claim registry does not by itself authorize changes to that behavior.

The mathematical exposition, formal verification, and operational implementation should therefore remain separable. Correspondence between them is explicit through claim identifiers rather than inferred from repository location, naming, or shared terminology.