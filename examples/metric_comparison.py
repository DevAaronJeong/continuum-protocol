"""
Metric Comparison - The "Cosine Removal" Analysis (Issue #4)

⚠️ THIS IS SYNTHETIC-DATA ANALYSIS, NOT EVIDENCE ABOUT HUMANS ⚠️

The project replaced Cosine Similarity (src/prototype.py) with weighted
Manhattan Distance (src/alignment_engine.py). Issue #4 asks whether that
was the right call. This script measures what the switch actually changes.

What synthetic data CAN tell us:
- Where the metrics agree and disagree, and on which kinds of pairs
- Structural properties (scale blindness, score compression, ties)

What it CANNOT tell us:
- Which metric matches how "fit" feels to a real person.
  That needs human judgments. Any "error" measured here assumes one
  metric is the truth, so this script reports disagreement, not accuracy.

All metrics are computed on the SAME vectors with the SAME weights,
so the only thing that varies is the metric itself.

Usage:
    python examples/metric_comparison.py           # full report
    python examples/metric_comparison.py --plot    # also save docs/assets/metric_comparison.png
    python examples/metric_comparison.py --test    # unit tests
"""

import os
import random
import sys
from typing import Dict, List

import numpy as np

ROOT = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..')
sys.path.insert(0, ROOT)
sys.path.insert(0, os.path.join(ROOT, 'examples'))

from src.alignment_engine import LifestyleVector, calculate_alignment  # noqa: E402
from synthetic_data import SyntheticDataGenerator  # noqa: E402


SEEDS = [0, 1, 2, 3, 4]
N_PEOPLE = 500
N_WORK = 50

# Same encoding and weights as src/alignment_engine.py
ENERGY_CODE = {"morning": 0.0, "afternoon": 0.33, "evening": 0.66, "distributed": 0.5}
DIMENSIONS = ["energy", "flexibility", "interaction", "change", "intensity"]
WEIGHTS = np.array([0.25, 0.15, 0.20, 0.20, 0.20])


# ============================================================================
# METRICS  (all return "higher = more aligned")
# ============================================================================

def cosine(x: np.ndarray, y: np.ndarray, w: np.ndarray) -> np.ndarray:
    """Weighted cosine similarity (the metric src/prototype.py used)."""
    num = (x * y * w).sum(-1)
    den = np.sqrt((x * x * w).sum(-1)) * np.sqrt((y * y * w).sum(-1))
    return np.divide(num, den, out=np.zeros_like(num, dtype=float), where=den > 0)


def centered_cosine(x: np.ndarray, y: np.ndarray, w: np.ndarray) -> np.ndarray:
    """Cosine measured from the scale midpoint (0.5) instead of from 0.

    This is the strongest version of cosine for bipolar [0, 1] scales:
    0.3 'morning preference' leans evening, and only centered cosine sees that.
    """
    return cosine(x - 0.5, y - 0.5, w)


def manhattan(x: np.ndarray, y: np.ndarray, w: np.ndarray) -> np.ndarray:
    """1 - weighted Manhattan distance (the current engine's core)."""
    return 1.0 - (np.abs(x - y) * w).sum(-1)


def euclidean(x: np.ndarray, y: np.ndarray, w: np.ndarray) -> np.ndarray:
    """1 - weighted Euclidean distance."""
    return 1.0 - np.sqrt((((x - y) ** 2) * w).sum(-1))


def chebyshev(x: np.ndarray, y: np.ndarray, w: np.ndarray) -> np.ndarray:
    """1 - largest single-dimension gap (unweighted 'dealbreaker' view)."""
    return 1.0 - np.abs(x - y).max(-1)


METRICS = {
    "cosine": cosine,
    "centered cosine": centered_cosine,
    "manhattan": manhattan,
    "euclidean": euclidean,
    "chebyshev": chebyshev,
}


# ============================================================================
# DATA
# ============================================================================

def to_array(v: LifestyleVector) -> np.ndarray:
    return np.array([
        ENERGY_CODE[v.energy_rhythm],
        v.time_flexibility,
        v.interaction_density,
        v.change_tolerance,
        v.intensity_preference,
    ])


def archetype_population(seed: int):
    """People and work drawn from the archetypes in examples/synthetic_data.py."""
    random.seed(seed)
    people = [SyntheticDataGenerator.generate_person() for _ in range(N_PEOPLE)]
    work = [SyntheticDataGenerator.generate_work() for _ in range(N_WORK)]
    return people, work


def uniform_population(seed: int):
    """No archetypes: every value uniform in [0, 1], rhythm uniform over 4."""
    rng = random.Random(seed)

    def one(kind):
        return LifestyleVector(
            energy_rhythm=rng.choice(list(ENERGY_CODE)),
            time_flexibility=rng.random(),
            interaction_density=rng.random(),
            change_tolerance=rng.random(),
            intensity_preference=rng.random(),
            consistency_score=rng.random(),
            profile_type=kind,
        )
    return [one("person") for _ in range(N_PEOPLE)], [one("work") for _ in range(N_WORK)]


POPULATIONS = {"archetype": archetype_population, "uniform": uniform_population}


# ============================================================================
# RANK HELPERS (no scipy dependency)
# ============================================================================

def _ranks(a: np.ndarray) -> np.ndarray:
    """Average ranks (ties share a rank), like scipy.stats.rankdata."""
    order = np.argsort(a, kind="mergesort")
    ranks = np.empty(len(a))
    sorted_a = a[order]
    i = 0
    while i < len(a):
        j = i
        while j + 1 < len(a) and sorted_a[j + 1] == sorted_a[i]:
            j += 1
        ranks[order[i:j + 1]] = (i + j) / 2.0
        i = j + 1
    return ranks


def spearman(a: np.ndarray, b: np.ndarray) -> float:
    ra, rb = _ranks(a), _ranks(b)
    ra, rb = ra - ra.mean(), rb - rb.mean()
    den = np.sqrt((ra ** 2).sum() * (rb ** 2).sum())
    return float((ra * rb).sum() / den) if den > 0 else 0.0


def top_k(scores: np.ndarray, k: int) -> set:
    return set(np.argsort(-scores, kind="mergesort")[:k].tolist())


# ============================================================================
# PART 1 - The worked examples from Issue #4 / docs/technical-philosophy.md
# ============================================================================

def part1_worked_examples():
    print("=" * 72)
    print("PART 1  Worked example from Issue #4 (person: morning=0.9, solo=0.2)")
    print("=" * 72)
    person = np.array([0.9, 0.2])
    jobs = {"A": [0.3, 0.1], "B": [0.85, 0.25], "C": [0.1, 0.9]}
    w = np.array([0.5, 0.5])
    print(f"{'job':<4}{'vector':<14}{'cosine':>8}{'ctr-cos':>9}{'L1 dist':>9}")
    for name, j in jobs.items():
        j = np.array(j)
        print(f"{name:<4}{str(j.tolist()):<14}"
              f"{cosine(person, j, w):>8.3f}{centered_cosine(person, j, w):>9.3f}"
              f"{np.abs(person - j).sum():>9.2f}")
    print("""
Reading:
  * Plain cosine rates A (0.995) almost the same as B (0.998): the doc is right.
  * But the reason is partly the 0..1 scale, not just 'magnitude blindness'.
    0.3 is BELOW the midpoint, i.e. job A leans evening. Plain cosine
    measures angles from 0, so every profile 'points the same way'.
  * Centered cosine (measured from 0.5) already separates A (0.18) from
    B (1.00). The real magnitude problem shows up in Part 2.
""")


# ============================================================================
# PART 2 - Pure magnitude test: same direction, weaker intensity
# ============================================================================

def part2_intensity_ladder():
    print("=" * 72)
    print("PART 2  Same preference direction, decreasing intensity")
    print("=" * 72)
    w = WEIGHTS
    person = np.array([0.0, 0.9, 0.1, 0.2, 0.9])  # morning, flexible, solo, routine, intense
    print("Work = person's profile pulled toward neutral (0.5) by factor k.")
    print(f"{'k':>5}{'cosine':>9}{'ctr-cos':>9}{'manhattan':>11}{'max gap':>9}")
    rows = []
    # k = 0 is left out: the work would sit exactly on the midpoint and
    # centered cosine is undefined there (zero vector).
    for k in [1.0, 0.75, 0.5, 0.25, 0.1]:
        work = 0.5 + k * (person - 0.5)
        row = (k, float(cosine(person, work, w)), float(centered_cosine(person, work, w)),
               float(manhattan(person, work, w)), float(np.abs(person - work).max()))
        rows.append(row)
        print(f"{row[0]:>5.2f}{row[1]:>9.3f}{row[2]:>9.3f}{row[3]:>11.3f}{row[4]:>9.2f}")
    high = np.full(5, 0.9)
    milder = np.full(5, 0.6)
    print(f"\nPerson high on everything (all 0.9) vs work at all 0.6:"
          f"  cosine={cosine(high, milder, w):.3f}"
          f"  manhattan={manhattan(high, milder, w):.3f}")
    print("""
Reading:
  * Centered cosine stays at 1.000 all the way down: 'leans the same way'
    is all it can see. This is the real 'Words' blind spot.
  * Manhattan falls steadily as the intensity gap grows: the 'Speed' signal.
  * Plain cosine also drops here, but only because this profile is lopsided.
    Its drop depends on the profile's shape, not the size of the gap: for the
    all-0.9 person, a uniformly milder job scores a perfect 1.000.
""")
    return rows


# ============================================================================
# PART 3 - The removed engine's own demo (src/prototype.py)
# ============================================================================

def part3_legacy_demo():
    print("=" * 72)
    print("PART 3  The removed cosine engine's own demo (src/prototype.py)")
    print("=" * 72)
    alice = np.array([0.9, 0.9, 0.2, 0.4])
    roles = {"startup": np.array([0.3, 0.3, 0.9, 0.9]),
             "async": np.array([0.8, 0.9, 0.1, 0.3])}
    w = np.full(4, 0.25)
    for name, r in roles.items():
        print(f"  Alice vs {name:<8} cosine={cosine(alice, r, w):.3f}  "
              f"manhattan={manhattan(alice, r, w):.3f}")
    print("""
Reading: both metrics agree on this demo, so it could never have shown the
difference. Disagreements live in 'same direction, different intensity'
cases (Part 2), which the demo did not include.
""")


# ============================================================================
# PART 4 - Population study
# ============================================================================

def score_matrix(people, work, metric, dims=slice(None)):
    X = np.array([to_array(p) for p in people])[:, dims]
    Y = np.array([to_array(v) for v in work])[:, dims]
    w = WEIGHTS[dims] / WEIGHTS[dims].sum()
    return METRICS[metric](X[:, None, :], Y[None, :, :], w), X, Y


def population_stats(people, work, dims=slice(None)) -> Dict:
    S = {m: score_matrix(people, work, m, dims)[0] for m in METRICS}
    _, X, Y = score_matrix(people, work, "manhattan", dims)
    gaps = np.abs(X[:, None, :] - Y[None, :, :])
    max_gap = gaps.max(-1)
    n = len(people)
    M = S["manhattan"]

    out = {}
    for m in ["cosine", "centered cosine", "euclidean", "chebyshev"]:
        A = S[m]
        out[m] = {
            "spearman": float(np.median([spearman(A[i], M[i]) for i in range(n)])),
            "top1": float(np.mean(A.argmax(1) == M.argmax(1))),
            "top5": float(np.mean([len(top_k(A[i], 5) & top_k(M[i], 5)) / 5 for i in range(n)])),
        }

    C = S["cosine"]
    near = C >= 0.95
    out["cos_ge_95_share"] = float(near.mean())
    out["cos_ge_95_gap_ge_40"] = float((near & (max_gap >= 0.4)).sum() / max(near.sum(), 1))
    out["cos_pct"] = np.percentile(C, [5, 50, 95]).tolist()
    out["man_pct"] = np.percentile(M, [5, 50, 95]).tolist()

    # What distinguishes the pairs where cosine and Manhattan disagree?
    # Split each gap into a shared 'level shift' (work is uniformly louder or
    # quieter) and the remaining 'shape' difference.
    diff = Y[None, :, :] - X[:, None, :]
    level = np.abs(diff.mean(-1))
    shape = np.abs(diff - diff.mean(-1, keepdims=True)).mean(-1)
    level_share = level / np.maximum(level + shape, 1e-9)
    cos_top = np.zeros_like(C, dtype=bool)
    man_top = np.zeros_like(M, dtype=bool)
    for i in range(n):
        cos_top[i, list(top_k(C[i], 5))] = True
        man_top[i, list(top_k(M[i], 5))] = True
    cos_only = cos_top & ~man_top
    man_only = man_top & ~cos_top
    out["level_share_cos_only"] = float(level_share[cos_only].mean())
    out["level_share_man_only"] = float(level_share[man_only].mean())
    out["level_share_all"] = float(level_share.mean())

    # Manhattan's own blind spot: dealbreakers hidden inside a good total
    best = M.argmax(1)
    out["man_top1_gap_ge_50"] = float(np.mean(max_gap[np.arange(n), best] >= 0.5))
    cheb_safe = np.array([
        max_gap[i, best[i]] >= 0.5 and (
            (max_gap[i] < 0.5) & (M[i] >= M[i, best[i]] - 0.02)).any()
        for i in range(n)])
    out["man_top1_avoidable_dealbreaker"] = float(cheb_safe.mean())
    # Engine sanity check: real engine score vs plain weighted Manhattan
    if dims == slice(None):
        E = np.array([[calculate_alignment(p, v)["score"] for v in work] for p in people])
        out["engine_vs_manhattan_spearman"] = float(
            np.median([spearman(E[i], M[i]) for i in range(n)]))
    return out


def part4_population():
    print("=" * 72)
    print(f"PART 4  Population study ({N_PEOPLE} people x {N_WORK} work, "
          f"seeds {SEEDS})")
    print("=" * 72)
    results = {}
    for pop_name, make in POPULATIONS.items():
        for enc_name, dims in [("5 dims", slice(None)), ("4 dims (no rhythm)", slice(1, None))]:
            runs = [population_stats(*make(s), dims=dims) for s in SEEDS]
            results[(pop_name, enc_name)] = runs
            _print_population(pop_name, enc_name, runs)
    return results


def _mean_range(runs: List[Dict], key, sub=None):
    vals = [r[key][sub] if sub else r[key] for r in runs]
    return np.mean(vals), np.min(vals), np.max(vals)


def _print_population(pop, enc, runs):
    print(f"\n[{pop} population, {enc}]  mean over seeds (min-max)")
    print(f"  {'vs manhattan':<17}{'spearman':>20}{'top-1 agree':>22}{'top-5 overlap':>22}")
    for m in ["cosine", "centered cosine", "euclidean", "chebyshev"]:
        cells = []
        for sub in ["spearman", "top1", "top5"]:
            mu, lo, hi = _mean_range(runs, m, sub)
            cells.append(f"{mu:.2f} ({lo:.2f}-{hi:.2f})")
        print(f"  {m:<17}{cells[0]:>20}{cells[1]:>22}{cells[2]:>22}")
    cp = np.mean([r["cos_pct"] for r in runs], axis=0)
    mp = np.mean([r["man_pct"] for r in runs], axis=0)
    print(f"  score spread p5/p50/p95  cosine {cp[0]:.2f}/{cp[1]:.2f}/{cp[2]:.2f}"
          f"   manhattan {mp[0]:.2f}/{mp[1]:.2f}/{mp[2]:.2f}")
    mu, lo, hi = _mean_range(runs, "cos_ge_95_share")
    print(f"  pairs cosine calls near-identical (>=0.95): {mu:.1%} ({lo:.1%}-{hi:.1%})")
    mu, lo, hi = _mean_range(runs, "cos_ge_95_gap_ge_40")
    print(f"    ...of which have a single-dimension gap >= 0.4: {mu:.1%} ({lo:.1%}-{hi:.1%})")
    a = _mean_range(runs, "level_share_cos_only")[0]
    b = _mean_range(runs, "level_share_man_only")[0]
    c = _mean_range(runs, "level_share_all")[0]
    print(f"  share of gap that is a uniform level shift:  cosine-only top-5 {a:.2f}"
          f" | manhattan-only top-5 {b:.2f} | all pairs {c:.2f}")
    mu, lo, hi = _mean_range(runs, "man_top1_gap_ge_50")
    print(f"  manhattan top-1 picks hiding a gap >= 0.5: {mu:.1%} ({lo:.1%}-{hi:.1%})")
    mu, lo, hi = _mean_range(runs, "man_top1_avoidable_dealbreaker")
    print(f"    ...where a near-equal option (within 0.02) had no such gap: "
          f"{mu:.1%} ({lo:.1%}-{hi:.1%})")
    if "engine_vs_manhattan_spearman" in runs[0]:
        mu, lo, hi = _mean_range(runs, "engine_vs_manhattan_spearman")
        print(f"  sanity: real engine vs plain weighted manhattan spearman {mu:.3f}")


# ============================================================================
# PART 5 - Manhattan's own weak spots
# ============================================================================

def part5_manhattan_weak_spots():
    print("\n" + "=" * 72)
    print("PART 5  Where Manhattan itself is weak")
    print("=" * 72)
    w = np.full(5, 0.2)
    person = np.full(5, 0.5)
    one_big = person + np.array([0.6, 0, 0, 0, 0])
    many_small = person + np.full(5, 0.12)
    print("  (a) Same total gap, different shape:")
    for name, y in [("one 0.60 gap", one_big), ("five 0.12 gaps", many_small)]:
        print(f"      {name:<15} manhattan={manhattan(person, y, w):.3f}  "
              f"euclidean={euclidean(person, y, w):.3f}  "
              f"chebyshev={chebyshev(person, y, w):.3f}")
    print("      Manhattan cannot tell a dealbreaker from spread-out friction.")

    print("\n  (b) Nominal weights vs. what each dimension can actually cost:")
    max_dist = {"energy": max(ENERGY_CODE.values()) - min(ENERGY_CODE.values())}
    for d, wt in zip(DIMENSIONS, WEIGHTS):
        md = max_dist.get(d, 1.0)
        print(f"      {d:<12} weight {wt:.2f}  x  max distance {md:.2f}  =  "
              f"max penalty {wt * md:.3f}")
    print("      energy has the largest weight but a smaller maximum penalty than")
    print("      interaction/change/intensity, because its codes only span 0-0.66.")

    print("\n  (c) Symmetry: a job 0.3 MORE intense and one 0.3 LESS intense than")
    print("      you get the same score. Overload and boredom are treated as equal.")


# ============================================================================
# PLOT
# ============================================================================

def save_plot(path: str):
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt

    people, work = archetype_population(SEEDS[0])
    C, X, Y = score_matrix(people, work, "cosine")
    M, _, _ = score_matrix(people, work, "manhattan")
    max_gap = np.abs(X[:, None, :] - Y[None, :, :]).max(-1)

    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 4.8))
    sc = ax1.scatter(C.ravel(), M.ravel(), c=max_gap.ravel(), s=3, alpha=0.4,
                     cmap="viridis", vmin=0, vmax=1)
    ax1.axvline(0.95, color="crimson", ls="--", lw=1)
    ax1.set_xlabel("Cosine similarity (removed engine)")
    ax1.set_ylabel("1 - weighted Manhattan (current engine)")
    ax1.set_title("Every person x work pair (archetype population, seed 0)")
    fig.colorbar(sc, ax=ax1, label="largest single-dimension gap")
    ax1.text(0.945, M.min(), "cosine >= 0.95 \u2192", color="crimson", fontsize=8,
             ha="right", va="bottom")

    rows = part2_rows()
    ks = [r[0] for r in rows]
    ax2.plot(ks, [r[1] for r in rows], "o-", label="cosine")
    ax2.plot(ks, [r[2] for r in rows], "s-", label="centered cosine")
    ax2.plot(ks, [r[3] for r in rows], "^-", label="manhattan")
    ax2.invert_xaxis()
    ax2.set_xlabel("work intensity relative to person (k: 1 = same, toward 0 = neutral)")
    ax2.set_ylabel("score")
    ax2.set_title("Same direction, weaker intensity")
    ax2.legend()
    ax2.grid(alpha=0.3)

    plt.tight_layout()
    plt.savefig(path, dpi=130)
    print(f"\nSaved figure to {path}")


def part2_rows():
    w = WEIGHTS
    person = np.array([0.0, 0.9, 0.1, 0.2, 0.9])
    rows = []
    for k in np.linspace(1.0, 0.1, 10):
        work = 0.5 + k * (person - 0.5)
        rows.append((k, float(cosine(person, work, w)),
                     float(centered_cosine(person, work, w)), float(manhattan(person, work, w))))
    return rows


# ============================================================================
# UNIT TESTS
# ============================================================================

def test_cosine_ignores_scale():
    x = np.array([0.2, 0.4, 0.6])
    assert abs(cosine(x, 0.5 * x, np.ones(3)) - 1.0) < 1e-12
    print("✅ test_cosine_ignores_scale passed")


def test_centered_cosine_ignores_intensity_around_midpoint():
    x = np.array([0.9, 0.2, 0.7])
    y = 0.5 + 0.25 * (x - 0.5)
    assert abs(centered_cosine(x, y, np.ones(3)) - 1.0) < 1e-12
    assert manhattan(x, y, np.ones(3) / 3) < 0.9
    print("✅ test_centered_cosine_ignores_intensity_around_midpoint passed")


def test_manhattan_matches_engine_on_continuous_dims():
    p = LifestyleVector("morning", 0.2, 0.4, 0.6, 0.8, consistency_score=1.0)
    q = LifestyleVector("morning", 0.3, 0.1, 0.6, 0.5, consistency_score=1.0)
    engine = calculate_alignment(p, q)["score"]
    ours = float(manhattan(to_array(p), to_array(q), WEIGHTS))
    assert abs(engine - ours) < 1e-9, (engine, ours)
    print("✅ test_manhattan_matches_engine_on_continuous_dims passed")


def test_spearman():
    a = np.array([1.0, 2.0, 3.0, 4.0])
    assert abs(spearman(a, a) - 1.0) < 1e-12
    assert abs(spearman(a, -a) + 1.0) < 1e-12
    assert abs(spearman(a, np.array([1.0, 1.0, 2.0, 2.0])) - 0.8944271909999159) < 1e-9
    print("✅ test_spearman passed")


def test_equal_l1_shapes_tie():
    w = np.full(5, 0.2)
    p = np.full(5, 0.5)
    a = manhattan(p, p + np.array([0.6, 0, 0, 0, 0]), w)
    b = manhattan(p, p + np.full(5, 0.12), w)
    assert abs(a - b) < 1e-12
    print("✅ test_equal_l1_shapes_tie passed")


def run_tests():
    print("\nRUNNING UNIT TESTS\n")
    test_cosine_ignores_scale()
    test_centered_cosine_ignores_intensity_around_midpoint()
    test_manhattan_matches_engine_on_continuous_dims()
    test_spearman()
    test_equal_l1_shapes_tie()
    print("\n✅ All unit tests passed!")


# ============================================================================
# MAIN
# ============================================================================

def main():
    if "--test" in sys.argv:
        run_tests()
        return
    print("\nMETRIC COMPARISON - 'cosine removal' analysis for Issue #4")
    print("Synthetic data only. Reports disagreement, not accuracy.\n")
    part1_worked_examples()
    part2_intensity_ladder()
    part3_legacy_demo()
    part4_population()
    part5_manhattan_weak_spots()
    if "--plot" in sys.argv:
        save_plot(os.path.join(ROOT, "docs", "assets", "metric_comparison.png"))


if __name__ == "__main__":
    main()
