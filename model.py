"""
Virus Spread Model
===================
A Mesa implementation of Virus Spread model.
"""

import os
import sys

sys.path.insert(0, os.path.abspath("../../../.."))

from mesa.datacollection import DataCollector
import numpy as np
import random
from mesa import Model
from agent import Person
from mesa.experimental.continuous_space import ContinuousSpace

def count_susceptible(model):
    # Hanya hitung agen jika itu adalah instance dari Person DAN statusnya cocok
    return len([a for a in model.agents if isinstance(a, Person) and a.state == "Susceptible"])

def count_infected(model):
    # Hanya hitung agen jika itu adalah instance dari Person DAN statusnya cocok
    return len([a for a in model.agents if isinstance(a, Person) and a.state == "Infected"])

def count_recovered(model):
    # Hanya hitung agen jika itu adalah instance dari Person DAN statusnya cocok
    return len([a for a in model.agents if isinstance(a, Person) and a.state == "Recovered"])

class VirusSpread(Model):
    """Virus model class. Handles agent creation, placement and scheduling."""

    def __init__(
        self,
        population_size=100,
        width=50,
        height=50,
        infection_radius=2,
        infection_probability=0.3,
        infection_duration=30,
        initial_infected=1,
        speed=1.0,
        cloud_decay_rate=0.553,
        sneeze_probability=0.07,
        cloud_radius=1.5,
        cloud_init_intensity=1.0,
        mask_usage_percentage=0.0,
        mask_effectiveness=0.7,
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
            speed: Speed of movement for each agent (default: 1.0)
            cloud_decay_rate: Rate at which the sneeze cloud dissipates (default: 0.02)
            sneeze_probability: Probability of an infected person sneezing (default: 0.05)
            cloud_radius: Radius of the sneeze cloud (default: 2.0)
            cloud_init_intensity: Initial intensity of the sneeze cloud (default: 1.0)
        """
        super().__init__(seed=seed)
        self.width = width
        self.height = height
        self.population_size = population_size
        self.infection_radius = infection_radius
        self.infection_probability = infection_probability
        self.infection_duration = infection_duration
        self.cloud_decay_rate = cloud_decay_rate
        self.sneeze_probability = sneeze_probability
        self.cloud_radius = cloud_radius
        self.cloud_init_intensity = cloud_init_intensity
        self.mask_usage_percentage = mask_usage_percentage
        self.mask_effectiveness = mask_effectiveness

                # --- INISIALISASI DATACOLLECTOR DI SINI ---
        self.datacollector = DataCollector(
            model_reporters={
                "Susceptible": count_susceptible,
                "Infected": count_infected,
                "Recovered": count_recovered,
            },
            agent_reporters={ # Mengumpulkan data per agen (jika diperlukan)
                "State": "state",
                "IsMasked": "is_masked" 
            }
        )


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

        num_masked = int(self.mask_usage_percentage * population_size)
        is_masked_list = [True] * num_masked + [False] * (population_size - num_masked)
        self.random.shuffle(is_masked_list)

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
            is_masked=is_masked_list
            )


    def step(self):
        """Run one step of the model.

        All agents are activated in random order using the AgentSet shuffle_do method.
        """
        self.agents.shuffle_do("step")
        self.datacollector.collect(self)
