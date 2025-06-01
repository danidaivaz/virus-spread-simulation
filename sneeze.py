import numpy as np
from mesa.experimental.continuous_space import ContinuousSpaceAgent

class VirusCloud(ContinuousSpaceAgent):
    """
    Jejak virus yang tertinggal setelah agen Infected bersin.
    VirusCloud akan menghilang secara bertahap berdasarkan decay rate.
    """

    def __init__(
        self,
        model,
        space,
        position,
        radius=2.0,
        intensity=1.0,
        decay_rate=0.01
    ):
        super().__init__(space, model)
        self.position = position
        self.radius = radius
        self.intensity = intensity
        self.decay_rate = decay_rate

    def step(self):
        """Kurangi intensitas dan hapus cloud jika sudah terlalu lemah."""
        self.intensity -= self.decay_rate
        if self.intensity <= 0:
            self.model.agents.remove(self)
