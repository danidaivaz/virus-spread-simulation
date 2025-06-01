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
        is_masked=False,
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
        self.is_masked = is_masked 


    def step(self):
        # Move in the set direction with constant speed
        self.position += self.direction * self.speed

        if self.state == "Infected":
            self.infection_timer += 1
            if self.infection_timer >= self.infection_duration:
                self.state = "Recovered"
            
            if self.model.random.random() < self.sneeze_probability:
                intensity = self.model.cloud_init_intensity
                radius = self.model.cloud_radius
                if self.is_masked:
                    intensity *= (1 - self.model.mask_effectiveness)
                    radius *= (1 - self.model.mask_effectiveness)

                cloud = VirusCloud(
                    model=self.model,
                    space=self.space,
                    position=self.position.copy(),
                    cloud_radius=radius,
                    cloud_intensity=intensity,
                    decay_rate=self.model.cloud_decay_rate,
                )
                self.model.agents.add(cloud)
        
        elif self.state == "Susceptible":
            # Cek tetangga
            neighbors, _ = self.get_neighbors_in_radius(radius=self.model.infection_radius)
            for neighbor in neighbors:
                # SOLUSI: Cek dulu apakah tetangga adalah Person!
                if isinstance(neighbor, Person) and neighbor.state == "Infected":
                    infection_probability = self.model.infection_probability
                    
                    # Jika yang terinfeksi (neighbor) pakai masker, probabilitas turun
                    if neighbor.is_masked:
                        infection_probability *= (1 - self.model.mask_effectiveness)
                    
                    # Jika yang rentan (self) pakai masker, probabilitas turun lagi
                    if self.is_masked:
                        infection_probability *= (1 - self.model.mask_effectiveness)
                        
                    if self.model.random.random() < infection_probability:
                        self.state = "Infected"
                        break
            
            if self.state == "Susceptible":
                # Dapatkan semua agen dalam radius deteksi awan
                all_neighbors_in_cloud_range, _ = self.get_neighbors_in_radius(radius=self.model.cloud_radius)
                # Filter hanya untuk VirusCloud
                clouds_nearby = [agent for agent in all_neighbors_in_cloud_range if isinstance(agent, VirusCloud)]

                for cloud in clouds_nearby:
                    # Kalkulasi probabilitas infeksi dari awan
                    cloud_infection_prob = cloud.intensity * self.model.infection_probability
                    # Jika yang rentan pakai masker, probabilitas turun
                    if self.is_masked:
                        cloud_infection_prob *= (1 - self.model.mask_effectiveness)
                    
                    if self.model.random.random() < cloud_infection_prob:
                        self.state = "Infected"
                        break # Hentikan pengecekan jika sudah terinfeksi
