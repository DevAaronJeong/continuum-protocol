import numpy as np
from dataclasses import dataclass

@dataclass
class RhythmVector:
    """
    Life-Work Rhythm Vector Model
    All values are normalized between 0.0 and 1.0
    """
    peak_energy_time: float      # 0.0 (Midnight) -> 1.0 (Next Midnight)
    focus_span: float            # 0.0 (Fragmented) -> 1.0 (Deep Work)
    social_density: float        # 0.0 (Solitary) -> 1.0 (Constant Collaboration)
    variance_tolerance: float    # 0.0 (Routine) -> 1.0 (Chaos/Dynamic)

    def to_array(self):
        return np.array([
            self.peak_energy_time, 
            self.focus_span, 
            self.social_density, 
            self.variance_tolerance
        ])

class AlignmentEngine:
    def calculate_compatibility(self, person: RhythmVector, role: RhythmVector) -> float:
        """
        Calculates cosine similarity between a person and a role.
        This is not a 'score' of quality, but a measure of 'angle'.
        """
        v_p = person.to_array()
        v_r = role.to_array()
        
        # Cosine Similarity Logic
        dot_product = np.dot(v_p, v_r)
        norm_p = np.linalg.norm(v_p)
        norm_r = np.linalg.norm(v_r)
        
        if norm_p == 0 or norm_r == 0:
            return 0.0
            
        return dot_product / (norm_p * norm_r)

# --- Demo Scenario ---
if __name__ == "__main__":
    # Case: A developer who loves deep work at night
    alice = RhythmVector(
        peak_energy_time=0.9,  # Night Owl
        focus_span=0.9,        # Deep Focus
        social_density=0.2,    # Low Interaction
        variance_tolerance=0.4 # Prefer Stability
    )
    
    # Job A: Early stage startup (Chaos, Meetings, Morning standups)
    startup_role = RhythmVector(
        peak_energy_time=0.3,  # Morning
        focus_span=0.3,        # Frequent Switching
        social_density=0.9,    # High Interaction
        variance_tolerance=0.9 # High Variance
    )
    
    # Job B: Async Remote Protocol Engineer
    async_role = RhythmVector(
        peak_energy_time=0.8,  # Flexible/Late
        focus_span=0.9,        # Long Focus Blocks
        social_density=0.1,    # Async/Text mostly
        variance_tolerance=0.3 # Defined Spec
    )

    engine = AlignmentEngine()
    
    print(f"Alignment with Startup: {engine.calculate_compatibility(alice, startup_role):.4f}")
    print(f"Alignment with Async Role: {engine.calculate_compatibility(alice, async_role):.4f}")
    
    # This proves: It's not about skill, it's about the shape of work.
