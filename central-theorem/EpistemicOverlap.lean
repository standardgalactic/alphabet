/-
MANIFEST: CT-000

Formalization of the Epistemic Overlap material in "The Central Theorem:
Epistemic Overlap" (v3, patched): the CT-000 core, refinement (Prop. 1.1/1.3,
Cor. 1.4), finite obstruction certificates (Thm. 1.6), the Helly reduction
(Thm. 1.9), randomized policies (patched §1.14), and policy equivalence
(Prop. 1.14, Cors. 1.15-1.16).

Scope (per paper §1.17): this file verifies only the propositions encoded here.
It does not formalize CT-001 .. CT-016.

STATUS: written without access to a Lean toolchain, so it has NOT been compiled.
Expect small repairs. The most fragile spots are marked `-- FRAGILE`:
  * `helly_reduction` depends on the exact name/signature of Mathlib's Helly
    lemma (`Convex.helly_theorem'`, in Mathlib/Analysis/Convex/Radon.lean) and on
    `Module.finrank` vs `FiniteDimensional.finrank` for your Mathlib version.
  * `lebesgue_counterexample` depends on measure-API simp lemmas.
No `sorry` is used.
-/
import Mathlib

open Set

noncomputable section

namespace EpistemicOverlap

/-- Def. 2.1: worlds `W`, observations `O`, actions `A`, observation map and
admissible-action map. -/
structure AdmStruct (W O A : Type*) where
  obs : W → O
  adm : W → Set A

namespace AdmStruct

variable {W O A : Type*} (S : AdmStruct W O A)

/-- The observation class `[o]`. -/
def cls (o : O) : Set W := {w | S.obs w = o}

/-- The common admissible-action set `C(o)`. Written as a set-builder so that
membership unfolds definitionally; `common_eq_iInter` relates it to the paper's
intersection. -/
def common (o : O) : Set A := {a | ∀ w, S.obs w = o → a ∈ S.adm w}

theorem mem_common {o : O} {a : A} :
    a ∈ S.common o ↔ ∀ w, S.obs w = o → a ∈ S.adm w := Iff.rfl

theorem common_eq_iInter (o : O) :
    S.common o = ⋂ w ∈ S.cls o, S.adm w := by
  ext a
  simp [common, cls]

/-- Realized observations `O(W)`. -/
def Realized : Type _ := {o : O // ∃ w, S.obs w = o}

/-- Def. 2.2: a deterministic policy `π : O → A` is globally admissible. -/
def GloballyAdmissible (π : O → A) : Prop := ∀ w, π (S.obs w) ∈ S.adm w

/-! ## CT-000 -/

/-- **CT-000** (total-policy version). `A` must be nonempty so that unrealized
observations can be assigned an action. Choice is Lean's `Classical.choose`. -/
theorem epistemic_overlap [Nonempty A] :
    (∃ π : O → A, S.GloballyAdmissible π) ↔
      ∀ o, (∃ w, S.obs w = o) → (S.common o).Nonempty := by
  constructor
  · rintro ⟨π, hπ⟩ o _
    refine ⟨π o, S.mem_common.mpr fun w' hw' => ?_⟩
    have h := hπ w'
    rwa [hw'] at h
  · intro h
    classical
    refine ⟨fun o => if ho : ∃ w, S.obs w = o then Classical.choose (h o ho)
                      else Classical.arbitrary A, ?_⟩
    intro w
    have hw : ∃ w', S.obs w' = S.obs w := ⟨w, rfl⟩
    simp only [dif_pos hw]
    have hspec := Classical.choose_spec (h (S.obs w) hw)
    exact S.mem_common.mp hspec w rfl

/-- Cor. 2.4 (No Safe Action). -/
theorem no_safe_action {o : O} (ho : ∃ w, S.obs w = o) (hempty : S.common o = ∅) :
    ¬ ∃ π : O → A, S.GloballyAdmissible π := by
  rintro ⟨π, hπ⟩
  obtain ⟨w, hw⟩ := ho
  have hmem : π o ∈ S.common o := S.mem_common.mpr fun w' hw' => by
    have h := hπ w'
    rwa [hw'] at h
  rw [hempty] at hmem
  simp at hmem

/-- Cor. 2.5 (two-world obstruction). -/
theorem two_world_obstruction {w w' : W} (hobs : S.obs w = S.obs w')
    (hdis : Disjoint (S.adm w) (S.adm w')) :
    ¬ ∃ π : O → A, S.GloballyAdmissible π := by
  rintro ⟨π, hπ⟩
  have h1 := hπ w
  have h2 := hπ w'
  rw [hobs] at h1
  exact Set.disjoint_left.mp hdis h1 h2

/-! ## §1.11 Refinement (Prop. 1.1 / 1.3, Cor. 1.4) -/

variable {O₁ O₂ : Type*}

/-- `S₂` refines `S₁`: same admissibility, and `obs₁ = f ∘ obs₂`. -/
def Refines (S₂ : AdmStruct W O₂ A) (S₁ : AdmStruct W O₁ A) : Prop :=
  S₁.adm = S₂.adm ∧ ∃ f : O₂ → O₁, S₁.obs = f ∘ S₂.obs

/-- Prop. 1.3: admissibility-sufficiency is upward closed under refinement. -/
theorem sufficient_of_refines {S₁ : AdmStruct W O₁ A} {S₂ : AdmStruct W O₂ A}
    (hr : Refines S₂ S₁) :
    (∃ π : O₁ → A, S₁.GloballyAdmissible π) →
      (∃ π : O₂ → A, S₂.GloballyAdmissible π) := by
  obtain ⟨hadm, f, hf⟩ := hr
  rintro ⟨π₁, h⟩
  refine ⟨π₁ ∘ f, fun w => ?_⟩
  have h1 : S₁.obs w = f (S₂.obs w) := congrFun hf w
  have hw := h w
  rw [h1, hadm] at hw
  exact hw

/-- Add a second observation to `S₁`, giving the joint observation `(O₁, O₂)`. -/
def withObs (S₁ : AdmStruct W O₁ A) (obs₂ : W → O₂) : AdmStruct W (O₁ × O₂) A :=
  ⟨fun w => (S₁.obs w, obs₂ w), S₁.adm⟩

/-- Cor. 1.4: joint observations preserve admissibility-sufficiency. -/
theorem common_refinement (S₁ : AdmStruct W O₁ A) (obs₂ : W → O₂) :
    (∃ π : O₁ → A, S₁.GloballyAdmissible π) →
      (∃ π : O₁ × O₂ → A, (S₁.withObs obs₂).GloballyAdmissible π) := by
  refine sufficient_of_refines ⟨rfl, Prod.fst, ?_⟩
  funext w
  rfl

/-! ## §1.12 Finite obstruction certificate (Thm. 1.6) -/

/-- If `A` is finite with `m` elements and `C(o) = ∅`, then at most `m` worlds
of the class `[o]` already have empty common admissible set. -/
theorem finite_obstruction [Fintype A] (o : O) (h : S.common o = ∅) :
    ∃ s : Finset W, s.card ≤ Fintype.card A ∧ (∀ w ∈ s, S.obs w = o) ∧
      ∀ a : A, ∃ w ∈ s, a ∉ S.adm w := by
  classical
  have hwit : ∀ a : A, ∃ w, S.obs w = o ∧ a ∉ S.adm w := by
    intro a
    by_contra hc
    push_neg at hc
    have ha : a ∈ S.common o := S.mem_common.mpr hc
    rw [h] at ha
    simp at ha
  choose wf hobs hna using hwit
  refine ⟨Finset.univ.image wf, ?_, ?_, ?_⟩
  · exact Finset.card_image_le.trans (le_of_eq Finset.card_univ)
  · intro w hw
    obtain ⟨a, -, rfl⟩ := Finset.mem_image.mp hw
    exact hobs a
  · intro a
    exact ⟨wf a, Finset.mem_image_of_mem wf (Finset.mem_univ a), hna a⟩

/-! ## §1.13 Helly reduction (Thm. 1.9) -/

/-- Forward direction of Thm. 1.9: trivial. -/
theorem subfamily_nonempty_of_common {o : O} (hc : (S.common o).Nonempty)
    (t : Finset W) (ht : ∀ w ∈ t, S.obs w = o) :
    (⋂ w ∈ t, S.adm w).Nonempty := by
  obtain ⟨a, ha⟩ := hc
  refine ⟨a, ?_⟩
  simp only [Set.mem_iInter]
  intro w hw
  exact S.mem_common.mp ha w (ht w hw)

end AdmStruct

section Helly

variable {W O E : Type*} [AddCommGroup E] [Module ℝ E] [FiniteDimensional ℝ E]

/-- Converse direction of Thm. 1.9 for a finite observation class, with convex
admissible sets in a finite-dimensional real vector space `E` (take
`E = EuclideanSpace ℝ (Fin d)` for `ℝ^d`; then `finrank = d`).

FRAGILE: relies on Mathlib's Helly theorem. In recent Mathlib it is
`Convex.helly_theorem'` (Mathlib/Analysis/Convex/Radon.lean):
  (h_convex : ∀ i ∈ s, Convex 𝕜 (F i))
  (h_inter : ∀ I ⊆ s, I.card ≤ finrank 𝕜 E + 1 → (⋂ i ∈ I, F i).Nonempty) :
  (⋂ i ∈ s, F i).Nonempty
Adjust the name and `finrank` namespace if your version differs. -/
theorem helly_reduction (S : AdmStruct W O E)
    (hconv : ∀ w, Convex ℝ (S.adm w)) (o : O)
    (hfin : (S.cls o).Finite)
    (hsub : ∀ t : Finset W, (∀ w ∈ t, S.obs w = o) →
      t.card ≤ Module.finrank ℝ E + 1 → (⋂ w ∈ t, S.adm w).Nonempty) :
    (S.common o).Nonempty := by
  classical
  obtain ⟨a, ha⟩ := Convex.helly_theorem' (𝕜 := ℝ) (F := S.adm)
    (s := hfin.toFinset) (fun i _ => hconv i)
    (fun I hI hcard => hsub I
      (fun w hw => (hfin.mem_toFinset.mp (hI hw) : w ∈ S.cls o)) hcard)
  refine ⟨a, S.mem_common.mpr fun w hw => ?_⟩
  exact Set.mem_iInter₂.mp ha w (hfin.mem_toFinset.mpr hw)

end Helly

namespace AdmStruct

variable {W O A : Type*} (S : AdmStruct W O A)

/-! ## §1.14 Randomized policies (patched version) -/

section Random

variable [MeasurableSpace A]

/-- A randomized observation-based policy. -/
structure RandPolicy (O A : Type*) [MeasurableSpace A] where
  μ : O → MeasureTheory.Measure A
  isProb : ∀ o, MeasureTheory.IsProbabilityMeasure (μ o)

variable {S}

/-- Pointwise almost-sure admissibility. -/
def PointwiseAS (S : AdmStruct W O A) (ρ : RandPolicy O A) : Prop :=
  ∀ w, ρ.μ (S.obs w) (S.adm w) = 1

/-- Robust almost-sure admissibility. -/
def RobustAS (S : AdmStruct W O A) (ρ : RandPolicy O A) : Prop :=
  ∀ o, (∃ w, S.obs w = o) →
    MeasurableSet (S.common o) ∧ ρ.μ o (S.common o) = 1

/-- Robust implies pointwise. -/
theorem robust_imp_pointwise {ρ : RandPolicy O A} (hρ : RobustAS S ρ) :
    PointwiseAS S ρ := by
  intro w
  haveI := ρ.isProb (S.obs w)
  have hsub : S.common (S.obs w) ⊆ S.adm w :=
    fun a ha => S.mem_common.mp ha w rfl
  have h1 := (hρ (S.obs w) ⟨w, rfl⟩).2
  exact le_antisymm MeasureTheory.prob_le_one
    ((le_of_eq h1.symm).trans (MeasureTheory.measure_mono hsub))

/-- Robust almost-sure admissibility forces `C(o) ≠ ∅` at every realized `o`. -/
theorem robust_nonempty {ρ : RandPolicy O A} (hρ : RobustAS S ρ) {o : O}
    (ho : ∃ w, S.obs w = o) : (S.common o).Nonempty := by
  obtain ⟨_, h1⟩ := hρ o ho
  by_contra hne
  rw [Set.not_nonempty_iff_eq_empty] at hne
  rw [hne] at h1
  simp at h1

/-- Countable classes: pointwise almost-sure admissibility implies robust. -/
theorem pointwise_imp_robust_of_countable {ρ : RandPolicy O A}
    (hmeas : ∀ w, MeasurableSet (S.adm w))
    (hcount : ∀ o, (S.cls o).Countable)
    (hρ : PointwiseAS S ρ) : RobustAS S ρ := by
  intro o _
  haveI := ρ.isProb o
  have hmc : MeasurableSet (S.common o) := by
    rw [S.common_eq_iInter]
    exact MeasurableSet.biInter (hcount o) (fun w _ => hmeas w)
  refine ⟨hmc, ?_⟩
  have hc : (S.common o)ᶜ = ⋃ w ∈ S.cls o, (S.adm w)ᶜ := by
    rw [S.common_eq_iInter, Set.compl_iInter₂]
  have hnull : ρ.μ o (S.common o)ᶜ = 0 := by
    rw [hc, MeasureTheory.measure_biUnion_null_iff (hcount o)]
    intro w hw
    have hwo : S.obs w = o := hw
    have h1 := hρ w
    rw [hwo] at h1
    exact (MeasureTheory.prob_compl_eq_zero_iff (hmeas w)).mpr h1
  exact (MeasureTheory.prob_compl_eq_zero_iff hmc).mp hnull

/-- Hence on countable classes, `C(o) = ∅` rules out pointwise admissibility. -/
theorem no_pointwise_of_empty_common {ρ : RandPolicy O A}
    (hmeas : ∀ w, MeasurableSet (S.adm w))
    (hcount : ∀ o, (S.cls o).Countable)
    {o : O} (ho : ∃ w, S.obs w = o) (hempty : S.common o = ∅) :
    ¬ PointwiseAS S ρ := by
  intro hρ
  have := robust_nonempty (pointwise_imp_robust_of_countable hmeas hcount hρ) ho
  rw [hempty] at this
  simp at this

end Random

end AdmStruct

/-- The uncountable counterexample: pointwise almost-sure admissibility without
any common admissible action. `A = W = ℝ`, `Adm(w) = {w}ᶜ`, and `ρ` is Lebesgue
measure restricted to `[0,1]`.

FRAGILE: the `simp` calls depend on the measure API of your Mathlib version. -/
theorem lebesgue_counterexample :
    ∃ (S : AdmStruct ℝ Unit ℝ) (ρ : AdmStruct.RandPolicy Unit ℝ),
      AdmStruct.PointwiseAS S ρ ∧ S.common () = ∅ := by
  have hprob : MeasureTheory.IsProbabilityMeasure
      (MeasureTheory.volume.restrict (Set.Icc (0 : ℝ) 1)) :=
    ⟨by simp⟩
  refine ⟨⟨fun _ => (), fun w => ({w} : Set ℝ)ᶜ⟩,
          ⟨fun _ => MeasureTheory.volume.restrict (Set.Icc (0 : ℝ) 1),
           fun _ => hprob⟩, ?_, ?_⟩
  · intro w
    haveI := hprob
    refine (MeasureTheory.prob_compl_eq_zero_iff
      (measurableSet_singleton w).compl).mp ?_
    simp
  · ext a
    simp only [AdmStruct.common, Set.mem_setOf_eq, Set.mem_empty_iff_false, iff_false]
    intro h
    have := h a rfl
    simp at this

namespace AdmStruct

variable {W O A : Type*} (S : AdmStruct W O A)

/-! ## §1.15 Policy equivalence (Prop. 1.14, Cors. 1.15, 1.16) -/

/-- A realized-observation policy is globally admissible. -/
def RealizedAdmissible (π : S.Realized → A) : Prop :=
  ∀ w, π ⟨S.obs w, w, rfl⟩ ∈ S.adm w

/-- **Prop. 1.14**: globally admissible realized-observation policies are
`∏_{o ∈ O(W)} C(o)`. -/
def policyEquiv :
    {π : S.Realized → A // S.RealizedAdmissible π} ≃
      ((p : S.Realized) → S.common p.1) where
  toFun π p := ⟨π.1 p, S.mem_common.mpr fun w hw => by
    have hp : (⟨S.obs w, w, rfl⟩ : S.Realized) = p := Subtype.ext hw
    have h := π.2 w
    rw [hp] at h
    exact h⟩
  invFun c := ⟨fun p => (c p).1, fun w =>
    S.mem_common.mp (c ⟨S.obs w, w, rfl⟩).2 w rfl⟩
  left_inv π := by
    apply Subtype.ext
    rfl
  right_inv c := by
    funext p
    apply Subtype.ext
    rfl

/-- Helper policy: take value `x` at the realized observation `o`, and an
arbitrary element of `C(·)` elsewhere. -/
open Classical in
def patch (hne : ∀ o, (∃ w, S.obs w = o) → (S.common o).Nonempty)
    (o : O) (x : A) : S.Realized → A :=
  fun q => if q.1 = o then x else Classical.choose (hne q.1 q.2)

theorem patch_admissible (hne : ∀ o, (∃ w, S.obs w = o) → (S.common o).Nonempty)
    {o : O} {x : A} (hx : x ∈ S.common o) :
    S.RealizedAdmissible (S.patch hne o x) := by
  classical
  intro w
  by_cases hw : S.obs w = o
  · simp only [patch]
    rw [if_pos hw]
    exact S.mem_common.mp hx w hw
  · simp only [patch]
    rw [if_neg hw]
    exact S.mem_common.mp (Classical.choose_spec (hne (S.obs w) ⟨w, rfl⟩)) w rfl

/-- **Cor. 1.15** (uniqueness). Assuming every `C(o)` is nonempty (so that an
admissible policy exists), the admissible policy is unique iff every `C(o)` has
at most one element. -/
theorem policy_unique_iff
    (hne : ∀ o, (∃ w, S.obs w = o) → (S.common o).Nonempty) :
    (∀ π₁ π₂ : S.Realized → A, S.RealizedAdmissible π₁ →
        S.RealizedAdmissible π₂ → π₁ = π₂) ↔
      ∀ o, (∃ w, S.obs w = o) → (S.common o).Subsingleton := by
  constructor
  · intro h o ho a ha b hb
    have h12 := h (S.patch hne o a) (S.patch hne o b)
      (S.patch_admissible hne ha) (S.patch_admissible hne hb)
    have := congrFun h12 ⟨o, ho⟩
    classical
    simpa [patch] using this
  · intro h π₁ π₂ h₁ h₂
    funext p
    exact h p.1 p.2 (S.policyEquiv ⟨π₁, h₁⟩ p).2 (S.policyEquiv ⟨π₂, h₂⟩ p).2

/-- **Cor. 1.16** (policy count). With finitely many realized observations,
the number of admissible realized-observation policies is `∏ |C(o)|`. -/
theorem policy_count [Fintype S.Realized] :
    Nat.card {π : S.Realized → A // S.RealizedAdmissible π} =
      ∏ p : S.Realized, Nat.card (S.common p.1) := by
  rw [Nat.card_congr S.policyEquiv]
  exact Nat.card_pi

end AdmStruct

end EpistemicOverlap

end

