"""
Survey Analysis - Experiment 2.5 (Retrospective Fit Survey)

Reads the exported survey responses and runs exactly the checks fixed in
docs/experiments/retrospective-fit-survey.md, before any data was collected.

Do not change the primary check, the exclusions, or the reading rules after
the survey opens. Anything added later must be labelled exploratory.

Usage:
    python examples/survey_analysis.py data/survey_responses.csv
    python examples/survey_analysis.py --demo              # made-up data, fit follows Manhattan
    python examples/survey_analysis.py --demo cosine       # made-up data, fit follows cosine
    python examples/survey_analysis.py --demo none         # made-up data, fit is random
    python examples/survey_analysis.py --test              # unit tests

Columns: see docs/experiments/retrospective-fit-survey.md ("CSV columns").
Energy answers may be in English or Korean.
"""

import csv
import os
import random
import sys
import tempfile
from typing import Dict, List, Optional, Tuple

import numpy as np

ROOT = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..')
sys.path.insert(0, os.path.join(ROOT, 'examples'))

from metric_comparison import ENERGY_CODE, METRICS, WEIGHTS, spearman  # noqa: E402

SEED = 2026
N_BOOT = 5000
DIMS = ["energy", "flex", "people", "change", "pace"]
DIM_LABELS = ["energy rhythm", "schedule flexibility", "working with others",
              "change", "pace"]


# ============================================================================
# PARSING
# ============================================================================

_ENERGY_PREFIXES = [
    ("morning", ["morning", "오전"]),
    ("afternoon", ["afternoon", "오후"]),
    ("evening", ["evening", "night", "저녁", "밤"]),
    ("distributed", ["it varies", "varies", "spread", "distributed",
                     "하루 중", "하루 전체", "그때그때"]),
]


def parse_energy(value: str) -> Optional[str]:
    v = (value or "").strip().lower()
    if not v:
        return None
    for code, keys in _ENERGY_PREFIXES:
        if any(v.startswith(k) or k in v for k in keys):
            return code
    return None


def parse_number(value: str) -> Optional[float]:
    v = (value or "").strip()
    if not v:
        return None
    try:
        return float(v)
    except ValueError:
        return None


def parse_consent(value: str) -> bool:
    v = (value or "").strip().lower()
    return v not in {"", "false", "no", "0", "아니요", "아니오", "n"}


def load_rows(path: str) -> List[Dict[str, str]]:
    with open(path, newline="", encoding="utf-8-sig") as f:
        return list(csv.DictReader(f))


# ============================================================================
# EXCLUSIONS AND PAIRS (fixed in advance)
# ============================================================================

def _job(row: Dict[str, str], prefix: str):
    """Return (vector, fit, adjust) for a job, or None if any required answer is missing."""
    energy = parse_energy(row.get(f"{prefix}_energy", ""))
    nums = [parse_number(row.get(f"{prefix}_{d}", "")) for d in DIMS[1:]]
    fit = parse_number(row.get(f"{prefix}_fit", ""))
    adjust = parse_number(row.get(f"{prefix}_adjust", ""))
    if energy is None or any(n is None for n in nums) or fit is None or adjust is None:
        return None
    vec = np.array([ENERGY_CODE[energy]] + [n / 10.0 for n in nums])
    return vec, fit, adjust


def _self(row: Dict[str, str]):
    energy = parse_energy(row.get("self_energy", ""))
    nums = [parse_number(row.get(f"self_{d}", "")) for d in DIMS[1:]]
    if energy is None or any(n is None for n in nums):
        return None
    return np.array([ENERGY_CODE[energy]] + [n / 10.0 for n in nums])


def _all_0_10_answers(row: Dict[str, str]) -> List[float]:
    vals = []
    for prefix in ["self", "a", "b"]:
        for d in DIMS[1:] + (["adjust"] if prefix != "self" else []):
            n = parse_number(row.get(f"{prefix}_{d}", ""))
            if n is not None:
                vals.append(n)
    return vals


def build_pairs(rows: List[Dict[str, str]]):
    """Apply the pre-declared exclusions and return person-job pairs."""
    excluded = {"no consent": 0, "Part 2 incomplete": 0,
                "attention check": 0, "same answer everywhere": 0}
    pairs = []  # (respondent, self_vec, job_vec, fit, adjust, which)
    kept = 0
    for i, row in enumerate(rows):
        if not parse_consent(row.get("consent", "")):
            excluded["no consent"] += 1
            continue
        me = _self(row)
        job_a = _job(row, "a")
        if me is None or job_a is None:
            excluded["Part 2 incomplete"] += 1
            continue
        if parse_number(row.get("a_check", "")) != 4:
            excluded["attention check"] += 1
            continue
        answers = _all_0_10_answers(row)
        if len(answers) > 1 and len(set(answers)) == 1:
            excluded["same answer everywhere"] += 1
            continue
        kept += 1
        pairs.append((i, me, job_a[0], job_a[1], job_a[2], "a"))
        job_b = _job(row, "b")
        if job_b is not None:
            pairs.append((i, me, job_b[0], job_b[1], job_b[2], "b"))
    return pairs, excluded, kept


# ============================================================================
# CHECKS
# ============================================================================

def scores(pairs, metric: str) -> np.ndarray:
    X = np.array([p[1] for p in pairs])
    Y = np.array([p[2] for p in pairs])
    return METRICS[metric](X, Y, WEIGHTS)


def cluster_bootstrap(pairs, stat, n_boot: int = N_BOOT, seed: int = SEED) -> np.ndarray:
    """Resample respondents (not pairs) with replacement."""
    rng = np.random.default_rng(seed)
    by_person: Dict[int, List[int]] = {}
    for k, p in enumerate(pairs):
        by_person.setdefault(p[0], []).append(k)
    people = list(by_person)
    out = np.empty(n_boot)
    for b in range(n_boot):
        chosen = rng.choice(len(people), size=len(people), replace=True)
        idx = [k for c in chosen for k in by_person[people[c]]]
        out[b] = stat([pairs[k] for k in idx])
    return out


def rho(pairs, metric: str, outcome: str = "fit") -> float:
    col = 3 if outcome == "fit" else 4
    return spearman(scores(pairs, metric), np.array([p[col] for p in pairs]))


def interval(samples: np.ndarray) -> Tuple[float, float]:
    lo, hi = np.nanpercentile(samples, [2.5, 97.5])
    return float(lo), float(hi)


def primary_check(pairs, n_boot: int = N_BOOT) -> Dict:
    r_m = rho(pairs, "manhattan")
    r_c = rho(pairs, "cosine")
    boot_m = cluster_bootstrap(pairs, lambda ps: rho(ps, "manhattan"), n_boot)
    boot_d = cluster_bootstrap(pairs, lambda ps: rho(ps, "manhattan") - rho(ps, "cosine"), n_boot)
    return {"rho_manhattan": r_m, "rho_cosine": r_c, "d": r_m - r_c,
            "ci_manhattan": interval(boot_m), "ci_d": interval(boot_d)}


def reading(res: Dict) -> List[str]:
    """The reading rules from the plan, applied mechanically."""
    lines = []
    lo_m, hi_m = res["ci_manhattan"]
    if lo_m <= 0 <= hi_m:
        lines.append("BASIC CHECK FAILS: the Manhattan alignment score does not track "
                     "reported fit in this sample (its interval includes 0).")
    else:
        lines.append("Basic check holds: the Manhattan alignment score tracks reported fit.")
    lo, hi = res["ci_d"]
    if lo > 0:
        lines.append("Consistent with the 'same speed' assumption: Manhattan tracks fit "
                     "better than cosine.")
    elif hi < 0:
        lines.append("Inconsistent with the assumption: cosine tracks fit better. "
                     "Revisit the metric choice.")
    else:
        lines.append("Can't tell Manhattan and cosine apart with this sample.")
    return lines


def within_person(pairs) -> Dict[str, Tuple[int, int]]:
    """For people with two jobs: how often does the higher-scoring job get the higher fit?"""
    by_person: Dict[int, List] = {}
    for p in pairs:
        by_person.setdefault(p[0], []).append(p)
    twos = [ps for ps in by_person.values() if len(ps) == 2 and ps[0][3] != ps[1][3]]
    out = {}
    for m in METRICS:
        agree = 0
        for a, b in twos:
            s = scores([a, b], m)
            if s[0] != s[1] and (s[0] > s[1]) == (a[3] > b[3]):
                agree += 1
        out[m] = (agree, len(twos))
    return out


def exploratory(pairs) -> Dict:
    X = np.array([p[1] for p in pairs])
    Y = np.array([p[2] for p in pairs])
    fit = np.array([p[3] for p in pairs])
    gaps = {DIM_LABELS[d]: spearman(np.abs(Y[:, d] - X[:, d]), fit) for d in range(5)}
    pace = Y[:, 4] - X[:, 4]
    more = fit[pace >= 0.2]
    less = fit[pace <= -0.2]
    return {"gap_rho": gaps,
            "pace_more_intense": (float(more.mean()) if len(more) else float("nan"), len(more)),
            "pace_less_intense": (float(less.mean()) if len(less) else float("nan"), len(less))}


# ============================================================================
# REPORT
# ============================================================================

def report(rows, n_boot: int = N_BOOT) -> Dict:
    pairs, excluded, kept = build_pairs(rows)
    print("=" * 70)
    print("EXPERIMENT 2.5  Retrospective fit survey")
    print("=" * 70)
    print(f"Responses: {len(rows)}   kept: {kept}   person-job pairs: {len(pairs)}")
    for reason, n in excluded.items():
        print(f"  excluded ({reason}): {n}")
    if kept < 5 or len(pairs) < 8:
        print("\nToo few usable responses to run the checks.")
        return {}

    res = primary_check(pairs, n_boot)
    print("\nPRIMARY CHECK  (Spearman correlation with fit rating, 1-7)")
    print(f"  Manhattan (engine):  rho = {res['rho_manhattan']:+.2f}   "
          f"95% interval {res['ci_manhattan'][0]:+.2f} to {res['ci_manhattan'][1]:+.2f}")
    print(f"  Cosine (removed):    rho = {res['rho_cosine']:+.2f}")
    print(f"  Difference d:        {res['d']:+.2f}   "
          f"95% interval {res['ci_d'][0]:+.2f} to {res['ci_d'][1]:+.2f}")
    print("\nREADING (rules fixed before data collection)")
    for line in reading(res):
        print(f"  - {line}")

    print("\nSECONDARY  (reported, not used for the reading)")
    print("  Correlation with fit / with adjustment effort (expected negative):")
    for m in METRICS:
        print(f"    {m:<16} fit {rho(pairs, m):+.2f}   adjustment {rho(pairs, m, 'adjust'):+.2f}")
    wp = within_person(pairs)
    n2 = next(iter(wp.values()))[1]
    print(f"  Within-person ({n2} people with two jobs rated differently):")
    for m, (agree, n) in wp.items():
        share = f"{agree / n:.0%}" if n else "n/a"
        print(f"    {m:<16} higher score = higher fit in {agree}/{n} ({share})")

    ex = exploratory(pairs)
    print("\nEXPLORATORY  (no conclusions)")
    print("  Gap on each dimension vs fit (negative = bigger gap, worse fit):")
    for label, r in ex["gap_rho"].items():
        print(f"    {label:<22} {r:+.2f}")
    (m_more, n_more), (m_less, n_less) = ex["pace_more_intense"], ex["pace_less_intense"]
    print(f"  Pace: job more intense than you -> mean fit {m_more:.2f} (n={n_more}); "
          f"less intense -> {m_less:.2f} (n={n_less})")
    return res


# ============================================================================
# DEMO DATA (made up, for checking the pipeline only)
# ============================================================================

def make_demo_rows(truth: str = "manhattan", n_people: int = 30, seed: int = 7) -> List[Dict[str, str]]:
    """Fake responses. `truth` decides which metric the fit ratings follow."""
    rng = random.Random(seed)
    energies = ["Morning", "오후", "Evening or night", "하루 중 그때그때 다름"]
    rows = []
    for _ in range(n_people):
        row = {"consent": "true", "self_energy": rng.choice(energies), "a_check": "4"}
        for d in DIMS[1:]:
            row[f"self_{d}"] = str(rng.randint(0, 10))
        for prefix in ["a", "b"] if rng.random() < 0.6 else ["a"]:
            row[f"{prefix}_energy"] = rng.choice(energies)
            for d in DIMS[1:]:
                row[f"{prefix}_{d}"] = str(rng.randint(0, 10))
            me, job = _self(row), _job({**row, f"{prefix}_fit": "4", f"{prefix}_adjust": "5"}, prefix)[0]
            if truth == "none":
                latent = rng.random()
            else:
                latent = float(METRICS[truth](me, job, WEIGHTS))
                latent = (latent - 0.5) * 2 + rng.gauss(0, 0.15)
            fit = int(np.clip(round(1 + 6 * latent), 1, 7))
            row[f"{prefix}_fit"] = str(fit)
            row[f"{prefix}_adjust"] = str(int(np.clip(round(10 - fit * 1.3 + rng.gauss(0, 1)), 0, 10)))
        rows.append(row)
    rows.append({"consent": "", "self_energy": "Morning"})                       # no consent
    rows.append({**rows[0], "a_check": "6"})                                      # attention
    return rows


def run_demo(truth: str):
    rows = make_demo_rows(truth)
    with tempfile.TemporaryDirectory() as d:
        path = os.path.join(d, "demo.csv")
        cols = sorted({k for r in rows for k in r})
        with open(path, "w", newline="", encoding="utf-8") as f:
            w = csv.DictWriter(f, fieldnames=cols)
            w.writeheader()
            w.writerows(rows)
        print(f"\n*** DEMO: made-up responses where fit follows '{truth}'. Not real data. ***\n")
        report(load_rows(path), n_boot=1000)


# ============================================================================
# TESTS
# ============================================================================

def test_parse_energy():
    assert parse_energy("Morning") == "morning"
    assert parse_energy("오후") == "afternoon"
    assert parse_energy("Evening or night") == "evening"
    assert parse_energy("저녁·밤") == "evening"
    assert parse_energy("It varies across the day") == "distributed"
    assert parse_energy("하루 전체에 퍼져 있음") == "distributed"
    assert parse_energy("") is None
    print("✅ test_parse_energy passed")


def test_exclusions():
    good = {"consent": "true", "self_energy": "Morning", "self_flex": "2", "self_people": "3",
            "self_change": "4", "self_pace": "5", "a_energy": "오전", "a_flex": "6",
            "a_people": "7", "a_change": "8", "a_pace": "9", "a_fit": "5", "a_adjust": "3",
            "a_check": "4"}
    rows = [good,
            {**good, "consent": ""},
            {**good, "a_fit": ""},
            {**good, "a_check": "5"},
            {**good, **{k: "5" for k in good if k.split("_")[-1] in DIMS[1:] + ["adjust"]}}]
    pairs, excluded, kept = build_pairs(rows)
    assert kept == 1 and len(pairs) == 1, (kept, len(pairs))
    assert excluded == {"no consent": 1, "Part 2 incomplete": 1,
                        "attention check": 1, "same answer everywhere": 1}, excluded
    assert np.allclose(pairs[0][1], [0.0, 0.2, 0.3, 0.4, 0.5])
    print("✅ test_exclusions passed")


def test_second_job_needs_all_answers():
    base = make_demo_rows("manhattan", n_people=1)[0]
    base.update({"b_energy": "Morning", "b_flex": "1", "b_people": "", "b_change": "1",
                 "b_pace": "1", "b_fit": "3", "b_adjust": "2"})
    pairs, _, _ = build_pairs([base])
    assert len(pairs) == 1
    print("✅ test_second_job_needs_all_answers passed")


def test_bootstrap_is_reproducible():
    pairs, _, _ = build_pairs(make_demo_rows("manhattan"))
    a = cluster_bootstrap(pairs, lambda ps: rho(ps, "manhattan"), n_boot=200)
    b = cluster_bootstrap(pairs, lambda ps: rho(ps, "manhattan"), n_boot=200)
    assert np.array_equal(a, b)
    print("✅ test_bootstrap_is_reproducible passed")


def test_pipeline_recovers_the_truth():
    pairs, _, _ = build_pairs(make_demo_rows("manhattan", n_people=300, seed=1))
    res = primary_check(pairs, n_boot=300)
    assert res["ci_manhattan"][0] > 0 and res["ci_d"][0] > 0, res
    pairs, _, _ = build_pairs(make_demo_rows("none", n_people=300, seed=1))
    res = primary_check(pairs, n_boot=300)
    assert res["ci_manhattan"][0] <= 0 <= res["ci_manhattan"][1], res
    print("✅ test_pipeline_recovers_the_truth passed")


def run_tests():
    print("\nRUNNING UNIT TESTS\n")
    test_parse_energy()
    test_exclusions()
    test_second_job_needs_all_answers()
    test_bootstrap_is_reproducible()
    test_pipeline_recovers_the_truth()
    print("\n✅ All unit tests passed!")


# ============================================================================
# MAIN
# ============================================================================

def main():
    args = sys.argv[1:]
    if "--test" in args:
        run_tests()
    elif "--demo" in args:
        i = args.index("--demo")
        truth = args[i + 1] if i + 1 < len(args) else "manhattan"
        if truth not in list(METRICS) + ["none"]:
            sys.exit(f"--demo takes one of: {', '.join(list(METRICS) + ['none'])}")
        run_demo(truth)
    elif args:
        report(load_rows(args[0]))
    else:
        print(__doc__)


if __name__ == "__main__":
    main()
