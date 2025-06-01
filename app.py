import os
import sys

from matplotlib.markers import MarkerStyle

sys.path.insert(0, os.path.abspath("../../../.."))

from model import VirusSpread
from mesa.visualization import Slider, SolaraViz, make_space_component


def draw_person(agent):
    if agent.state == "Susceptible":
        return {"color": "blue", "size": 20}
    elif agent.state == "Infected":
        return {"color": "red", "size": 20}
    elif agent.state == "Recovered":
        return {"color": "green", "size": 20}


model_params = {
    "seed": {
        "type": "InputText",
        "value": 42,
        "label": "Random Seed",
    },
    "population_size": Slider(
        label="Population Size",
        value=100,
        min=10,
        max=300,
        step=10,
    ),
    "width": 100,
    "height": 100,
    "initial_infected": Slider(
        label="Initially Infected",
        value=5,
        min=0,
        max=100,
        step=1,
    ),
    "infection_radius": Slider(
        label="Infection Radius",
        value=2,
        min=0.5,
        max=10,
        step=0.1,
    ),
    "infection_probability": Slider(
        label="Infection Probability",
        value=0.2,
        min=0.0,
        max=1.0,
        step=0.01,
    ),
    "infection_duration": Slider(
        label="Infection Duration (steps)",
        value=50,
        min=1,
        max=200,
        step=1,
    ),
}

model = VirusSpread()

page = SolaraViz(
    model,
    components=[make_space_component(agent_portrayal=draw_person, backend="matplotlib")],
    model_params=model_params,
    name="Virus Spread Simulation",
)

page  # Shows the interactive UI

