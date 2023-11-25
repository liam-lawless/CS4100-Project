"""
File name: main.py
Author(s): Liam Lawless
Date created: November 22, 2023
Last modified: November 25, 2023

Description:
    This script serves as the entry point for the natural selection simulation. It sets up the environment, initializes the simulation agents and food sources, and starts the main application loop.

Dependencies:
    - agent.py: Defines the Agent class with its properties and behaviors.
    - environment.py: Manages the simulation environment and its state.
    - pos.py: Provides a class for X, Y coordinate representation.
    - food.py: Defines the Food class used in the simulation.
    - simulation_view.py: Handles the visual representation of the simulation.
    - tkinter: Provides GUI components for the simulation.
    - random: Provides random assignment of traits, and object starting positions
"""

import tkinter as tk
import random
from agent import Agent
from pos import Pos
from food import Food
from simulation_view import SimulationView
from environment import Environment
from adversary import Adversary

# Configuration Constants
BOUNDS = (500, 500)
NUM_AGENTS = 10
NUM_ADVERSARIES = 1
FOOD_AMOUNT = 20
START_SIZE = 10
VARIABILITY = 2
MAX_TICKS = 15000
TICK_RATE = 10  # Milliseconds between ticks

# Function Definitions
def generate_edge_position(bounds):
    return random.choice([
        Pos(random.choice([0, bounds[0]]), random.randint(0, bounds[1])),
        Pos(random.randint(0, bounds[0]), random.choice([0, bounds[1]]))
    ])

def generate_food_position(bounds, food, food_amount):
    # Keeps food from spawning too close to the edge
    x_min_bound = int(bounds[0] * 0.1)
    y_min_bound = int(bounds[1] * 0.1)

    while len(food) < food_amount:
        new_position = Pos(
            random.randint(x_min_bound, bounds[0]-x_min_bound),
            random.randint(y_min_bound, bounds[1]-y_min_bound)
        )
        if all(new_position != f.position for f in food):
            food.append(Food(new_position))

def game_tick():
    global gameTick
    gameTick += 1

    sim.update_environment()
    view.update_view()

    if gameTick < MAX_TICKS:
        root.after(TICK_RATE, game_tick)
    else:
        print("Simulation ended after reaching the maximum number of ticks")

# Main Execution
if __name__ == "__main__":
    # Initialize game variables
    gameTick = 0
    agents = []
    food = []
    adversaries = []

    # Generate agents, adversaries, and food
    for _ in range(NUM_AGENTS):
        rand_pos = generate_edge_position(BOUNDS)
        new_agent = Agent(
            rand_pos,
            round(random.uniform(1.0, 4.0), 1),   # size
            round(random.uniform(1.0, 4.0), 1),   # speed
            round(random.uniform(5.0, 10.0), 1),   # vision
            round(random.uniform(1.0, 4.0), 1),   # strength
            BOUNDS
        )
        agents.append(new_agent)

    for _ in range(NUM_ADVERSARIES):
        # Generate a random pos near the middle of the canvas
        rand_pos = Pos(
            random.randint((BOUNDS[0]/2)-10, (BOUNDS[0]/2)+10),
            random.randint((BOUNDS[1]/2)-10, (BOUNDS[1]/2)+10),
        )
        new_adversary = Adversary(rand_pos, 2.0, BOUNDS)
        adversaries.append(new_adversary)

    generate_food_position(BOUNDS, food, FOOD_AMOUNT)

    # Set up the GUI
    root = tk.Tk()
    root.title("Natural Selection Simulation")
    canvas = tk.Canvas(root, width=BOUNDS[0], height=BOUNDS[1], bg='white')
    canvas.pack()

    # Initialize the Model (Environment) and the View (SimulationView)
    sim = Environment(agents, adversaries,food, BOUNDS)
    view = SimulationView(canvas, sim)

    # Start the simulation loop
    root.after(TICK_RATE, game_tick)

    # Start the Tkinter event loop
    root.mainloop()