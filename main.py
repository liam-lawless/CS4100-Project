import tkinter as tk
import random
from agent import Agent
from environment import Environment
from pos import Pos
from food import Food

def generate_edge_position(bounds):
    return Pos(
        random.choice([0, bounds[0]]),
        random.randint(0, bounds[1])
    )

def generate_food_position(bounds, food):
    while len(food) < food_amount:
        new_position = Pos(
            random.randint(50, bounds[0]-50),
            random.randint(50, bounds[1]-50)
        )
        if all(new_position != f.position for f in food):
            food.append(Food(new_position, 50))

def game_tick():
    global gameTick
    gameTick += 1

    # Update the environment, which will update the positions of agents
    sim.update_environment()

    # Perform actions for each agent with energy
    for agent in agents:
        if agent.energy > 0:
            agent.perform_action()
        else:
            # Handle the agent with no energy (e.g., remove from board, mark as dead)
            pass

    # Check for game end condition
    if gameTick < MAX_TICKS:
        # Schedule the next tick
        root.after(TICK_RATE, game_tick)
    else:
        print("Simulation ended after reaching the maximum number of ticks")

# Environment Variables
bounds = (400, 400)

# Agent variables
num_agents = 5  # How many agents to start the game with
agents = []
# temporary, need to figure out what the base stat value will be
start_size = 10  # starting value for each trait
variability = 2  # introduce slight variability in each trait

# Food variables
food = []
food_amount = 15

# Initialize gameTick before the game_tick function
gameTick = 0

# Instantiate agents
for _ in range(num_agents):
    rand_pos = generate_edge_position(bounds)
    new_agent = Agent(
        rand_pos,
        random.randint(start_size-variability, start_size+variability),
        random.randint(start_size-variability, start_size+variability),
        random.randint(start_size-variability, start_size+variability),
        random.randint(start_size-variability, start_size+variability),
        bounds
    )
    agents.append(new_agent)

generate_food_position(bounds, food)

# Create the main Tkinter window
root = tk.Tk()

# Create the simulation environment
sim = Environment(root, agents, food, bounds)

# Define the total number of ticks for the simulation
MAX_TICKS = 1000

# Milliseconds between ticks
TICK_RATE = 100  # Example: 1000 ms = 1 second

# Initialize the simulation
sim.run()

# Start the game tick process
root.after(TICK_RATE, game_tick)

# Start the Tkinter event loop
root.mainloop()