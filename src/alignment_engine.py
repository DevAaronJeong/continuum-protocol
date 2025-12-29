"""
Continuum Protocol - Alignment Engine (Conceptual Prototype)

⚠️ THIS IS NOT PRODUCTION CODE ⚠️

This is a conceptual exploration of how lifestyle-based alignment
could be expressed in code. It is intentionally simple, incomplete,
and designed to spark discussion rather than solve problems.

Purpose:
- Explore how "rhythms" could be modeled as vectors
- Demonstrate alignment calculation (not optimization)
- Show explainability (why a match works/doesn't work)
- Provoke questions about what we're missing

What this is NOT:
- A production-ready matching system
- An AI/ML solution
- A hiring tool
- A complete implementation

What this IS:
- A thought experiment in code form
- An invitation to critique and improve
- A starting point for exploring "work as a state"

Philosophy:
- No rankings (good/bad jobs don't exist)
- Only alignment (how well do rhythms match right now?)
- Time-aware (alignment changes over time)
- Explainable (always show why)

Usage:
    from alignment_engine import LifestyleVector, calculate_alignment
    
    person = LifestyleVector(...)
    work = LifestyleVector(...)
    
    result = calculate_alignment(person, work)
    print(result['score'], result['explanation'])
"""

from dataclasses import dataclass
from typing import Literal, Dict, List, Tuple
import math


# ============================================================================
# CORE DATA MODEL
# ============================================================================

@dataclass
class LifestyleVector:
    """
    Represents the lifestyle configuration of a person or organization.
    
    All numeric values are normalized to [0.0, 1.0] for comparability.
    
    Attributes:
        energy_rhythm: When peak activity occurs
        time_flexibility: How rigid the schedule is (0=fixed, 1=flexible)
        interaction_density: Communication frequency (0=solo, 1=constant)
        change_tolerance: Comfort with unpredictability (0=routine, 1=chaos-ok)
        intensity_preference: Work pace preference (0=steady, 1=sprints)
        consistency_score: How stable the lifestyle is (0=erratic, 1=stable)
        
    Examples:
        >>> # A night owl who prefers solo work
        >>> person = LifestyleVector(
        ...     energy_rhythm="evening",
        ...     time_flexibility=0.8,
        ...     interaction_density=0.2,
        ...     change_tolerance=0.4,
        ...     intensity_preference=0.5,
        ...     consistency_score=0.7
        ... )
    """
    
    energy_rhythm: Literal["morning", "afternoon", "evening", "distributed"]
    time_flexibility: float
    interaction_density: float
    change_tolerance: float
    intensity_preference: float
    consistency_score: float = 0.5
    
    # Metadata (not used in calculations)
    label: str = ""
    profile_type: Literal["person", "work"] = "person"
    
    def __post_init__(self):
        """Validate that all numeric values are in [0, 1]."""
        for field in ['time_flexibility', 'interaction_density', 
                      'change_tolerance', 'intensity_preference', 'consistency_score']:
            value = getattr(self, field)
            if not 0.0 <= value <= 1.0:
                raise ValueError(f"{field} must be between 0.0 and 1.0, got {value}")


# ============================================================================
# ALIGNMENT CALCULATION
# ============================================================================

def _energy_rhythm_distance(rhythm1: str, rhythm2: str) -> float:
    """
    Calculate distance between two energy rhythms.
    
    Rhythms are mapped to a circular space where:
    - morning -> 0.0
    - afternoon -> 0.33
    - evening -> 0.66
    - distributed -> 0.5 (center point, compatible with all)
    
    Returns:
        Distance in [0, 1] where 0 = perfect match, 1 = worst match
    """
    mapping = {
        "morning": 0.0,
        "afternoon": 0.33,
        "evening": 0.66,
        "distributed": 0.5  # Center point, works with all
    }
    
    r1 = mapping.get(rhythm1, 0.5)
    r2 = mapping.get(rhythm2, 0.5)
    
    # Special case: "distributed" has lower distance to everything
    if rhythm1 == "distributed" or rhythm2 == "distributed":
        return abs(r1 - r2) * 0.5  # Half penalty
    
    return abs(r1 - r2)


def calculate_alignment(
    person: LifestyleVector,
    work: LifestyleVector,
    weights: Dict[str, float] = None
) -> Dict:
    """
    Calculate alignment between a person and work opportunity.
    
    Note: This uses weighted Manhattan distance (sum of absolute differences)
    rather than cosine similarity. We chose this because:
    1. It's more interpretable (each dimension matters independently)
    2. It naturally produces scores in [0, 1]
    3. It allows us to weight dimensions differently
    
    Alignment is measured across multiple dimensions:
    1. Energy rhythm compatibility
    2. Schedule flexibility match
    3. Communication style alignment
    4. Change tolerance compatibility
    5. Intensity preference match
    
    Args:
        person: The person's lifestyle vector
        work: The work opportunity's lifestyle vector
        weights: Optional dimension weights (default: balanced)
        
    Returns:
        Dictionary containing:
        - 'score': Overall alignment (0.0 to 1.0)
        - 'breakdown': Per-dimension scores
        - 'explanation': Human-readable reasons
        - 'recommendation': What to do next
        
    Examples:
        >>> person = LifestyleVector(energy_rhythm="evening", ...)
        >>> work = LifestyleVector(energy_rhythm="distributed", ...)
        >>> result = calculate_alignment(person, work)
        >>> print(f"Alignment: {result['score']:.2f}")
    """
    
    # Default weights (can be tuned)
    if weights is None:
        weights = {
            'energy': 0.25,
            'flexibility': 0.15,
            'interaction': 0.20,
            'change': 0.20,
            'intensity': 0.20
        }
    
    # Calculate per-dimension alignment (1.0 = perfect, 0.0 = mismatch)
    energy_dist = _energy_rhythm_distance(person.energy_rhythm, work.energy_rhythm)
    energy_align = 1.0 - energy_dist
    
    flexibility_align = 1.0 - abs(person.time_flexibility - work.time_flexibility)
    interaction_align = 1.0 - abs(person.interaction_density - work.interaction_density)
    change_align = 1.0 - abs(person.change_tolerance - work.change_tolerance)
    intensity_align = 1.0 - abs(person.intensity_preference - work.intensity_preference)
    
    # Weighted overall score
    base_score = (
        energy_align * weights['energy'] +
        flexibility_align * weights['flexibility'] +
        interaction_align * weights['interaction'] +
        change_align * weights['change'] +
        intensity_align * weights['intensity']
    )
    
    # Consistency bonus: stable lifestyles get a small boost
    # This reflects the philosophy: "consistency is a form of effort"
    consistency_multiplier = 0.95 + (person.consistency_score * 0.05)
    final_score = base_score * consistency_multiplier
    
    # Clamp to [0, 1]
    final_score = max(0.0, min(1.0, final_score))
    
    # Generate human-readable explanation
    explanation = _generate_explanation(
        person, work,
        energy_align, flexibility_align, interaction_align,
        change_align, intensity_align
    )
    
    # Generate recommendation
    recommendation = _generate_recommendation(final_score)
    
    return {
        'score': final_score,
        'breakdown': {
            'energy': energy_align,
            'flexibility': flexibility_align,
            'interaction': interaction_align,
            'change': change_align,
            'intensity': intensity_align
        },
        'explanation': explanation,
        'recommendation': recommendation
    }


def _generate_explanation(
    person: LifestyleVector,
    work: LifestyleVector,
    energy_align: float,
    flexibility_align: float,
    interaction_align: float,
    change_align: float,
    intensity_align: float
) -> List[str]:
    """Generate human-readable explanations for alignment."""
    
    explanations = []
    
    # Energy rhythm
    if energy_align > 0.8:
        explanations.append(
            f"✓ Energy rhythms align well ({person.energy_rhythm} ≈ {work.energy_rhythm})"
        )
    elif energy_align < 0.5:
        explanations.append(
            f"✗ Energy rhythm mismatch ({person.energy_rhythm} vs {work.energy_rhythm})"
        )
    
    # Interaction density
    if interaction_align > 0.8:
        explanations.append("✓ Communication preferences match")
    elif interaction_align < 0.5:
        if person.interaction_density < work.interaction_density:
            explanations.append("✗ This role requires more collaboration than you prefer")
        else:
            explanations.append("✗ This role offers less interaction than you prefer")
    
    # Intensity
    if intensity_align > 0.8:
        explanations.append("✓ Work intensity matches your preference")
    elif intensity_align < 0.5:
        if person.intensity_preference < work.intensity_preference:
            explanations.append("✗ This role is more intense than you typically prefer")
        else:
            explanations.append("✗ This role may feel too slow-paced for you")
    
    # Change tolerance
    if change_align > 0.8:
        explanations.append("✓ Similar comfort with change and variability")
    elif change_align < 0.5:
        if person.change_tolerance < work.change_tolerance:
            explanations.append("✗ This environment changes more rapidly than you prefer")
        else:
            explanations.append("✗ This environment may feel too rigid for you")
    
    # Flexibility
    if flexibility_align > 0.8:
        explanations.append("✓ Schedule flexibility aligns well")
    
    # Consistency bonus
    if person.consistency_score > 0.7:
        explanations.append("✓ Your lifestyle consistency suggests good long-term potential")
    
    return explanations


def _generate_recommendation(score: float) -> str:
    """Generate action recommendation based on alignment score."""
    
    if score >= 0.80:
        return "🟢 Strong alignment — worth serious exploration"
    elif score >= 0.65:
        return "🟡 Moderate alignment — consider a trial period"
    elif score >= 0.50:
        return "🟠 Weak alignment — proceed with caution"
    else:
        return "🔴 Poor alignment — probably not a good fit right now"


# ============================================================================
# BATCH MATCHING
# ============================================================================

def find_best_matches(
    person: LifestyleVector,
    work_options: List[LifestyleVector],
    top_n: int = 5
) -> List[Tuple[LifestyleVector, Dict]]:
    """
    Find the best matching work opportunities for a person.
    
    Important: This returns a ranked list, but the ranking is contextual
    (best for THIS person) not absolute (best jobs). The same work
    opportunity could rank differently for different people.
    
    Args:
        person: The person's lifestyle vector
        work_options: List of work opportunities to consider
        top_n: Number of top matches to return
        
    Returns:
        List of (work, result) tuples, sorted by alignment score (descending)
        
    Examples:
        >>> person = LifestyleVector(...)
        >>> works = [work1, work2, work3, ...]
        >>> matches = find_best_matches(person, works, top_n=3)
        >>> for work, result in matches:
        ...     print(f"{work.label}: {result['score']:.2f}")
    """
    
    results = []
    for work in work_options:
        result = calculate_alignment(person, work)
        results.append((work, result))
    
    # Sort by score (descending)
    results.sort(key=lambda x: x[1]['score'], reverse=True)
    
    return results[:top_n]


# ============================================================================
# CONVENIENCE FUNCTIONS
# ============================================================================

def print_alignment_report(person: LifestyleVector, work: LifestyleVector):
    """
    Print a formatted alignment report.
    
    Args:
        person: Person's lifestyle vector
        work: Work opportunity's lifestyle vector
    """
    
    result = calculate_alignment(person, work)
    
    print("=" * 70)
    print("ALIGNMENT REPORT")
    print("=" * 70)
    print()
    print(f"Person: {person.label or 'Unknown'}")
    print(f"Work:   {work.label or 'Unknown'}")
    print()
    print(f"Overall Score: {result['score']:.3f}")
    print(f"Assessment:    {result['recommendation']}")
    print()
    print("Breakdown:")
    for dimension, score in result['breakdown'].items():
        print(f"  {dimension:12s}: {score:.3f}")
    print()
    print("Reasons:")
    for reason in result['explanation']:
        print(f"  {reason}")
    print()
    print("=" * 70)


# ============================================================================
# DEMO
# ============================================================================

def demo():
    """Run a demonstration of the alignment system."""
    
    print("\n" + "=" * 70)
    print("CONTINUUM PROTOCOL - ALIGNMENT ENGINE DEMO")
    print("=" * 70)
    print()
    print("⚠️  This is a conceptual prototype, not production code.")
    print()
    print("Concept: Match people and work by lifestyle rhythm, not resumes.")
    print()
    
    # Example 1: Good match
    print("SCENARIO 1: Night owl seeking async remote work")
    print("-" * 70)
    
    person1 = LifestyleVector(
        energy_rhythm="evening",
        time_flexibility=0.9,
        interaction_density=0.2,
        change_tolerance=0.4,
        intensity_preference=0.6,
        consistency_score=0.8,
        label="Night Owl Developer"
    )
    
    work1 = LifestyleVector(
        energy_rhythm="distributed",
        time_flexibility=0.9,
        interaction_density=0.3,
        change_tolerance=0.3,
        intensity_preference=0.5,
        consistency_score=0.7,
        label="Async Remote Team",
        profile_type="work"
    )
    
    print_alignment_report(person1, work1)
    
    # Example 2: Poor match
    print("\nSCENARIO 2: Morning person applying to late-night startup")
    print("-" * 70)
    
    person2 = LifestyleVector(
        energy_rhythm="morning",
        time_flexibility=0.3,
        interaction_density=0.7,
        change_tolerance=0.2,
        intensity_preference=0.4,
        consistency_score=0.9,
        label="Early Bird Manager"
    )
    
    work2 = LifestyleVector(
        energy_rhythm="evening",
        time_flexibility=0.8,
        interaction_density=0.9,
        change_tolerance=0.8,
        intensity_preference=0.9,
        consistency_score=0.4,
        label="Fast-Paced Startup",
        profile_type="work"
    )
    
    print_alignment_report(person2, work2)
    
    print("\n" + "=" * 70)
    print("KEY INSIGHT:")
    print("  Neither person nor work is 'better' than the other.")
    print("  We only measure alignment at this moment in time.")
    print("=" * 70)
    print()


if __name__ == "__main__":
    demo()
