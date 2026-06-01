"""
Admissibility Lab
=================
A document is not a bag of propositions but a constrained space of admissible
future queries. This module extracts inferential architecture from texts,
builds query-accessibility relations, and measures load-bearing structure
through point-load and distributed-load perturbation.

Taxonomy of components:
  Anchor            — high local curvature (removal destroys accessibility)
  Distributed Anchor — low local curvature per instance, high aggregate curvature
  Ghost Commitment  — formally load-bearing but compression-robust (recoverable)
  Decoration        — low local and aggregate curvature, compression-robust
"""

import re
import json
import math
import hashlib
from copy import deepcopy
from dataclasses import dataclass, field
from collections import defaultdict
from typing import Optional


# ---------------------------------------------------------------------------
# Inferential cue lexicons
# ---------------------------------------------------------------------------

UNIVERSAL_CUES = {
    "conditional":   ["if", "then", "unless", "provided that", "only if",
                      "given that", "in case", "assuming"],
    "causal":        ["because", "therefore", "thus", "hence", "since",
                      "it follows that", "consequently", "as a result"],
    "contrastive":   ["however", "but", "yet", "although", "even though",
                      "contrary to", "despite", "nevertheless", "whereas"],
    "alternative":   ["alternatively", "instead", "rather", "or", "either"],
    "objection":     ["one might object", "one could argue", "a critic might",
                      "this fails when", "a counterexample", "the problem is"],
    "dependency":    ["requires", "depends on", "this follows from",
                      "presupposes", "entails", "implies", "necessitates"],
    "supposition":   ["suppose", "assume", "consider", "imagine", "let us say",
                      "hypothetically"],
    "negation_test": ["without", "absent", "if not", "were it not for",
                      "remove", "eliminating"],
}

DOMAIN_CUES = {
    "legal":      ["provided that", "notwithstanding", "subject to",
                   "in the event that", "shall", "must not", "except where"],
    "scientific": ["we assume", "we hypothesize", "data suggest",
                   "evidence indicates", "it follows that", "contrary to",
                   "we observe"],
    "rfc":        ["MUST", "MUST NOT", "SHOULD", "SHALL", "MAY",
                   "if and only if", "is required to", "is prohibited"],
    "philosophy": ["necessarily", "it is possible that", "one might argue",
                   "this entails", "this presupposes", "the claim is",
                   "we are committed to"],
}

# Query templates derived from cue types
QUERY_TEMPLATES = {
    "conditional":   ["What if {antecedent} is false?",
                      "Under what conditions does {consequent} fail?",
                      "What alternatives to {antecedent} were considered?"],
    "causal":        ["Why does {effect} follow?",
                      "Could {effect} occur without {cause}?",
                      "What other causes might produce {effect}?"],
    "contrastive":   ["How are {a} and {b} reconciled?",
                      "Which takes priority when {a} and {b} conflict?"],
    "alternative":   ["Why was {alt} not chosen?",
                      "Under what conditions would {alt} be preferable?"],
    "objection":     ["Is the objection answered?",
                      "What assumptions does the objection target?"],
    "dependency":    ["What fails if {dependency} is removed?",
                      "Is {dependency} strictly necessary or merely sufficient?"],
    "supposition":   ["What changes if the supposition is relaxed?",
                      "How much of the argument survives without the supposition?"],
    "negation_test": ["What is lost when {target} is absent?",
                      "Is {target} recoverable from context?"],
}


# ---------------------------------------------------------------------------
# Data structures
# ---------------------------------------------------------------------------

@dataclass
class Component:
    """A passage, claim, definition, or premise extracted from a document."""
    id: str
    text: str
    cue_type: str
    sentence_indices: list[int]
    concept_cluster: Optional[str] = None
    # Edge-wise curvature: query_class_id -> curvature float
    curvature_profile: dict = field(default_factory=dict)
    local_curvature: float = 0.0       # max over query classes
    aggregate_curvature: float = 0.0   # filled by batch perturbation
    survives_extractive: bool = True
    survives_abstractive: bool = True
    taxonomy: str = "Decoration"       # assigned after analysis


@dataclass
class QueryClass:
    """A class of future queries licensed by inferential structure."""
    id: str
    template: str
    cue_type: str
    licensed_by: list[str] = field(default_factory=list)   # component ids
    blocked_by: list[str] = field(default_factory=list)
    depends_on: list[str] = field(default_factory=list)
    base_accessibility: float = 1.0
    current_accessibility: float = 1.0


@dataclass
class AccessibilityRelation:
    """
    The core data structure: maps (component_id, query_class_id) -> curvature.
    Represents a document as a constrained space of admissible future queries.
    """
    components: dict = field(default_factory=dict)   # id -> Component
    query_classes: dict = field(default_factory=dict) # id -> QueryClass
    # Edge tensor: (component_id, query_class_id) -> curvature
    curvature_tensor: dict = field(default_factory=dict)
    concept_clusters: dict = field(default_factory=dict)  # cluster -> [component_ids]
    null_baseline: float = 0.0  # mean curvature under random deletion


# ---------------------------------------------------------------------------
# Extractor
# ---------------------------------------------------------------------------

class InferentialExtractor:
    """
    Extracts inferential structure from a document using cue-word detection.
    Does not generate queries open-endedly; derives them from marked structure.
    """

    def __init__(self, domain: str = "general"):
        self.domain = domain
        self.domain_cues = DOMAIN_CUES  # full dict; domain key used in _detect_cue

    def _sentences(self, text: str) -> list[str]:
        # Simple sentence splitter — replace with NLTK if available
        text = re.sub(r'\n+', ' ', text)
        parts = re.split(r'(?<=[.!?])\s+(?=[A-Z])', text)
        return [p.strip() for p in parts if p.strip()]

    def _detect_cue(self, sentence: str) -> Optional[tuple[str, str]]:
        """Return (cue_type, matched_cue) or None."""
        s = sentence.lower()
        # Check domain cues first (more specific)
        for cue in self.domain_cues.get(self.domain, DOMAIN_CUES.get(self.domain, [])):
            if cue.lower() in s:
                return ("domain_specific", cue)
        # Universal cues
        for cue_type, cues in UNIVERSAL_CUES.items():
            for cue in cues:
                if cue.lower() in s:
                    return (cue_type, cue)
        return None

    def extract(self, text: str) -> list[Component]:
        sentences = self._sentences(text)
        components = []
        seen = set()

        for i, sent in enumerate(sentences):
            detection = self._detect_cue(sent)
            if detection is None:
                continue
            cue_type, matched_cue = detection

            # Include surrounding context (prev + next sentence)
            start = max(0, i - 1)
            end = min(len(sentences) - 1, i + 1)
            passage = " ".join(sentences[start:end + 1])

            # Deduplicate
            sig = hashlib.md5(passage[:80].encode()).hexdigest()[:8]
            if sig in seen:
                continue
            seen.add(sig)

            comp_id = f"C{len(components):04d}_{cue_type[:4]}_{sig}"
            components.append(Component(
                id=comp_id,
                text=passage,
                cue_type=cue_type,
                sentence_indices=list(range(start, end + 1)),
            ))

        return components


# ---------------------------------------------------------------------------
# Query class generator
# ---------------------------------------------------------------------------

class QueryClassGenerator:
    """
    Generates query classes from extracted components.
    Uses templates tied to cue types — no open-ended LLM generation.
    """

    def generate(self, components: list[Component]) -> list[QueryClass]:
        query_classes = []
        for comp in components:
            templates = QUERY_TEMPLATES.get(comp.cue_type, [
                "What does this passage establish?",
                "What fails if this is removed?",
            ])
            for t, template in enumerate(templates):
                qid = f"Q_{comp.id}_{t}"
                qc = QueryClass(
                    id=qid,
                    template=template,
                    cue_type=comp.cue_type,
                    licensed_by=[comp.id],
                )
                query_classes.append(qc)
        return query_classes


# ---------------------------------------------------------------------------
# Concept cluster assignment — embedding-based with fallback
# ---------------------------------------------------------------------------

def _load_embedder():
    """
    Try to load sentence-transformers (best quality).
    Falls back to TF-IDF cosine similarity if unavailable.
    Returns (embed_fn, backend_name).

    To use sentence-transformers locally:
        pip install sentence-transformers
    Any model works; 'all-MiniLM-L6-v2' is fast and accurate.
    """
    try:
        from sentence_transformers import SentenceTransformer
        model = SentenceTransformer("all-MiniLM-L6-v2")

        def embed_st(texts):
            return model.encode(texts, convert_to_numpy=True,
                                show_progress_bar=False)

        return embed_st, "sentence-transformers/all-MiniLM-L6-v2"
    except Exception:
        pass

    # Fallback: TF-IDF vectors (captures lexical overlap well for academic prose)
    from sklearn.feature_extraction.text import TfidfVectorizer

    def embed_tfidf(texts):
        import numpy as np
        vec = TfidfVectorizer(
            min_df=1,
            ngram_range=(1, 2),
            sublinear_tf=True,
            stop_words="english",
        )
        return vec.fit_transform(texts).toarray().astype(np.float32)

    return embed_tfidf, "tfidf-cosine (fallback)"


class ConceptClusterer:
    """
    Groups components by semantic similarity using embeddings.

    Clustering algorithm: agglomerative linkage over a cosine similarity
    matrix, with a configurable similarity threshold. This preserves the
    union-find structure for efficiency while using real semantic distances.

    Human-correction hook: pass a correction dict
        { component_id: cluster_label }
    to override automatic assignments for high-curvature components after
    the first analysis pass.

    Backend priority:
      1. sentence-transformers/all-MiniLM-L6-v2  (install locally)
      2. TF-IDF cosine similarity                (always available, good fallback)
    """

    def __init__(self,
                 min_cluster_size: int = 2,
                 similarity_threshold: float = 0.45,
                 human_corrections: Optional[dict] = None):
        self.min_cluster_size = min_cluster_size
        self.similarity_threshold = similarity_threshold
        self.human_corrections = human_corrections or {}
        self._embed, self.backend = _load_embedder()

    def _similarity_matrix(self, texts: list[str]):
        import numpy as np
        from sklearn.metrics.pairwise import cosine_similarity
        embeddings = self._embed(texts)
        return cosine_similarity(embeddings)

    def assign(self, components: list[Component],
               verbose: bool = True) -> dict:
        """
        Returns cluster_label -> [component_ids].
        Applies human corrections after automatic clustering.
        """
        if not components:
            return {}

        if verbose:
            print(f"    Embedding backend: {self.backend}")

        texts = [c.text for c in components]
        ids   = [c.id   for c in components]
        sim   = self._similarity_matrix(texts)

        # Union-find over similarity threshold
        parent = {cid: cid for cid in ids}

        def find(x):
            while parent[x] != x:
                parent[x] = parent[parent[x]]
                x = parent[x]
            return x

        def union(x, y):
            parent[find(x)] = find(y)

        n = len(ids)
        for i in range(n):
            for j in range(i + 1, n):
                if sim[i, j] >= self.similarity_threshold:
                    union(ids[i], ids[j])

        # Group by root
        groups = defaultdict(list)
        for cid in ids:
            groups[find(cid)].append(cid)

        # Build result, filtering by min cluster size
        comp_map = {c.id: c for c in components}
        result = {}
        for root, members in groups.items():
            if len(members) >= self.min_cluster_size:
                label = f"cluster_{root[:12]}"
                result[label] = members
                for cid in members:
                    comp_map[cid].concept_cluster = label

        # Apply human corrections (override automatic assignment)
        for cid, forced_label in self.human_corrections.items():
            if cid in comp_map:
                # Remove from old cluster
                old_label = comp_map[cid].concept_cluster
                if old_label and old_label in result:
                    result[old_label] = [x for x in result[old_label] if x != cid]
                    if not result[old_label]:
                        del result[old_label]
                # Add to forced cluster
                if forced_label not in result:
                    result[forced_label] = []
                result[forced_label].append(cid)
                comp_map[cid].concept_cluster = forced_label

        return result

    def similarity_report(self, components: list[Component]) -> list[dict]:
        """
        Returns ranked pairs by similarity — useful for deciding which
        high-curvature components need human correction.
        """
        if len(components) < 2:
            return []
        texts = [c.text for c in components]
        ids   = [c.id   for c in components]
        sim   = self._similarity_matrix(texts)
        pairs = []
        n = len(ids)
        for i in range(n):
            for j in range(i + 1, n):
                pairs.append({
                    "component_a": ids[i],
                    "component_b": ids[j],
                    "similarity": float(sim[i, j]),
                    "preview_a": texts[i][:60],
                    "preview_b": texts[j][:60],
                })
        return sorted(pairs, key=lambda p: p["similarity"], reverse=True)


# ---------------------------------------------------------------------------
# Perturbation engine
# ---------------------------------------------------------------------------

class PerturbationEngine:
    """
    Measures accessibility curvature under point-load and distributed-load removal.

    Curvature = distance(admissible_queries(original),
                         admissible_queries(with_component_removed))

    Without a full semantic model, accessibility is approximated by whether
    a query class's licensing components are still present in the document.
    """

    def _admissible_set(self, relation: AccessibilityRelation,
                        removed_ids: set) -> set:
        """Query classes with at least one licensing component still present."""
        admissible = set()
        for qid, qc in relation.query_classes.items():
            remaining_licensors = [lid for lid in qc.licensed_by
                                   if lid not in removed_ids]
            if remaining_licensors:
                admissible.add(qid)
        return admissible

    def _curvature(self, base: set, perturbed: set, total: int) -> float:
        """Normalized symmetric difference — how much did the accessible set change?"""
        if total == 0:
            return 0.0
        return len(base.symmetric_difference(perturbed)) / total

    def point_load(self, relation: AccessibilityRelation) -> AccessibilityRelation:
        """Remove each component individually; measure curvature per query class."""
        base_admissible = self._admissible_set(relation, set())
        total = len(relation.query_classes)

        for comp in relation.components.values():
            perturbed = self._admissible_set(relation, {comp.id})
            global_curve = self._curvature(base_admissible, perturbed, total)
            comp.local_curvature = global_curve

            # Edge-wise: curvature per query class
            for qid in relation.query_classes:
                was_accessible = qid in base_admissible
                still_accessible = qid in perturbed
                if was_accessible and not still_accessible:
                    relation.curvature_tensor[(comp.id, qid)] = 1.0
                    comp.curvature_profile[qid] = 1.0
                else:
                    relation.curvature_tensor[(comp.id, qid)] = 0.0
                    comp.curvature_profile[qid] = 0.0

        return relation

    def distributed_load(self, relation: AccessibilityRelation) -> AccessibilityRelation:
        """Remove all instances of each concept cluster; measure aggregate curvature."""
        base_admissible = self._admissible_set(relation, set())
        total = len(relation.query_classes)

        for cluster_label, member_ids in relation.concept_clusters.items():
            removed = set(member_ids)
            perturbed = self._admissible_set(relation, removed)
            agg_curve = self._curvature(base_admissible, perturbed, total)
            for cid in member_ids:
                if cid in relation.components:
                    relation.components[cid].aggregate_curvature = agg_curve

        # Components not in any cluster: aggregate = local
        for comp in relation.components.values():
            if comp.concept_cluster is None:
                comp.aggregate_curvature = comp.local_curvature

        return relation

    def null_baseline(self, relation: AccessibilityRelation,
                      n_samples: int = 20) -> float:
        """
        Mean curvature under random deletion of single components.
        Anchors should exceed this substantially.
        """
        import random
        ids = list(relation.components.keys())
        if not ids:
            return 0.0
        base = self._admissible_set(relation, set())
        total = len(relation.query_classes)
        curves = []
        for _ in range(n_samples):
            removed = {random.choice(ids)}
            perturbed = self._admissible_set(relation, removed)
            curves.append(self._curvature(base, perturbed, total))
        baseline = sum(curves) / len(curves) if curves else 0.0
        relation.null_baseline = baseline
        return baseline


# ---------------------------------------------------------------------------
# Compression simulation
# ---------------------------------------------------------------------------

class CompressionSimulator:
    """
    Simulates extractive and abstractive compression.

    Extractive: remove lowest-salience sentences (approximated by sentence length
    and cue-word absence — short, cue-free sentences are removed first).

    Abstractive: paraphrase by stripping inferential cues from sentences,
    approximating a model that rewrites without preserving connective structure.
    """

    def _salience(self, sent: str) -> float:
        score = len(sent.split()) / 30.0  # longer = more salient
        for cues in UNIVERSAL_CUES.values():
            for cue in cues:
                if cue in sent.lower():
                    score += 0.3
        return score

    def extractive(self, text: str, ratio: float = 0.5) -> str:
        sents = re.split(r'(?<=[.!?])\s+', text)
        scored = sorted(enumerate(sents), key=lambda x: self._salience(x[1]))
        keep_n = max(1, int(len(sents) * ratio))
        keep_indices = {i for i, _ in scored[-keep_n:]}
        return " ".join(s for i, s in enumerate(sents) if i in keep_indices)

    def abstractive(self, text: str) -> str:
        """Strip inferential cues — approximates a rewriting model."""
        result = text
        all_cues = []
        for cues in UNIVERSAL_CUES.values():
            all_cues.extend(cues)
        for cue in sorted(all_cues, key=len, reverse=True):
            result = re.sub(r'\b' + re.escape(cue) + r'\b', '', result,
                            flags=re.IGNORECASE)
        result = re.sub(r'\s+', ' ', result).strip()
        return result


# ---------------------------------------------------------------------------
# Taxonomy assignment
# ---------------------------------------------------------------------------

def assign_taxonomy(relation: AccessibilityRelation,
                    anchor_threshold: float = 0.15,
                    distributed_multiplier: float = 2.0) -> AccessibilityRelation:
    """
    Assign Anchor / Distributed Anchor / Ghost Commitment / Decoration
    based on curvature profiles and compression survival.
    """
    baseline = relation.null_baseline

    for comp in relation.components.values():
        local = comp.local_curvature
        agg = comp.aggregate_curvature
        survives = comp.survives_extractive and comp.survives_abstractive

        is_anchor = local > max(anchor_threshold, baseline * 2)
        is_dist_anchor = (not is_anchor and
                          agg > local * distributed_multiplier and
                          agg > anchor_threshold)
        is_ghost = (is_anchor or is_dist_anchor) and survives

        if is_ghost:
            comp.taxonomy = "Ghost Commitment"
        elif is_anchor:
            comp.taxonomy = "Anchor"
        elif is_dist_anchor:
            comp.taxonomy = "Distributed Anchor"
        else:
            comp.taxonomy = "Decoration"

    return relation


# ---------------------------------------------------------------------------
# Surprise detector
# ---------------------------------------------------------------------------

def find_surprises(relation: AccessibilityRelation) -> list[dict]:
    """
    Identify the four categories of unexpected findings:
      - Rare but high-curvature (small footprint, large inferential role)
      - Frequent but decorative (large footprint, little role)
      - Formal anchor with practical redundancy (ghost commitments)
      - Compression casualties (low salience, destroys counterfactual access)
    """
    surprises = []
    components = list(relation.components.values())
    if not components:
        return surprises

    avg_local = sum(c.local_curvature for c in components) / len(components)
    avg_length = sum(len(c.text.split()) for c in components) / len(components)

    for comp in components:
        length = len(comp.text.split())
        is_short = length < avg_length * 0.6
        is_long = length > avg_length * 1.6
        is_high_curve = comp.local_curvature > avg_local * 2

        if is_short and is_high_curve:
            surprises.append({
                "type": "rare_high_curvature",
                "component_id": comp.id,
                "description": "Small textual footprint, large inferential role",
                "local_curvature": comp.local_curvature,
                "word_count": length,
                "text_preview": comp.text[:120],
            })

        if is_long and comp.taxonomy == "Decoration":
            surprises.append({
                "type": "frequent_decorative",
                "component_id": comp.id,
                "description": "Large textual footprint, little accessibility role",
                "local_curvature": comp.local_curvature,
                "word_count": length,
                "text_preview": comp.text[:120],
            })

        if comp.taxonomy == "Ghost Commitment":
            surprises.append({
                "type": "ghost_commitment",
                "component_id": comp.id,
                "description": "Formally load-bearing but compression-robust",
                "local_curvature": comp.local_curvature,
                "aggregate_curvature": comp.aggregate_curvature,
                "text_preview": comp.text[:120],
            })

    return surprises


# ---------------------------------------------------------------------------
# Disagreement analysis
# ---------------------------------------------------------------------------

def disagreement_analysis(relation: AccessibilityRelation) -> list[dict]:
    """
    Type I:  CLIO detects trajectory loss but Spherepop found no Anchor.
             (Reducer missed a hidden load-bearing structure.)
    Type II: Spherepop finds an Anchor but CLIO finds it compression-robust.
             (Formally necessary but practically paraphrasable — ghost commitment.)
    """
    disagreements = []

    for comp in relation.components.values():
        compression_fragile = not (comp.survives_extractive and comp.survives_abstractive)
        is_anchor = comp.taxonomy in ("Anchor", "Distributed Anchor")

        # Type I: compression destroys access, but component wasn't flagged as Anchor
        if compression_fragile and not is_anchor:
            disagreements.append({
                "type": "Type_I",
                "label": "Compression casualty — missed anchor",
                "component_id": comp.id,
                "taxonomy": comp.taxonomy,
                "local_curvature": comp.local_curvature,
                "aggregate_curvature": comp.aggregate_curvature,
                "text_preview": comp.text[:120],
            })

        # Type II: Anchor but survives compression
        if is_anchor and comp.survives_extractive and comp.survives_abstractive:
            disagreements.append({
                "type": "Type_II",
                "label": "Formal anchor with practical redundancy",
                "component_id": comp.id,
                "taxonomy": comp.taxonomy,
                "local_curvature": comp.local_curvature,
                "text_preview": comp.text[:120],
            })

    return disagreements


# ---------------------------------------------------------------------------
# Main pipeline
# ---------------------------------------------------------------------------

class AdmissibilityLab:
    """
    Full pipeline: text -> inferential structure -> accessibility relation
    -> perturbation -> taxonomy -> surprises -> disagreements.
    """

    def __init__(self, domain: str = "general",
                 similarity_threshold: float = 0.45,
                 human_corrections: Optional[dict] = None):
        self.extractor = InferentialExtractor(domain=domain)
        self.qgen = QueryClassGenerator()
        self.clusterer = ConceptClusterer(
            similarity_threshold=similarity_threshold,
            human_corrections=human_corrections or {},
        )
        self.perturber = PerturbationEngine()
        self.compressor = CompressionSimulator()

    def similarity_report(self, text: str) -> list[dict]:
        """
        Run extraction only and return ranked similarity pairs.
        Use this to identify which components need human correction
        before running the full pipeline.
        """
        components = self.extractor.extract(text)
        return self.clusterer.similarity_report(components)

    def run(self, text: str, compression_ratio: float = 0.5,
            verbose: bool = True) -> dict:

        if verbose:
            print("=== Admissibility Lab ===\n")

        # 1. Extract inferential structure
        components = self.extractor.extract(text)
        if verbose:
            print(f"[1] Extracted {len(components)} inferential components")

        # 2. Generate query classes
        query_classes = self.qgen.generate(components)
        if verbose:
            print(f"[2] Generated {len(query_classes)} query classes")

        # 3. Build concept clusters (embedding-based)
        cluster_map = self.clusterer.assign(components, verbose=verbose)
        if verbose:
            print(f"[3] Identified {len(cluster_map)} concept clusters")

        # 4. Build accessibility relation
        relation = AccessibilityRelation(
            components={c.id: c for c in components},
            query_classes={q.id: q for q in query_classes},
            concept_clusters=cluster_map,
        )

        if not components:
            if verbose:
                print("\nNo inferential structure detected in text.")
            return {"error": "no_components"}

        # 5. Null baseline
        baseline = self.perturber.null_baseline(relation)
        if verbose:
            print(f"[4] Null baseline curvature: {baseline:.4f}")

        # 6. Point-load perturbation
        relation = self.perturber.point_load(relation)
        if verbose:
            print("[5] Point-load perturbation complete")

        # 7. Distributed-load perturbation
        relation = self.perturber.distributed_load(relation)
        if verbose:
            print("[6] Distributed-load perturbation complete")

        # 8. Compression simulation
        ext_compressed = self.compressor.extractive(text, ratio=compression_ratio)
        abs_compressed = self.compressor.abstractive(text)

        # Mark survival: component survives if its text appears (approx) in compressed version
        for comp in relation.components.values():
            key = comp.text[:40].lower().strip()
            comp.survives_extractive = key in ext_compressed.lower()
            comp.survives_abstractive = key in abs_compressed.lower()

        if verbose:
            print("[7] Compression simulation complete")

        # 9. Taxonomy assignment
        relation = assign_taxonomy(relation)
        if verbose:
            print("[8] Taxonomy assigned")

        # 10. Surprises and disagreements
        surprises = find_surprises(relation)
        disagreements = disagreement_analysis(relation)

        # 11. Build report
        report = self._report(relation, surprises, disagreements, verbose)
        return report

    def _report(self, relation, surprises, disagreements, verbose) -> dict:
        taxonomy_counts = defaultdict(int)
        for comp in relation.components.values():
            taxonomy_counts[comp.taxonomy] += 1

        top_anchors = sorted(
            [c for c in relation.components.values()
             if c.taxonomy in ("Anchor", "Distributed Anchor")],
            key=lambda c: c.local_curvature + c.aggregate_curvature,
            reverse=True
        )[:5]

        if verbose:
            print("\n--- Results ---\n")
            print("Taxonomy distribution:")
            for label, count in sorted(taxonomy_counts.items()):
                print(f"  {label:<25} {count}")

            print(f"\nNull baseline curvature:  {relation.null_baseline:.4f}")
            print(f"Total query classes:      {len(relation.query_classes)}")
            print(f"Total components:         {len(relation.components)}")

            if top_anchors:
                print("\nTop load-bearing components:")
                for comp in top_anchors:
                    print(f"\n  [{comp.taxonomy}] {comp.id}")
                    print(f"  Local curvature:     {comp.local_curvature:.4f}")
                    print(f"  Aggregate curvature: {comp.aggregate_curvature:.4f}")
                    print(f"  Cue type:            {comp.cue_type}")
                    print(f"  Preview: {comp.text[:100]}...")

            if surprises:
                print(f"\nSurprise cases ({len(surprises)}):")
                for s in surprises[:4]:
                    print(f"\n  [{s['type']}] {s['description']}")
                    print(f"  {s['text_preview']}...")

            if disagreements:
                print(f"\nDisagreement cases ({len(disagreements)}):")
                for d in disagreements[:4]:
                    print(f"\n  [{d['type']}] {d['label']}")
                    print(f"  Taxonomy: {d['taxonomy']}")
                    print(f"  {d['text_preview']}...")

        return {
            "taxonomy_counts": dict(taxonomy_counts),
            "null_baseline": relation.null_baseline,
            "n_components": len(relation.components),
            "n_query_classes": len(relation.query_classes),
            "n_clusters": len(relation.concept_clusters),
            "top_anchors": [
                {
                    "id": c.id,
                    "taxonomy": c.taxonomy,
                    "local_curvature": c.local_curvature,
                    "aggregate_curvature": c.aggregate_curvature,
                    "cue_type": c.cue_type,
                    "text": c.text,
                }
                for c in top_anchors
            ],
            "surprises": surprises,
            "disagreements": disagreements,
        }


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------

if __name__ == "__main__":
    import sys

    DEMO_TEXT = """
    If a system cannot reconstruct counterfactual queries from a compressed
    representation, then the compression has destroyed admissible trajectories,
    not merely reduced file size. This follows from the definition of
    accessibility: a state is accessible if and only if some admissible path
    leads to it from the current configuration.

    Markets allocate resources efficiently under conditions of perfect
    information. However, markets systematically fail under information
    asymmetry because buyers and sellers cannot coordinate on hidden states.
    Therefore, efficiency claims require assuming away the conditions most
    likely to obtain in practice.

    Suppose we remove the dependency on prior state. Then the system loses
    memory of admissible paths and cannot distinguish trajectories that
    passed through the same current state via different histories. Unless
    trajectory memory is preserved, reconstruction is impossible.

    One might object that compression is always lossy and this is trivially
    true. The claim is not that compression loses information — that is
    obvious — but that it loses information in a geometrically non-random
    way: it specifically destroys neighborhoods of states rather than
    isolated points. This requires demonstration, not assumption.

    Alternatively, one could model compression as projection onto a lower-
    dimensional manifold. In that case, the fibers of the projection —
    the sets of states mapped to the same compressed image — represent
    the destroyed distinctions. If those fibers are trajectory-aligned,
    the loss is catastrophic for counterfactual reasoning even when
    factual recall remains high.
    """

    if len(sys.argv) > 1:
        with open(sys.argv[1]) as f:
            text = f.read()
        domain = sys.argv[2] if len(sys.argv) > 2 else "general"
    else:
        text = DEMO_TEXT
        domain = "philosophy"

    lab = AdmissibilityLab(domain=domain)
    result = lab.run(text, verbose=True)

    out_path = "/mnt/user-data/outputs/admissibility_report.json"
    with open(out_path, "w") as f:
        json.dump(result, f, indent=2)
    print(f"\nFull report saved to {out_path}")
