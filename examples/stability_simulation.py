"""
Stability Simulation - Phase 0

Synthetic data exploration of fit as dynamic stability.

This script generates synthetic trajectories to:
1. Visualize what stable vs unstable fit looks like
2. Test if Manhattan Distance correlates with s_j behavior
3. Debug measurement protocols before human experiments

⚠️ IMPORTANT: This is NOT data analysis.
This is "hypothesis visualization" - showing what data WOULD look like
IF the hypothesis (distance → instability) were true.

Real correlation testing requires actual human data where the relationship
between initial distance and s_j is discovered, not assumed.

Usage:
    python examples/stability_simulation.py
    python examples/stability_simulation.py --test  # Run unit tests
"""

import numpy as np
import matplotlib.pyplot as plt
from dataclasses import dataclass
from typing import List, Tuple


@dataclass
class TrajectoryConfig:
    """Configuration for synthetic trajectory generation."""
    n_episodes: int = 50  # Number of work episodes to simulate
    stability_strength: float = 0.5  # 0=very unstable, 1=very stable
    initial_distance: float = 0.3  # Manhattan Distance at t=0
    noise_level: float = 0.1


def generate_work_state_sequence(config: TrajectoryConfig) -> np.ndarray:
    """
    Generate K(i) - the work-state readout sequence.
    
    stability_strength controls the dynamics:
    - High (→1): Strong mean reversion, bounded variance
    - Low (→0): Drift with increasing variance
    
    This models the "adjustment effort" someone experiences.
    """
    K = np.zeros(config.n_episodes)
    K[0] = config.initial_distance  # Start from Manhattan Distance
    
    mean_reversion_rate = config.stability_strength * 0.2
    drift_rate = (1 - config.stability_strength) * 0.03
    
    for i in range(1, config.n_episodes):
        # Noise grows with instability
        variance_growth = 1 + (1 - config.stability_strength) * i * 0.05
        noise = np.random.normal(0, config.noise_level * variance_growth)
        
        # Mean reversion (stability) vs. drift (instability)
        mean_reversion = -mean_reversion_rate * K[i-1]
        drift = drift_rate * i
        
        K[i] = K[i-1] + mean_reversion + drift + noise
    
    return np.abs(K)  # Work-state readout is always positive


def extract_first_time_states(K: np.ndarray, quantize: float = 0.5) -> List[float]:
    """
    Extract a_j - sequence of first-time-seen readout levels.
    
    L(i) = floor(K(i) / quantize)
    a_j = unique values encountered for the first time
    
    Args:
        quantize: Granularity of state detection (default 0.5)
                 Smaller values = more sensitive to state changes
    """
    L = np.floor(K / quantize)
    seen = set()
    a_sequence = []
    
    for level in L:
        if level not in seen:
            seen.add(level)
            a_sequence.append(level * quantize)
    
    return a_sequence


def compute_s_j(a_sequence: List[float]) -> List[float]:
    """
    Compute s_j - change in step size (acceleration of adjustment demands).
    
    Delta_j = a_{j+1} - a_j  (step size between new states)
    s_j = Delta_{j+1} - Delta_j  (change in step size)
    
    This is the "second derivative" - measures if adjustment demands
    are staying constant (stable) or compounding (unstable).
    """
    if len(a_sequence) < 3:
        return []
    
    deltas = [a_sequence[i+1] - a_sequence[i] for i in range(len(a_sequence)-1)]
    s_j = [deltas[i+1] - deltas[i] for i in range(len(deltas)-1)]
    
    return s_j


def is_bounded(s_j: List[float], threshold: float = 1.0) -> bool:
    """
    Test stability criterion: Is |s_j| bounded?
    
    Simple heuristic: check if max(|s_j|) stays below threshold.
    More sophisticated tests could check for trends, variance growth, etc.
    """
    if not s_j:
        return True
    return max(abs(s) for s in s_j) < threshold


def plot_trajectory(K: np.ndarray, s_j: List[float], title: str):
    """Plot K(i) and s_j side by side."""
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 4))
    
    # Plot K(i) - adjustment effort over time
    ax1.plot(K, marker='o', markersize=3)
    ax1.set_xlabel('Episode (i)')
    ax1.set_ylabel('Work-state K(i)')
    ax1.set_title(f'{title} - Adjustment Effort')
    ax1.grid(True, alpha=0.3)
    
    # Plot s_j - acceleration of adjustment
    if s_j:
        ax2.plot(s_j, marker='o', markersize=4, color='red')
        ax2.axhline(y=0, color='black', linestyle='--', alpha=0.3)
        ax2.set_xlabel('Step (j)')
        ax2.set_ylabel('Acceleration s_j')
        ax2.set_title(f'{title} - Adjustment Acceleration')
        ax2.grid(True, alpha=0.3)
    
    plt.tight_layout()
    plt.show()


def run_single_trajectory(stability_strength: float, initial_distance: float):
    """Run and visualize one trajectory."""
    config = TrajectoryConfig(
        n_episodes=50,
        stability_strength=stability_strength,
        initial_distance=initial_distance
    )
    
    K = generate_work_state_sequence(config)
    a_sequence = extract_first_time_states(K)
    s_j = compute_s_j(a_sequence)
    bounded = is_bounded(s_j)
    
    is_stable = stability_strength > 0.5
    title = "✅ Stable Fit" if is_stable else "❌ Unstable Fit"
    
    print(f"\n{title}")
    print(f"  Stability strength: {stability_strength:.2f}")
    print(f"  Initial distance: {initial_distance:.2f}")
    print(f"  Episodes: {len(K)}")
    print(f"  Unique states: {len(a_sequence)}")
    print(f"  s_j values: {len(s_j)}")
    print(f"  Bounded: {bounded}")
    print(f"  max(|s_j|): {max(abs(s) for s in s_j) if s_j else 'N/A'}")
    
    plot_trajectory(K, s_j, title)


def explore_hypothesis_visualization(n_samples: int = 100):
    """
    ⚠️ HYPOTHESIS VISUALIZATION (NOT DATA ANALYSIS)
    
    This generates data ASSUMING the hypothesis is true:
    "Large initial Manhattan Distance → Unbounded s_j"
    
    Purpose: Show what we EXPECT to see if hypothesis holds.
    
    This is NOT a correlation test. Real testing requires actual human data
    where the relationship is discovered, not assumed.
    """
    print("\n" + "⚠️" * 30)
    print("HYPOTHESIS VISUALIZATION (Not empirical correlation test)")
    print("Generating data WITH built-in assumption: distance → instability")
    print("⚠️" * 30 + "\n")
    
    results = []
    
    for _ in range(n_samples):
        initial_dist = np.random.uniform(0.1, 0.9)
        
        # ASSUMPTION INJECTED HERE:
        # We're making stability inversely proportional to distance
        # This is what we WANT to test, not what we should assume!
        stability_strength = 1 - initial_dist  # Direct inverse relationship
        
        config = TrajectoryConfig(
            n_episodes=50,
            stability_strength=stability_strength,
            initial_distance=initial_dist
        )
        
        K = generate_work_state_sequence(config)
        a_sequence = extract_first_time_states(K)
        s_j = compute_s_j(a_sequence)
        
        max_s_j = max(abs(s) for s in s_j) if s_j else 0
        results.append((initial_dist, max_s_j, stability_strength))
    
    # Plot "correlation" (which we artificially created)
    distances = [r[0] for r in results]
    max_s_js = [r[1] for r in results]
    
    plt.figure(figsize=(8, 6))
    plt.scatter(distances, max_s_js, alpha=0.5)
    plt.xlabel('Initial Manhattan Distance')
    plt.ylabel('max(|s_j|) - Adjustment Acceleration')
    plt.title('Hypothesis Visualization: If Distance → Instability Were True')
    plt.grid(True, alpha=0.3)
    
    correlation = np.corrcoef(distances, max_s_js)[0, 1]
    
    plt.text(0.05, 0.95, 
             f'Correlation: {correlation:.3f}\n(Built-in by assumption)', 
             transform=plt.gca().transAxes, 
             bbox=dict(boxstyle='round', facecolor='yellow', alpha=0.7),
             fontsize=10)
    
    plt.show()
    
    print(f"\n'Correlation': {correlation:.3f}")
    print("⚠️ This correlation is ARTIFICIAL - we built it into the simulation.")
    print("Real test requires human data where relationship is discovered, not assumed.")


def test_quantize_sensitivity():
    """
    Test how quantize parameter affects a_j extraction.
    
    Smaller quantize = more sensitive to state changes
    Larger quantize = less sensitive (groups similar states)
    
    This matters because different people may have different
    "sensitivity" to perceiving "new states" in their work.
    """
    print("\n" + "=" * 60)
    print("QUANTIZE SENSITIVITY ANALYSIS")
    print("=" * 60)
    
    # Generate one trajectory
    config = TrajectoryConfig(n_episodes=50, stability_strength=0.3)
    K = generate_work_state_sequence(config)
    
    quantize_values = [0.1, 0.25, 0.5, 1.0, 2.0]
    
    print(f"\nFor the same K(i) trajectory:")
    for q in quantize_values:
        a_seq = extract_first_time_states(K, quantize=q)
        s_j = compute_s_j(a_seq)
        max_s = max(abs(s) for s in s_j) if s_j else 0
        
        print(f"  quantize={q:4.2f} → {len(a_seq):2d} unique states, "
              f"{len(s_j):2d} s_j values, max(|s_j|)={max_s:.3f}")
    
    print("\nInsight: Quantize parameter trades off:")
    print("  - Too small: Noise creates false 'new states'")
    print("  - Too large: Miss real transitions")
    print("  - Optimal value likely needs empirical tuning")


# ============================================================================
# UNIT TESTS
# ============================================================================

def test_compute_s_j_basic():
    """Test s_j computation with known values."""
    # a_sequence: [0, 1, 3, 6]
    # deltas: [1, 2, 3]
    # s_j: [1, 1]  (differences of deltas)
    
    a_seq = [0.0, 1.0, 3.0, 6.0]
    s_j = compute_s_j(a_seq)
    
    assert len(s_j) == 2, f"Expected 2 s_j values, got {len(s_j)}"
    assert abs(s_j[0] - 1.0) < 0.001, f"Expected s_j[0]=1.0, got {s_j[0]}"
    assert abs(s_j[1] - 1.0) < 0.001, f"Expected s_j[1]=1.0, got {s_j[1]}"
    
    print("✅ test_compute_s_j_basic passed")


def test_bounded_criterion():
    """Test stability criterion."""
    s_j_stable = [0.1, -0.2, 0.15, -0.1]  # Bounded
    s_j_unstable = [0.5, 1.2, 2.5, 4.0]   # Unbounded
    
    assert is_bounded(s_j_stable, threshold=1.0) == True
    assert is_bounded(s_j_unstable, threshold=1.0) == False
    
    print("✅ test_bounded_criterion passed")


def test_extract_first_time_states():
    """Test a_j extraction logic."""
    K = np.array([0.3, 0.7, 0.9, 1.3, 1.1, 1.8])
    # With quantize=0.5:
    # L = [0, 1, 1, 2, 2, 3]
    # First-time: 0, 1, 2, 3
    # a_j = [0.0, 0.5, 1.0, 1.5]
    
    a_seq = extract_first_time_states(K, quantize=0.5)
    
    assert len(a_seq) == 4, f"Expected 4 unique states, got {len(a_seq)}"
    assert a_seq == [0.0, 0.5, 1.0, 1.5], f"Unexpected sequence: {a_seq}"
    
    print("✅ test_extract_first_time_states passed")


def run_tests():
    """Run all unit tests."""
    print("\n" + "=" * 60)
    print("RUNNING UNIT TESTS")
    print("=" * 60 + "\n")
    
    test_compute_s_j_basic()
    test_bounded_criterion()
    test_extract_first_time_states()
    
    print("\n✅ All unit tests passed!")


# ============================================================================
# MAIN
# ============================================================================

def main():
    """Run stability simulations."""
    import sys
    
    if '--test' in sys.argv:
        run_tests()
        return
    
    print("=" * 60)
    print("FIT AS DYNAMIC STABILITY - PHASE 0 SIMULATION")
    print("=" * 60)
    
    # Demo 1: Stable trajectory
    print("\n" + "-" * 60)
    print("DEMO 1: Stable System")
    print("-" * 60)
    run_single_trajectory(stability_strength=0.8, initial_distance=0.2)
    
    # Demo 2: Unstable trajectory
    print("\n" + "-" * 60)
    print("DEMO 2: Unstable System")
    print("-" * 60)
    run_single_trajectory(stability_strength=0.2, initial_distance=0.6)
    
    # Demo 3: Quantize sensitivity
    test_quantize_sensitivity()
    
    # Demo 4: Hypothesis visualization (WITH WARNING)
    print("\n" + "-" * 60)
    print("DEMO 3: Hypothesis Visualization")
    print("-" * 60)
    explore_hypothesis_visualization(n_samples=200)
    
    print("\n" + "=" * 60)
    print("Phase 0 Complete!")
    print("=" * 60)
    print("\nNext steps:")
    print("1. Refine quantize parameter based on sensitivity analysis")
    print("2. Design human measurement protocol (Phase 1)")
    print("3. Test with REAL data where correlation is discovered, not assumed")


if __name__ == "__main__":
    main()
