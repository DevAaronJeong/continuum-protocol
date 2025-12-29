"""
Simple Lifestyle Matching Example

This demonstrates the core idea of continuum-protocol:
matching people to work based on lifestyle rhythms, not skills.

Run this file to see how alignment scoring works.
"""

from dataclasses import dataclass
from typing import Literal
import math


@dataclass
class LifestyleVector:
    """
    Represents a person or organization's lifestyle configuration.
    
    All values are normalized between 0.0 and 1.0 for comparability.
    """
    
    # When does peak energy/activity occur?
    energy_rhythm: Literal["morning", "afternoon", "evening", "distributed"]
    
    # How flexible is the schedule? (0 = rigid, 1 = fully flexible)
    time_flexibility: float
    
    # Communication frequency (0 = solo/async, 1 = constant interaction)
    interaction_density: float
    
    # Preference for stability vs. variety (0 = routine, 1 = chaos-tolerant)
    change_tolerance: float
    
    # Work intensity preference (0 = low-key, 1 = high-intensity sprints)
    intensity_preference: float
    
    # Consistency of lifestyle (0 = erratic, 1 = highly stable)
    consistency_score: float = 0.5


def energy_rhythm_to_value(rhythm: str) -> float:
    """Convert categorical rhythm to numeric value for comparison."""
    mapping = {
        "morning": 0.0,
        "afternoon": 0.33,
        "evening": 0.66,
        "distributed": 1.0
    }
    return mapping.get(rhythm, 0.5)


def calculate_alignment(person: LifestyleVector, work: LifestyleVector) -> dict:
    """
    Calculate alignment between a person and a work opportunity.
    
    Returns a dict with:
    - overall_score: 0.0 to 1.0 (higher = better alignment)
    - breakdown: individual dimension scores
    - explanation: human-readable reasons
    """
    
    # Convert energy rhythms to comparable values
    person_energy = energy_rhythm_to_value(person.energy_rhythm)
    work_energy = energy_rhythm_to_value(work.energy_rhythm)
    
    # Calculate dimension-wise alignment (1.0 = perfect match, 0.0 = complete mismatch)
    energy_alignment = 1.0 - abs(person_energy - work_energy)
    flexibility_alignment = 1.0 - abs(person.time_flexibility - work.time_flexibility)
    interaction_alignment = 1.0 - abs(person.interaction_density - work.interaction_density)
    change_alignment = 1.0 - abs(person.change_tolerance - work.change_tolerance)
    intensity_alignment = 1.0 - abs(person.intensity_preference - work.intensity_preference)
    
    # Weight dimensions (you can adjust these)
    weights = {
        'energy': 0.25,
        'flexibility': 0.15,
        'interaction': 0.20,
        'change': 0.20,
        'intensity': 0.20
    }
    
    # Calculate weighted overall score
    overall_score = (
        energy_alignment * weights['energy'] +
        flexibility_alignment * weights['flexibility'] +
        interaction_alignment * weights['interaction'] +
        change_alignment * weights['change'] +
        intensity_alignment * weights['intensity']
    )
    
    # Adjust for consistency (stable lifestyles get a slight boost)
    consistency_multiplier = 0.9 + (person.consistency_score * 0.1)
    overall_score *= consistency_multiplier
    
    # Generate explanation
    explanations = []
    
    if energy_alignment > 0.8:
        explanations.append(f"✓ Energy rhythms align well ({person.energy_rhythm} ≈ {work.energy_rhythm})")
    elif energy_alignment < 0.5:
        explanations.append(f"✗ Energy rhythm mismatch ({person.energy_rhythm} vs {work.energy_rhythm})")
    
    if interaction_alignment > 0.8:
        explanations.append("✓ Communication density is a good match")
    elif interaction_alignment < 0.5:
        explanations.append("✗ Communication preferences differ significantly")
    
    if intensity_alignment > 0.8:
        explanations.append("✓ Work intensity matches your preference")
    elif intensity_alignment < 0.5:
        explanations.append("✗ Work intensity may not suit your style")
    
    if person.consistency_score > 0.7:
        explanations.append("✓ Your consistency suggests long-term alignment potential")
    
    return {
        'overall_score': overall_score,
        'breakdown': {
            'energy': energy_alignment,
            'flexibility': flexibility_alignment,
            'interaction': interaction_alignment,
            'change': change_alignment,
            'intensity': intensity_alignment
        },
        'explanations': explanations
    }


def interpret_score(score: float) -> str:
    """Human-readable interpretation of alignment score."""
    if score >= 0.80:
        return "🟢 Strong alignment — worth serious exploration"
    elif score >= 0.60:
        return "🟡 Moderate alignment — worth trying short-term"
    elif score >= 0.40:
        return "🟠 Weak alignment — proceed with caution"
    else:
        return "🔴 Poor alignment — probably not a good fit right now"


def main():
    """Run example scenarios."""
    
    print("=" * 60)
    print("continuum-protocol: Simple Matching Example")
    print("=" * 60)
    print()
    
    # Scenario 1: Good match
    print("Scenario 1: Night owl seeking async remote work")
    print("-" * 60)
    
    person_1 = LifestyleVector(
        energy_rhythm="evening",
        time_flexibility=0.9,
        interaction_density=0.2,  # Prefers solo/async work
        change_tolerance=0.4,      # Likes routine
        intensity_preference=0.6,  # Moderate intensity
        consistency_score=0.8      # Very consistent lifestyle
    )
    
    work_1 = LifestyleVector(
        energy_rhythm="distributed",  # No fixed hours
        time_flexibility=0.9,
        interaction_density=0.3,      # Mostly async
        change_tolerance=0.3,          # Stable processes
        intensity_preference=0.5,      # Steady pace
        consistency_score=0.7          # Reliable structure
    )
    
    result_1 = calculate_alignment(person_1, work_1)
    print(f"Alignment Score: {result_1['overall_score']:.2f}")
    print(f"Assessment: {interpret_score(result_1['overall_score'])}")
    print("\nReasons:")
    for reason in result_1['explanations']:
        print(f"  {reason}")
    
    print("\n")
    
    # Scenario 2: Poor match
    print("Scenario 2: Morning person applying to late-night team")
    print("-" * 60)
    
    person_2 = LifestyleVector(
        energy_rhythm="morning",
        time_flexibility=0.3,      # Prefers fixed schedule
        interaction_density=0.7,   # Likes collaboration
        change_tolerance=0.2,      # Very routine-oriented
        intensity_preference=0.4,  # Low intensity
        consistency_score=0.9
    )
    
    work_2 = LifestyleVector(
        energy_rhythm="evening",
        time_flexibility=0.8,
        interaction_density=0.9,   # Constant meetings
        change_tolerance=0.8,      # Fast-moving, chaotic
        intensity_preference=0.9,  # High-intensity sprints
        consistency_score=0.4
    )
    
    result_2 = calculate_alignment(person_2, work_2)
    print(f"Alignment Score: {result_2['overall_score']:.2f}")
    print(f"Assessment: {interpret_score(result_2['overall_score'])}")
    print("\nReasons:")
    for reason in result_2['explanations']:
        print(f"  {reason}")
    
    print("\n")
    print("=" * 60)
    print("Key Insight:")
    print("  Neither person nor work is 'better' than the other.")
    print("  We only measure alignment at this moment in time.")
    print("=" * 60)


if __name__ == "__main__":
    main()
