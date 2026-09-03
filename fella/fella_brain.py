from fella.core_substrate import ENNSubstrate
from fella.frontier_manifold import FrontierManifold

class FellaBrain(ENNSubstrate):
    """The master ENN engine wrapping the 4D coordinate system."""
    def __init__(self, dim: int = 128):
        super().__init__(dim=dim)
