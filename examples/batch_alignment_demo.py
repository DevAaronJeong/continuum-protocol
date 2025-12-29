"""
Batch Alignment Demo

⚠️ THIS IS A CONCEPTUAL EXPLORATION, NOT PRODUCTION CODE ⚠️

This demonstrates how alignment could work with multiple options:
- One person
- Multiple work opportunities
- Find best fits (not "best jobs")

Key insight: The same work can rank differently for different people.
There are no universally "good" or "bad" jobs — only contextual alignment.

Usage:
    python examples/batch_alignment_demo.py
"""

import sys
import os

# Add parent directory to path to import alignment_engine
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from src.alignment_engine import LifestyleVector, find_best_matches, print_alignment_report


def main():
    print("=" * 70)
    print("BATCH ALIGNMENT DEMO")
    print("=" * 70)
    print()
    print("⚠️  Conceptual prototype — exploring ideas, not solving problems")
    print()
    
    # Define a person
    person = LifestyleVector(
        energy_rhythm="evening",
        time_flexibility=0.7,
        interaction_density=0.4,
        change_tolerance=0.5,
        intensity_preference=0.6,
        consistency_score=0.75,
        label="Alex (Evening-oriented, Moderate Flexibility)"
    )
    
    print(f"Person Profile: {person.label}")
    print(f"  Energy: {person.energy_rhythm}")
    print(f"  Flexibility: {person.time_flexibility:.2f}")
    print(f"  Interaction: {person.interaction_density:.2f}")
    print(f"  Change Tolerance: {person.change_tolerance:.2f}")
    print(f"  Intensity: {person.intensity_preference:.2f}")
    print()
    print("-" * 70)
    print()
    
    # Define multiple work opportunities
    work_options = [
        LifestyleVector(
            energy_rhythm="distributed",
            time_flexibility=0.9,
            interaction_density=0.3,
            change_tolerance=0.4,
            intensity_preference=0.5,
            consistency_score=0.8,
            label="Remote Async Team",
            profile_type="work"
        ),
        LifestyleVector(
            energy_rhythm="morning",
            time_flexibility=0.2,
            interaction_density=0.8,
            change_tolerance=0.2,
            intensity_preference=0.6,
            consistency_score=0.9,
            label="Traditional Office (9-5)",
            profile_type="work"
        ),
        LifestyleVector(
            energy_rhythm="evening",
            time_flexibility=0.8,
            interaction_density=0.5,
            change_tolerance=0.7,
            intensity_preference=0.8,
            consistency_score=0.5,
            label="Late-Night Startup",
            profile_type="work"
        ),
        LifestyleVector(
            energy_rhythm="afternoon",
            time_flexibility=0.5,
            interaction_density=0.6,
            change_tolerance=0.5,
            intensity_preference=0.5,
            consistency_score=0.7,
            label="Flexible Agency",
            profile_type="work"
        ),
        LifestyleVector(
            energy_rhythm="distributed",
            time_flexibility=1.0,
            interaction_density=0.2,
            change_tolerance=0.3,
            intensity_preference=0.4,
            consistency_score=0.9,
            label="Freelance Platform",
            profile_type="work"
        ),
    ]
    
    print(f"Available Work Opportunities: {len(work_options)}")
    for i, work in enumerate(work_options, 1):
        print(f"  {i}. {work.label}")
    print()
    print("-" * 70)
    print()
    
    # Find best matches
    print("Finding top 3 matches...")
    print()
    matches = find_best_matches(person, work_options, top_n=3)
    
    print("=" * 70)
    print("TOP MATCHES (FOR THIS PERSON)")
    print("=" * 70)
    print()
    print("Remember: These rankings are contextual, not absolute.")
    print("A different person would get different results.")
    print()
    
    for rank, (work, result) in enumerate(matches, 1):
        print(f"RANK {rank}: {work.label}")
        print(f"  Score: {result['score']:.3f}")
        print(f"  {result['recommendation']}")
        print(f"  Reasons:")
        for reason in result['explanation']:
            print(f"    {reason}")
        print()
    
    print("-" * 70)
    print()
    
    # Show detailed report for best match
    print("DETAILED REPORT FOR BEST MATCH:")
    print()
    best_work, best_result = matches[0]
    print_alignment_report(person, best_work)
    
    print()
    print("=" * 70)
    print("INSIGHT:")
    print("  Notice how different work environments score differently")
    print("  for the same person. There's no 'best job' in absolute terms —")
    print("  only 'best fit for this person, right now.'")
    print()
    print("  If we ran this with a different person (e.g., a morning person"),
    print("  who prefers high collaboration), the rankings would change.")
    print("=" * 70)


if __name__ == "__main__":
    main()
