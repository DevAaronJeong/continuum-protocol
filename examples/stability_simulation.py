"""
Stability Simulation

Synthetic trajectories for the "fit as dynamic stability" model
(docs/fit-as-stability.md), and the check that reads them.

K(i) is the work-state readout at episode i. In the planned diary study
(Roadmap Experiment 2.6) it is a weekly answer to "How much did you have to
adjust yourself to your work this week?" on a 0-10 scale, so the synthetic
trajectories here use the same scale.

What this script does:
1. Generates three kinds of synthetic K(i):
   - settling:     returns to a fixed sustainable baseline (mean reversion)
   - drifting:     the baseline itself keeps rising at a steady rate
   - accelerating: the baseline rises faster and faster
2. Reads each one by its level, trend, and volatility over time
   (stability_profile), after a settling period.
3. Keeps the original first-arrival gaps (a_j, s_j) as an auxiliary measure
   and shows where they fail on their own.
4. Checks how many episodes the time-based check needs before it can tell
   the kinds apart (window_study).

⚠️ Synthetic data only. Every trajectory is generated from the assumption it
illustrates, so nothing here is evidence about real people.

Revised in November 2026 after Issue #4: the earlier "stable" generator still
drifted upward over long runs, and the stability check read levels in the
order they first appeared instead of over time. See "Correction (November
2026)" in docs/fit-as-stability.md.

Usage:
    python examples/stability_simulation.py                 # report and plots
    python examples/stability_simulation.py --save-figures  # write docs/assets/Figure_1-3.png
    python examples/stability_simulation.py --test          # unit tests
"""

import os
import sys
from dataclasses import dataclass, replace
from typing import Dict, List, Optional, Sequence

import numpy as np


# ============================================================================
# SYNTHETIC TRAJECTORIES
# ============================================================================

@dataclass
class TrajectoryConfig:
    """Parameters for one synthetic K(i) sequence on a 0-10 adjustment scale."""
    n_episodes: int = 50
    start: float = 3.0         # K at episode 0
    baseline: float = 3.0      # level the process is pulled back to
    reversion: float = 0.4     # share of the gap to the baseline closed each episode (0 < r <= 1)
    drift: float = 0.0         # how much the baseline rises per episode
    acceleration: float = 0.0  # how much that rise grows per episode
    noise: float = 0.5         # SD of episode-to-episode noise
    scale_max: float = 10.0    # top of the answer scale; K is kept in [0, scale_max]


# The kinds of trajectory used throughout this script.
KINDS: Dict[str, TrajectoryConfig] = {
    # Starts high (a new job), then returns to a fixed baseline and stays there.
    "settling": TrajectoryConfig(start=5.0),
    # Same as settling, but with much larger week-to-week swings.
    "noisy": TrajectoryConfig(start=5.0, noise=1.2),
    # The baseline rises by 0.08 per episode: about 4 points over 50 episodes.
    "drifting": TrajectoryConfig(drift=0.08),
    # The baseline rises faster and faster: about 5 points over 50 episodes.
    "accelerating": TrajectoryConfig(acceleration=0.004),
}


def baseline_at(config: TrajectoryConfig, i: int) -> float:
    """The level K is pulled toward at episode i."""
    return config.baseline + config.drift * i + 0.5 * config.acceleration * i * i


def generate_work_state_sequence(config: TrajectoryConfig,
                                 rng: Optional[np.random.Generator] = None) -> np.ndarray:
    """
    Generate K(i), the work-state readout sequence.

        K[i] = K[i-1] + reversion * (baseline_at(i) - K[i-1]) + noise

    With drift = acceleration = 0 the baseline is fixed, so K is pulled back to
    the same level however long it runs (with noise off, K[i] -> baseline).
    With drift > 0, K follows a baseline that keeps rising, so it rises at the
    drift rate for as long as it runs.
    """
    rng = rng if rng is not None else np.random.default_rng()
    K = np.zeros(config.n_episodes)
    K[0] = config.start
    for i in range(1, config.n_episodes):
        pull = config.reversion * (baseline_at(config, i) - K[i - 1])
        value = K[i - 1] + pull + rng.normal(0.0, config.noise)
        K[i] = min(max(value, 0.0), config.scale_max)
    return K


# ============================================================================
# TIME-BASED STABILITY CHECK
# ============================================================================

def theil_sen_slope(y: Sequence[float], x: Optional[Sequence[float]] = None) -> float:
    """Median of all pairwise slopes. One bad week cannot drag it far."""
    y = np.asarray(y, dtype=float)
    x = np.arange(len(y), dtype=float) if x is None else np.asarray(x, dtype=float)
    i, j = np.triu_indices(len(y), k=1)
    dx = x[j] - x[i]
    keep = dx != 0
    if not keep.any():
        return float("nan")
    return float(np.median((y[j] - y[i])[keep] / dx[keep]))


@dataclass
class StabilityProfile:
    """
    How K behaved over the observed episodes.

    Every field describes the observed window only. "flat" means no clear
    trend in this window; it does not prove K would stay bounded forever.
    """
    n_used: int          # episodes read, after the settling period
    level: float         # median K
    trend: float         # Theil-Sen slope of K, in scale points per episode
    volatility: float    # typical distance from the trend line (scaled MAD)
    trend_change: float  # slope in the later half minus slope in the earlier half
    label: str           # "flat", "falling", "rising", "accelerating", or "too short"


def stability_profile(K: Sequence[float], settle: int = 4,
                      slope_tol: float = 0.05, accel_tol: float = 0.05,
                      min_points: int = 5) -> StabilityProfile:
    """
    Read K over time: level, trend, and volatility after a settling period.

    Args:
        settle: episodes to skip at the start (the settling period)
        slope_tol: trends within +/- this many points per episode count as flat.
                   0.05 is one scale point over 20 episodes.
        accel_tol: a rising K whose later-half slope exceeds its earlier-half
                   slope by more than this counts as accelerating
        min_points: fewer episodes than this after settling -> "too short"

    These defaults are starting values for synthetic data on a 0-10 scale.
    They should be revisited once real diary data exists (Experiment 2.6).
    """
    y = np.asarray(K, dtype=float)[settle:]
    n = len(y)
    nan = float("nan")
    if n < min_points:
        level = float(np.median(y)) if n else nan
        return StabilityProfile(n, level, nan, nan, nan, "too short")

    x = np.arange(settle, settle + n, dtype=float)
    trend = theil_sen_slope(y, x)
    intercept = float(np.median(y - trend * x))
    resid = y - (intercept + trend * x)
    volatility = float(1.4826 * np.median(np.abs(resid - np.median(resid))))

    # Each half needs at least 4 episodes for its own slope to mean much.
    trend_change = nan
    if n >= 8:
        half = n // 2
        early = theil_sen_slope(y[:half], x[:half])
        late = theil_sen_slope(y[half:], x[half:])
        trend_change = late - early

    if trend > slope_tol:
        label = "accelerating" if trend_change > accel_tol else "rising"
    elif trend < -slope_tol:
        label = "falling"
    else:
        label = "flat"
    return StabilityProfile(n, float(np.median(y)), trend, volatility, trend_change, label)


def is_rising(label: str) -> bool:
    return label in ("rising", "accelerating")


# ============================================================================
# FIRST-ARRIVAL GAPS (AUXILIARY MEASURE)
# ============================================================================
#
# The original Phase 0 check. It looks only at when a new readout level is
# reached for the first time, in the order those levels appear, and ignores
# the time between them. Issue #4 showed two failures:
#   K = [0, 2, 1]        -> s_j = [-3]       "unstable", though adjustment is bounded
#   K = [0, 1, 2, 3, 4]  -> s_j = [0, 0, 0]  "stable", though adjustment keeps rising
# It is kept as a secondary description of how new levels arrive, not as the
# stability check.

def extract_first_time_states(K: Sequence[float], quantize: float = 0.5) -> List[float]:
    """
    Extract a_j - first-time-seen readout levels, in the order they appear.

    L(i) = floor(K(i) / quantize)
    a_j = values of L (times quantize) not seen before, in encounter order

    The formulation in docs/fit-as-stability.md writes a_1 < a_2 < ...; the two
    only match when K keeps reaching new highs.
    """
    L = np.floor(np.asarray(K, dtype=float) / quantize)
    seen = set()
    a_sequence = []
    for level in L:
        if level not in seen:
            seen.add(level)
            a_sequence.append(float(level * quantize))
    return a_sequence


def compute_s_j(a_sequence: List[float]) -> List[float]:
    """
    s_j - change in step size between first-time levels.

    Delta_j = a_{j+1} - a_j
    s_j = Delta_{j+1} - Delta_j
    """
    if len(a_sequence) < 3:
        return []
    deltas = [a_sequence[i + 1] - a_sequence[i] for i in range(len(a_sequence) - 1)]
    return [deltas[i + 1] - deltas[i] for i in range(len(deltas) - 1)]


def is_bounded(s_j: List[float], threshold: float = 1.0) -> bool:
    """Auxiliary: is max(|s_j|) below the threshold? See the note above."""
    if not s_j:
        return True
    return max(abs(s) for s in s_j) < threshold


def first_arrival_reading(K: Sequence[float], quantize: float = 0.5) -> str:
    """What the original Phase 0 check would have said."""
    return "stable" if is_bounded(compute_s_j(extract_first_time_states(K, quantize))) else "unstable"


# ============================================================================
# STUDIES
# ============================================================================

def window_study(windows: Sequence[int] = (8, 12, 26, 50), n_people: int = 500,
                 settle: int = 4, seed: int = 2026) -> List[dict]:
    """
    For each kind and window length (episodes after settling), the share of
    synthetic trajectories that each check calls rising, and for the
    accelerating kind, the share called accelerating.
    """
    rng = np.random.default_rng(seed)
    rows = []
    for kind, base in KINDS.items():
        for w in windows:
            config = replace(base, n_episodes=settle + w)
            labels, old = [], []
            for _ in range(n_people):
                K = generate_work_state_sequence(config, rng)
                labels.append(stability_profile(K, settle=settle).label)
                old.append(first_arrival_reading(K[settle:]))
            rows.append({
                "kind": kind,
                "window": w,
                "rising": sum(is_rising(lab) for lab in labels) / n_people,
                "accelerating": labels.count("accelerating") / n_people,
                "old_unstable": old.count("unstable") / n_people,
            })
    return rows


def print_window_study(rows: List[dict]):
    print("\n" + "=" * 72)
    print("HOW MANY EPISODES DOES THE CHECK NEED? (500 synthetic trajectories each)")
    print("=" * 72)
    print(f"{'kind':<13}{'episodes':>9}{'called rising':>15}{'called accel.':>15}"
          f"{'old: unstable':>15}")
    for r in rows:
        print(f"{r['kind']:<13}{r['window']:>9}{r['rising']:>15.0%}{r['accelerating']:>15.0%}"
              f"{r['old_unstable']:>15.0%}")
    print("\n'called rising' includes 'accelerating'. 'old: unstable' is the first-arrival")
    print("check (max |s_j| >= 1) on the same episodes.")


def hypothesis_visualization(n_samples: int = 200, seed: int = 7):
    """
    HYPOTHESIS VISUALIZATION (NOT DATA ANALYSIS)

    Generates trajectories ASSUMING the hypothesis "larger initial distance ->
    rising adjustment" is true, then reads them with the time-based check.
    Any relationship in the output was put there by the assumption below.
    """
    rng = np.random.default_rng(seed)
    results = []
    for _ in range(n_samples):
        distance = rng.uniform(0.1, 0.9)
        # ASSUMPTION INJECTED HERE: no drift for close matches, drift grows
        # with distance beyond 0.3. This is what real data would have to show,
        # not something the simulation can discover.
        drift = 0.12 * max(0.0, distance - 0.3)
        K = generate_work_state_sequence(replace(KINDS["settling"], drift=drift), rng)
        profile = stability_profile(K)
        results.append((distance, profile.trend, profile.label))
    return results


def quantize_sensitivity_demo(seed: int = 3):
    """How the quantize step changes the auxiliary first-arrival measure."""
    print("\n" + "=" * 72)
    print("QUANTIZE SENSITIVITY (auxiliary first-arrival measure only)")
    print("=" * 72)
    K = generate_work_state_sequence(KINDS["drifting"], np.random.default_rng(seed))
    for q in (0.1, 0.25, 0.5, 1.0, 2.0):
        a_seq = extract_first_time_states(K, quantize=q)
        s_j = compute_s_j(a_seq)
        max_s = max(abs(s) for s in s_j) if s_j else 0.0
        print(f"  quantize={q:4.2f} -> {len(a_seq):2d} first-time levels, "
              f"{len(s_j):2d} s_j values, max(|s_j|)={max_s:.2f}")
    print("  Too small: noise creates false 'new levels'. Too large: real changes vanish.")


# ============================================================================
# PLOTS
# ============================================================================

COLORS = {
    "surface": "#fcfcfb", "ink": "#0b0b0b", "ink2": "#52514e", "grid": "#e4e3df",
    "k": "#2a78d6", "trend": "#eb6834", "s": "#1baf7a",
    "flat": "#2a78d6", "rising": "#eb6834",
}

EXAMPLE_SEEDS = {"settling": 1, "drifting": 2, "accelerating": 3}


def _style(ax):
    ax.set_facecolor(COLORS["surface"])
    ax.grid(True, color=COLORS["grid"], linewidth=0.8)
    ax.set_axisbelow(True)
    for side in ("top", "right"):
        ax.spines[side].set_visible(False)
    for side in ("left", "bottom"):
        ax.spines[side].set_color(COLORS["ink2"])
    ax.tick_params(colors=COLORS["ink2"], labelsize=9)
    ax.xaxis.label.set_color(COLORS["ink2"])
    ax.yaxis.label.set_color(COLORS["ink2"])
    ax.title.set_color(COLORS["ink"])


def plot_trajectory(K: np.ndarray, title: str, settle: int = 4):
    """Left: K over time with the time-based reading. Right: first-arrival s_j."""
    import matplotlib.pyplot as plt
    from matplotlib.ticker import MaxNLocator

    profile = stability_profile(K, settle=settle)
    s_j = compute_s_j(extract_first_time_states(K[settle:]))
    old = first_arrival_reading(K[settle:])

    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 4.2), facecolor=COLORS["surface"],
                                   gridspec_kw={"width_ratios": [1.6, 1]})
    episodes = np.arange(len(K))
    ax1.axvspan(-0.5, settle - 0.5, color=COLORS["grid"], alpha=0.6, linewidth=0)
    ax1.text(settle / 2 - 0.5, 9.6, "settling", ha="center", va="top",
             fontsize=8, color=COLORS["ink2"])
    ax1.plot(episodes, K, color=COLORS["k"], linewidth=2, marker="o", markersize=3.5,
             label="K(i)")
    x = np.arange(settle, len(K))
    intercept = np.median(K[settle:] - profile.trend * x)
    ax1.plot(x, intercept + profile.trend * x, color=COLORS["trend"], linewidth=2,
             label="trend (Theil-Sen)")
    ax1.set_ylim(0, 10)
    ax1.set_xlabel("Episode (i)")
    ax1.set_ylabel("Adjustment K(i), 0-10")
    ax1.set_title(f"{title}: K over time", fontsize=11, loc="left")
    ax1.legend(loc="upper right", fontsize=8, frameon=False, labelcolor=COLORS["ink2"])
    reading = (f"time-based check: {profile.label}\n"
               f"level {profile.level:.1f}  trend {profile.trend:+.3f}/episode  "
               f"volatility {profile.volatility:.2f}")
    ax1.text(0.02, 0.04, reading, transform=ax1.transAxes, fontsize=8.5,
             color=COLORS["ink"], va="bottom",
             bbox=dict(boxstyle="round,pad=0.4", facecolor="white", edgecolor=COLORS["grid"]))
    _style(ax1)

    if s_j:
        ax2.plot(range(len(s_j)), s_j, color=COLORS["s"], linewidth=2, marker="o", markersize=4)
    ax2.axhline(0, color=COLORS["ink2"], linewidth=0.8)
    for limit in (-1, 1):
        ax2.axhline(limit, color=COLORS["ink2"], linewidth=0.8, linestyle="--")
    ax2.xaxis.set_major_locator(MaxNLocator(integer=True))
    ax2.set_xlabel("First-time level (j)")
    ax2.set_ylabel("s_j")
    ax2.set_title("Auxiliary: first-arrival s_j (after settling)", fontsize=11, loc="left")
    ax2.text(0.02, 0.04, f"first-arrival check: {old}\n(ignores time between levels)",
             transform=ax2.transAxes, fontsize=8.5, color=COLORS["ink"], va="bottom",
             bbox=dict(boxstyle="round,pad=0.4", facecolor="white", edgecolor=COLORS["grid"]))
    _style(ax2)
    fig.tight_layout()
    return fig


def plot_hypothesis(results):
    import matplotlib.pyplot as plt

    fig, ax = plt.subplots(figsize=(8, 5.5), facecolor=COLORS["surface"])
    groups = (("flat", "flat or falling", False), ("rising", "rising (incl. accelerating)", True))
    for color, name, rising in groups:
        pts = [(d, t) for d, t, lab in results if is_rising(lab) == rising]
        if pts:
            d, t = zip(*pts)
            ax.scatter(d, t, s=28, color=COLORS[color], alpha=0.8, label=name,
                       edgecolors=COLORS["surface"], linewidths=1)
    ax.axhline(0, color=COLORS["ink2"], linewidth=0.8)
    ax.axhline(0.05, color=COLORS["ink2"], linewidth=0.8, linestyle="--")
    ax.text(0.105, 0.052, "rising threshold (0.05)", fontsize=8, color=COLORS["ink2"], va="bottom")
    ax.set_xlabel("Initial Manhattan distance")
    ax.set_ylabel("Trend of K (points per episode)")
    ax.set_title("Hypothesis visualization: if distance led to rising adjustment",
                 fontsize=11, loc="left")
    corr = np.corrcoef([r[0] for r in results], [r[1] for r in results])[0, 1]
    ax.text(0.02, 0.96, f"Correlation {corr:.2f}\nBuilt in by assumption, not discovered",
            transform=ax.transAxes, fontsize=9, va="top", color=COLORS["ink"],
            bbox=dict(boxstyle="round,pad=0.4", facecolor="white", edgecolor=COLORS["grid"]))
    ax.legend(loc="lower right", fontsize=8, frameon=False, labelcolor=COLORS["ink2"])
    _style(ax)
    fig.tight_layout()
    return fig, corr


def example_trajectory(kind: str) -> np.ndarray:
    return generate_work_state_sequence(KINDS[kind], np.random.default_rng(EXAMPLE_SEEDS[kind]))


def save_figures(out_dir: Optional[str] = None):
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt

    out_dir = out_dir or os.path.join(os.path.dirname(os.path.abspath(__file__)),
                                      "..", "docs", "assets")
    figures = [
        ("Figure_1.png", plot_trajectory(example_trajectory("settling"), "Settling (stable fit)")),
        ("Figure_2.png", plot_trajectory(example_trajectory("drifting"), "Drifting (unstable fit)")),
        ("Figure_3.png", plot_hypothesis(hypothesis_visualization())[0]),
    ]
    for name, fig in figures:
        path = os.path.normpath(os.path.join(out_dir, name))
        fig.savefig(path, dpi=130, facecolor=COLORS["surface"])
        plt.close(fig)
        print(f"wrote {path}")


# ============================================================================
# REPORT
# ============================================================================

def describe(kind: str, K: np.ndarray, settle: int = 4):
    p = stability_profile(K, settle=settle)
    print(f"\n{kind}")
    print(f"  episodes after settling: {p.n_used}")
    print(f"  level {p.level:.2f}   trend {p.trend:+.3f}/episode   volatility {p.volatility:.2f}"
          f"   trend change {p.trend_change:+.3f}")
    print(f"  time-based check:      {p.label}")
    print(f"  first-arrival check:   {first_arrival_reading(K[settle:])}")


def main():
    if "--test" in sys.argv:
        run_tests()
        return
    if "--save-figures" in sys.argv:
        save_figures()
        return

    print("=" * 72)
    print("FIT AS DYNAMIC STABILITY - SYNTHETIC SIMULATION")
    print("=" * 72)
    print("Synthetic data only: each trajectory follows the assumption it illustrates.")

    for kind in ("settling", "drifting", "accelerating"):
        describe(kind, example_trajectory(kind))

    print("\nIssue #4 examples (quantize=0.5):")
    for K in ([0, 2, 1], [0, 1, 2, 3, 4]):
        s_j = compute_s_j(extract_first_time_states(K))
        p = stability_profile(K, settle=0)
        print(f"  K={K}: s_j={s_j} -> first-arrival says {first_arrival_reading(K)}; "
              f"time-based says {p.label}")

    quantize_sensitivity_demo()
    print_window_study(window_study())

    results = hypothesis_visualization()
    corr = np.corrcoef([r[0] for r in results], [r[1] for r in results])[0, 1]
    print(f"\nHypothesis visualization: correlation {corr:.2f} between distance and trend.")
    print("⚠️ This correlation was built into the simulation. Only real data can show one.")

    import matplotlib.pyplot as plt
    plot_trajectory(example_trajectory("settling"), "Settling (stable fit)")
    plot_trajectory(example_trajectory("drifting"), "Drifting (unstable fit)")
    plot_hypothesis(results)
    plt.show()


# ============================================================================
# UNIT TESTS
# ============================================================================

def test_compute_s_j_basic():
    # a = [0, 1, 3, 6] -> deltas [1, 2, 3] -> s_j [1, 1]
    s_j = compute_s_j([0.0, 1.0, 3.0, 6.0])
    assert len(s_j) == 2, f"Expected 2 s_j values, got {len(s_j)}"
    assert abs(s_j[0] - 1.0) < 1e-9 and abs(s_j[1] - 1.0) < 1e-9, s_j
    print("✅ test_compute_s_j_basic passed")


def test_bounded_criterion():
    assert is_bounded([0.1, -0.2, 0.15, -0.1], threshold=1.0)
    assert not is_bounded([0.5, 1.2, 2.5, 4.0], threshold=1.0)
    print("✅ test_bounded_criterion passed")


def test_extract_first_time_states():
    # quantize 0.5: L = [0, 1, 1, 2, 2, 3] -> first-time 0, 1, 2, 3
    a_seq = extract_first_time_states(np.array([0.3, 0.7, 0.9, 1.3, 1.1, 1.8]), quantize=0.5)
    assert a_seq == [0.0, 0.5, 1.0, 1.5], f"Unexpected sequence: {a_seq}"
    print("✅ test_extract_first_time_states passed")


def test_issue_4_first_arrival_examples():
    # The two examples from Issue #4, pinned so the known limits stay documented.
    s_j = compute_s_j(extract_first_time_states([0, 2, 1], quantize=0.5))
    assert s_j == [-3.0], s_j
    assert first_arrival_reading([0, 2, 1]) == "unstable"  # though adjustment is bounded
    s_j = compute_s_j(extract_first_time_states([0, 1, 2, 3, 4], quantize=0.5))
    assert s_j == [0.0, 0.0, 0.0], s_j
    assert first_arrival_reading([0, 1, 2, 3, 4]) == "stable"  # though it keeps rising
    print("✅ test_issue_4_first_arrival_examples passed")


def test_issue_4_examples_time_based():
    # Three readings are too few to say anything about boundedness.
    assert stability_profile([0, 2, 1], settle=0).label == "too short"
    # The same bounded pattern, observed for longer, reads as flat...
    assert stability_profile([0, 2, 1] * 4, settle=0).label == "flat"
    # ...while the first-arrival check still calls it unstable.
    assert first_arrival_reading([0, 2, 1] * 4) == "unstable"
    # Steadily rising adjustment reads as rising.
    p = stability_profile([0, 1, 2, 3, 4], settle=0)
    assert p.label == "rising" and abs(p.trend - 1.0) < 1e-9, p
    print("✅ test_issue_4_examples_time_based passed")


def test_settling_generator_returns_to_baseline():
    # With noise off, the settling case ends at its baseline however long it runs.
    # (The Phase 0 generator at stability_strength=0.8 reached 1.64 at episode 50
    # and 18.52 at episode 500.)
    config = replace(KINDS["settling"], noise=0.0, n_episodes=501)
    K = generate_work_state_sequence(config)
    assert abs(K[50] - config.baseline) < 1e-6, K[50]
    assert abs(K[500] - config.baseline) < 1e-9, K[500]
    print("✅ test_settling_generator_returns_to_baseline passed")


def test_drifting_generator_rises_at_drift_rate():
    config = replace(KINDS["drifting"], noise=0.0, n_episodes=60)
    K = generate_work_state_sequence(config)
    assert abs((K[59] - K[58]) - config.drift) < 1e-6, K[59] - K[58]
    assert abs(stability_profile(K).trend - config.drift) < 1e-3
    print("✅ test_drifting_generator_rises_at_drift_rate passed")


def test_theil_sen_resists_outlier():
    y = 2.0 * np.arange(12) + 1.0
    y[5] = 100.0
    assert abs(theil_sen_slope(y) - 2.0) < 1e-9
    print("✅ test_theil_sen_resists_outlier passed")


def test_profile_reads_clean_lines():
    p = stability_profile(2.0 + 0.1 * np.arange(20), settle=0)
    assert p.label == "rising" and abs(p.trend - 0.1) < 1e-9 and p.volatility < 1e-9, p
    p = stability_profile(np.full(20, 4.0), settle=0)
    assert p.label == "flat" and p.trend == 0.0 and p.volatility == 0.0 and p.level == 4.0, p
    p = stability_profile(2.0 + 0.004 * np.arange(30) ** 2, settle=0)
    assert p.label == "accelerating", p
    print("✅ test_profile_reads_clean_lines passed")


def test_too_short_window():
    p = stability_profile(np.arange(8.0), settle=4)
    assert p.n_used == 4 and p.label == "too short", p
    print("✅ test_too_short_window passed")


def test_profile_separates_kinds_over_50_episodes():
    rng = np.random.default_rng(0)
    rates = {}
    for kind, base in KINDS.items():
        labels = [stability_profile(generate_work_state_sequence(replace(base, n_episodes=54), rng)).label
                  for _ in range(200)]
        rates[kind] = (sum(is_rising(lab) for lab in labels) / 200, labels.count("accelerating") / 200)
    assert rates["settling"][0] < 0.05, rates
    assert rates["noisy"][0] < 0.10, rates
    assert rates["drifting"][0] > 0.95, rates
    assert rates["accelerating"][1] > 0.80, rates
    print("✅ test_profile_separates_kinds_over_50_episodes passed")


def test_noisy_flat_is_not_rising():
    # The Phase 0 failure: noisy but flat adjustment looked unstable.
    rng = np.random.default_rng(1)
    config = replace(KINDS["noisy"], n_episodes=54)
    old_unstable = new_rising = 0
    for _ in range(200):
        K = generate_work_state_sequence(config, rng)
        old_unstable += first_arrival_reading(K[4:]) == "unstable"
        new_rising += is_rising(stability_profile(K).label)
    assert old_unstable > 100, old_unstable
    assert new_rising < 20, new_rising
    print("✅ test_noisy_flat_is_not_rising passed")


def test_window_study_shape():
    rows = window_study(windows=(8, 50), n_people=50)
    assert len(rows) == 2 * len(KINDS)
    assert all(0.0 <= r["rising"] <= 1.0 and r["accelerating"] <= r["rising"] for r in rows)
    print("✅ test_window_study_shape passed")


def run_tests():
    print("\n" + "=" * 72)
    print("RUNNING UNIT TESTS")
    print("=" * 72 + "\n")
    test_compute_s_j_basic()
    test_bounded_criterion()
    test_extract_first_time_states()
    test_issue_4_first_arrival_examples()
    test_issue_4_examples_time_based()
    test_settling_generator_returns_to_baseline()
    test_drifting_generator_rises_at_drift_rate()
    test_theil_sen_resists_outlier()
    test_profile_reads_clean_lines()
    test_too_short_window()
    test_profile_separates_kinds_over_50_episodes()
    test_noisy_flat_is_not_rising()
    test_window_study_shape()
    print("\n✅ All unit tests passed!")


if __name__ == "__main__":
    main()
