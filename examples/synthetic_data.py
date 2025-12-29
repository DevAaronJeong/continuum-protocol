"""
Synthetic Lifestyle Data Generator

Generates realistic fake profiles for testing matching algorithms
without needing real user data.

This helps us experiment with different matching strategies while
respecting privacy.
"""

import random
from dataclasses import dataclass, asdict
from typing import List, Literal
import json


@dataclass
class LifestyleVector:
    """Represents a person or organization's lifestyle configuration."""
    
    energy_rhythm: Literal["morning", "afternoon", "evening", "distributed"]
    time_flexibility: float  # 0.0 to 1.0
    interaction_density: float  # 0.0 to 1.0
    change_tolerance: float  # 0.0 to 1.0
    intensity_preference: float  # 0.0 to 1.0
    consistency_score: float  # 0.0 to 1.0
    
    # Optional metadata for interpretation
    profile_type: str = "person"  # or "work"
    label: str = ""  # human-readable description


class SyntheticDataGenerator:
    """Generate realistic synthetic lifestyle profiles."""
    
    ENERGY_RHYTHMS = ["morning", "afternoon", "evening", "distributed"]
    
    # Archetypal person profiles
    PERSON_ARCHETYPES = {
        "early_bird_stable": {
            "energy_rhythm": "morning",
            "time_flexibility": (0.2, 0.4),
            "interaction_density": (0.3, 0.6),
            "change_tolerance": (0.1, 0.3),
            "intensity_preference": (0.4, 0.6),
            "consistency_score": (0.7, 0.9)
        },
        "night_owl_creative": {
            "energy_rhythm": "evening",
            "time_flexibility": (0.6, 0.9),
            "interaction_density": (0.1, 0.4),
            "change_tolerance": (0.5, 0.8),
            "intensity_preference": (0.5, 0.8),
            "consistency_score": (0.4, 0.7)
        },
        "distributed_collaborator": {
            "energy_rhythm": "distributed",
            "time_flexibility": (0.7, 1.0),
            "interaction_density": (0.6, 0.9),
            "change_tolerance": (0.6, 0.9),
            "intensity_preference": (0.6, 0.9),
            "consistency_score": (0.5, 0.8)
        },
        "routine_specialist": {
            "energy_rhythm": random.choice(["morning", "afternoon"]),
            "time_flexibility": (0.1, 0.3),
            "interaction_density": (0.2, 0.5),
            "change_tolerance": (0.1, 0.2),
            "intensity_preference": (0.3, 0.6),
            "consistency_score": (0.8, 1.0)
        },
        "burnout_recovering": {
            "energy_rhythm": "distributed",
            "time_flexibility": (0.8, 1.0),
            "interaction_density": (0.1, 0.3),
            "change_tolerance": (0.1, 0.3),
            "intensity_preference": (0.1, 0.3),
            "consistency_score": (0.3, 0.6)
        }
    }
    
    # Archetypal work profiles
    WORK_ARCHETYPES = {
        "startup_sprint": {
            "energy_rhythm": "distributed",
            "time_flexibility": (0.6, 0.8),
            "interaction_density": (0.7, 0.9),
            "change_tolerance": (0.8, 1.0),
            "intensity_preference": (0.8, 1.0),
            "consistency_score": (0.2, 0.5)
        },
        "enterprise_stable": {
            "energy_rhythm": "morning",
            "time_flexibility": (0.2, 0.4),
            "interaction_density": (0.5, 0.7),
            "change_tolerance": (0.1, 0.3),
            "intensity_preference": (0.4, 0.6),
            "consistency_score": (0.7, 0.9)
        },
        "async_remote": {
            "energy_rhythm": "distributed",
            "time_flexibility": (0.8, 1.0),
            "interaction_density": (0.2, 0.4),
            "change_tolerance": (0.3, 0.6),
            "intensity_preference": (0.4, 0.7),
            "consistency_score": (0.6, 0.8)
        },
        "creative_agency": {
            "energy_rhythm": "afternoon",
            "time_flexibility": (0.5, 0.7),
            "interaction_density": (0.6, 0.8),
            "change_tolerance": (0.6, 0.9),
            "intensity_preference": (0.6, 0.9),
            "consistency_score": (0.4, 0.7)
        },
        "nonprofit_mission": {
            "energy_rhythm": "morning",
            "time_flexibility": (0.3, 0.5),
            "interaction_density": (0.5, 0.7),
            "change_tolerance": (0.2, 0.5),
            "intensity_preference": (0.5, 0.7),
            "consistency_score": (0.6, 0.8)
        }
    }
    
    @staticmethod
    def _sample_from_range(value_range):
        """Sample a random float from a range tuple."""
        if isinstance(value_range, tuple):
            return random.uniform(value_range[0], value_range[1])
        return value_range
    
    @classmethod
    def generate_person(cls, archetype: str = None) -> LifestyleVector:
        """
        Generate a synthetic person profile.
        
        Args:
            archetype: One of the PERSON_ARCHETYPES keys, or None for random
        """
        if archetype is None:
            archetype = random.choice(list(cls.PERSON_ARCHETYPES.keys()))
        
        template = cls.PERSON_ARCHETYPES[archetype]
        
        return LifestyleVector(
            energy_rhythm=template["energy_rhythm"] if isinstance(template["energy_rhythm"], str) 
                         else random.choice(cls.ENERGY_RHYTHMS),
            time_flexibility=cls._sample_from_range(template["time_flexibility"]),
            interaction_density=cls._sample_from_range(template["interaction_density"]),
            change_tolerance=cls._sample_from_range(template["change_tolerance"]),
            intensity_preference=cls._sample_from_range(template["intensity_preference"]),
            consistency_score=cls._sample_from_range(template["consistency_score"]),
            profile_type="person",
            label=archetype
        )
    
    @classmethod
    def generate_work(cls, archetype: str = None) -> LifestyleVector:
        """
        Generate a synthetic work profile.
        
        Args:
            archetype: One of the WORK_ARCHETYPES keys, or None for random
        """
        if archetype is None:
            archetype = random.choice(list(cls.WORK_ARCHETYPES.keys()))
        
        template = cls.WORK_ARCHETYPES[archetype]
        
        return LifestyleVector(
            energy_rhythm=template["energy_rhythm"] if isinstance(template["energy_rhythm"], str) 
                         else random.choice(cls.ENERGY_RHYTHMS),
            time_flexibility=cls._sample_from_range(template["time_flexibility"]),
            interaction_density=cls._sample_from_range(template["interaction_density"]),
            change_tolerance=cls._sample_from_range(template["change_tolerance"]),
            intensity_preference=cls._sample_from_range(template["intensity_preference"]),
            consistency_score=cls._sample_from_range(template["consistency_score"]),
            profile_type="work",
            label=archetype
        )
    
    @classmethod
    def generate_dataset(cls, n_people: int = 100, n_work: int = 50) -> dict:
        """
        Generate a full synthetic dataset for testing.
        
        Returns a dict with 'people' and 'work' lists.
        """
        people = [cls.generate_person() for _ in range(n_people)]
        work = [cls.generate_work() for _ in range(n_work)]
        
        return {
            "people": [asdict(p) for p in people],
            "work": [asdict(w) for w in work],
            "metadata": {
                "n_people": n_people,
                "n_work": n_work,
                "archetypes_used": {
                    "people": list(cls.PERSON_ARCHETYPES.keys()),
                    "work": list(cls.WORK_ARCHETYPES.keys())
                }
            }
        }


def main():
    """Generate and display sample synthetic data."""
    
    print("=" * 60)
    print("Synthetic Lifestyle Data Generator")
    print("=" * 60)
    print()
    
    # Generate examples of each archetype
    print("PERSON ARCHETYPES:")
    print("-" * 60)
    for archetype_name in SyntheticDataGenerator.PERSON_ARCHETYPES.keys():
        person = SyntheticDataGenerator.generate_person(archetype_name)
        print(f"\n{archetype_name}:")
        print(f"  Energy: {person.energy_rhythm}")
        print(f"  Flexibility: {person.time_flexibility:.2f}")
        print(f"  Interaction: {person.interaction_density:.2f}")
        print(f"  Change tolerance: {person.change_tolerance:.2f}")
        print(f"  Intensity: {person.intensity_preference:.2f}")
        print(f"  Consistency: {person.consistency_score:.2f}")
    
    print("\n")
    print("WORK ARCHETYPES:")
    print("-" * 60)
    for archetype_name in SyntheticDataGenerator.WORK_ARCHETYPES.keys():
        work = SyntheticDataGenerator.generate_work(archetype_name)
        print(f"\n{archetype_name}:")
        print(f"  Energy: {work.energy_rhythm}")
        print(f"  Flexibility: {work.time_flexibility:.2f}")
        print(f"  Interaction: {work.interaction_density:.2f}")
        print(f"  Change tolerance: {work.change_tolerance:.2f}")
        print(f"  Intensity: {work.intensity_preference:.2f}")
        print(f"  Consistency: {work.consistency_score:.2f}")
    
    # Generate a small dataset
    print("\n")
    print("=" * 60)
    print("Generating synthetic dataset (10 people, 5 work profiles)...")
    dataset = SyntheticDataGenerator.generate_dataset(n_people=10, n_work=5)
    
    # Save to file
    with open('synthetic_dataset.json', 'w') as f:
        json.dump(dataset, f, indent=2)
    
    print("✓ Dataset saved to synthetic_dataset.json")
    print(f"  - {len(dataset['people'])} person profiles")
    print(f"  - {len(dataset['work'])} work profiles")
    print()
    print("You can now use this data to test matching algorithms!")


if __name__ == "__main__":
    main()
