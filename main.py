# instantiate board
# gameTick = 0
#
from agent import Agent
from environment import Environment
from pos import pos
import tkinter as tk
import random
from food import Food


generations =  10
gamtick = 0

num_agents = 10     # How many agents to start the game with 
agents = []
s = 10              # starting value for each trait
v = 2               # introduce slight variability in each trait

# generate food
food = []
food_amount = 5
for i in range(food_amount):
    item = Food(pos(random.randint(100,400), random.randint(100,400)), 50)
    food.append(item)

# instantiate agents
for i in range(num_agents):
    # starts every agent on the edge of the board
    starting_positions = [pos(random.choice([0,400]), random.randint(0,400)), pos(random.randint(0,400), random.choice([0,400]))]
    rand_pos = random.choice(starting_positions)

    # creates a new agent
    new_agent = Agent(rand_pos, random.randint(s-v, s+v), random.randint(s-v, s+v), random.randint(s-v, s+v), random.randint(s-v, s+v))

    # append the new agent to our list of agents
    agents.append(new_agent)

for i in range(generations):
    pass

# Example usage:
# Assuming you have a list called 'population' containing VirtualAnimal objects
# and each VirtualAnimal object has a 'position' attribute of type tuple (x, y)
root = tk.Tk()
sim = Environment(root, agents, food)
root.mainloop()
