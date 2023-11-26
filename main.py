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
NUM_AGENTS = 4
NUM_ADVERSARIES = 1
FOOD_AMOUNT = 10
START_SIZE = 10
VARIABILITY = 2
MAX_TICKS = 1000
TICK_RATE = 10  # Milliseconds between ticks
NUM_GENERATIONS = 5  # The total number of generations to simulate
DELAY_BETWEEN_GENERATIONS = 2500  # Delay in milliseconds between generations

# Function Definitions
def generate_edge_position(bounds):
    return random.choice([
        Pos(random.choice([0, bounds[0]]), random.randint(0, bounds[1])),
        Pos(random.randint(0, bounds[0]), random.choice([0, bounds[1]]))
    ])

def generate_center_position(bounds):
    return Pos(
            random.randint((bounds[0]/2)-10, (bounds[0]/2)+10),
            random.randint((bounds[1]/2)-10, (bounds[1]/2)+10),
        )

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

def end_generation():
    # Clear the canvas for the next generation
    view.clear_canvas()
    
    # Assess agents and adversaries for survival and reproduction
    next_generation_agents = [agent for agent in agents if agent.consumed >= 1]
    next_generation_adversaries = [adversary for adversary in adversaries if adversary.consumed >= 1]

    # Reproduce agents
    for agent in agents:
        if agent.consumed >= 2 and agent.is_safe():
            offspring = agent.reproduce()
            next_generation_agents.append(offspring)

    # Reset positions and food for the next generation
    agents[:] = next_generation_agents
    adversaries[:] = next_generation_adversaries
    food[:] = []
    generate_food_position(BOUNDS, food, FOOD_AMOUNT)
    for agent in agents:
        agent.reset_for_new_generation()
        agent.position = generate_edge_position(BOUNDS)
    for adversary in adversaries:
        adversary.reset_for_new_generation()
        adversary.position = generate_center_position(BOUNDS)  

    # Check if we have more generations to simulate
    if current_generation < NUM_GENERATIONS:
        root.after(DELAY_BETWEEN_GENERATIONS, start_generation)
    else:
        print(f"Simulation finished after {NUM_GENERATIONS} generations")

def start_generation():
    global gameTick, current_generation
    gameTick = 0
    current_generation += 1
    print(f"Starting generation {current_generation}")
    root.after(TICK_RATE, game_tick)

def game_tick():
    global gameTick
    gameTick += 1

    sim.update_environment()
    view.update_view()

    if all(agent.is_safe() or agent.energy <= 0 for agent in agents):
        print(f"All agents are done for generation {current_generation}. Ending generation.")

        root.after(DELAY_BETWEEN_GENERATIONS, end_generation)
        return
    
    # Check if max ticks reached
    if gameTick >= MAX_TICKS:
        print(f"Reached max ticks for generation {current_generation}. Ending generation.")
        end_generation()
        return

    root.after(TICK_RATE, game_tick)

# Main Execution
if __name__ == "__main__":
    # Initialize game variables
    gameTick = 0
    current_generation = 0
    agents = []
    food = []
    adversaries = []

    # Generate agents, adversaries, and food
    for _ in range(NUM_AGENTS):
        rand_pos = generate_edge_position(BOUNDS)
        new_agent = Agent(
            rand_pos,
            round(random.uniform(1.8, 2.2), 1),   # size
            round(random.uniform(1.8, 2.2), 1),   # speed
            round(random.uniform(7.0, 8.0), 1),   # vision
            round(random.uniform(1.0, 3.0), 1),   # strength
            BOUNDS
        )
        agents.append(new_agent)

    for _ in range(NUM_ADVERSARIES):
        # Generate a random pos near the middle of the canvas
        rand_pos = generate_center_position(BOUNDS)
        #  (position, size, speed, vision, strength, bounds)
        new_adversary = Adversary(rand_pos, 5, 2.0, 20, 2.0, BOUNDS)
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
    start_generation()

    # Start the Tkinter event loop
    root.mainloop()


