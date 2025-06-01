"""Person agent for modelling virus spread.

"""

from mesa.experimental.continuous_space import ContinuousSpaceAgent
from sneeze import VirusCloud

class Person(ContinuousSpaceAgent):
    """A Person agent.

    The agent has three possible states:
        - Susceptible: can be infected by others
        - Infected: can infect others
        - Recovered: can't be infected again

    The agent moves randomly within the space
    """

    def __init__(
        self,
        model,
        space,
        position,
        state,
        infection_timer=0,
        infection_duration=30,
        speed=1.0,
        direction=(1, 1),
        sneeze_probability=0.5,
    ):
        """Create a new Person agent.

        Args:
            model: Model instance the agent belongs to
            space: ContinuousSpace instance the agent belongs to
            position: Initial position of the agent in the space
            state: Current state of the agent, one of 'susceptible', 'infected', or 'recovered'
        """
        super().__init__(space, model)
        self.position = position
        self.state = state  # 'susceptible', 'infected', or 'recovered'
        self.infection_timer = infection_timer
        self.infection_duration = infection_duration
        self.speed = speed
        self.direction = direction
        self.sneeze_probability = sneeze_probability


    def step(self):
        # Move in the set direction with constant speed
        self.position += self.direction * self.speed

        if self.state == "Infected":
            self.infection_timer += 1
            if self.infection_timer >= self.infection_duration:
                self.state = "Recovered"
            
            if self.model.random.random() < self.sneeze_probability:
                cloud = VirusCloud(
                    model=self.model,
                    space=self.space,
                    position=self.position.copy(),
                    radius=self.model.sneeze_radius,
                    intensity=self.model.sneeze_init_intensity,
                    decay_rate=self.model.sneeze_decay_rate,
                )
                self.model.agents.add(cloud)
        
        elif self.state == "Susceptible":
            # Cek tetangga
            neighbors, _ = self.get_neighbors_in_radius(radius=self.model.infection_radius)
            for neighbor in neighbors:
                # SOLUSI: Cek dulu apakah tetangga adalah Person!
                if isinstance(neighbor, Person) and neighbor.state == "Infected":
                    if self.model.random.random() < self.model.infection_probability:
                        self.state = "Infected"
                        # Keluar dari loop jika sudah terinfeksi agar efisien
                        break
