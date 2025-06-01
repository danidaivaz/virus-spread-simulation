"""
Virus Spread Model
===================
A Mesa implementation of Virus Spread model.
"""

import os
import sys

sys.path.insert(0, os.path.abspath("../../../.."))


import numpy as np
import random
from mesa import Model
from agent import Person
from mesa.experimental.continuous_space import ContinuousSpace


class VirusSpread(Model):
    """Virus model class. Handles agent creation, placement and scheduling."""

    def __init__(
        self,
        population_size=100,
        width=100,
        height=100,
        infection_radius=2,
        infection_probability=0.3,
        infection_duration=30,
        initial_infected=1,
        speed=1.0,
        sneeze_decay_rate=0.02,  # <--- Tambahan
        sneeze_probability=0.05,  # <--- Tambahan juga, untuk diteruskan ke agent
        sneeze_radius=2.0,  # <--- Tambahan untuk radius bersin
        sneeze_init_intensity=1.0,  # <--- Tambahan untuk intensitas bersin
        seed=None
    ):
        """Create a new Virus Spread model.

        Args:
            population_size: Number of Person in the simulation (default: 100)
            width: Width of the space (default: 100)
            height: Height of the space (default: 100)
            infection_radius: Radius within which an infected person can infect others (default: 2)
            infection_probability: Probability of infection when in range (default: 0.2)
            infection_duration: Duration of infection in steps (default: 30)
            initial_infected: Number of initially infected persons (default: 1)
            seed: Random seed for reproducibility (default: None)
        """
        super().__init__(seed=seed)
        self.population_size = population_size
        self.infection_radius = infection_radius
        self.infection_probability = infection_probability
        self.infection_duration = infection_duration
        self.sneeze_decay_rate = sneeze_decay_rate
        self.sneeze_probability = sneeze_probability
        self.sneeze_radius = sneeze_radius
        self.sneeze_init_intensity = sneeze_init_intensity

        # Set up the space
        self.space = ContinuousSpace(
            [[0, width], [0, height]],
            torus=True,
            random=self.random,
        )

        # Create and place the Person agents
        positions = self.rng.random(size=(population_size, 2)) * self.space.size
        directions = self.rng.uniform(-1, 1, size=(population_size, 2))
        directions /= np.linalg.norm(directions, axis=1, keepdims=True)
        
        # Generate states
        states = ["Infected"] * initial_infected + ["Susceptible"] * (population_size - initial_infected)
        random.shuffle(states)

        Person.create_agents(
            self,
            population_size,
            self.space,
            position=positions,
            state=states,
            infection_duration=infection_duration,
            speed=speed,
            direction=directions,
            sneeze_probability=sneeze_probability,
            )


    def step(self):
        """Run one step of the model.

        All agents are activated in random order using the AgentSet shuffle_do method.
        """
        self.agents.shuffle_do("step")
