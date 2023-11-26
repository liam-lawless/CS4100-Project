"""
File name: simulation.py
Author(s): Liam Lawless
Date created: November 26, 2023
Last modified: November 26, 2023

Description:

Dependencies:

"""

import random
from tkinter import Tk, Canvas
from agent import Agent
from adversary import Adversary
from environment import Environment
from food import Food
from pos import Pos
from simulation_view import SimulationView

class SimulationRunner:
    def __init__(self, root, canvas, bounds, num_agents, num_adversaries, food_amount, max_ticks, tick_rate, num_generations, delay_between_generations):
        self.root = root
        self.canvas = canvas
        self.bounds = bounds
        self.num_agents = num_agents
        self.num_adversaries = num_adversaries
        self.food_amount = food_amount
        self.max_ticks = max_ticks
        self.tick_rate = tick_rate
        self.num_generations = num_generations
        self.delay_between_generations = delay_between_generations

        self.game_tick = 0
        self.current_generation = 0
        self.agents = []
        self.food = []
        self.adversaries = []

        self.sim = None
        self.view = None

        self.setup_simulation()  # Set self.sim to a new Environment instance

    def setup_simulation(self):
        self.sim = Environment(self.agents, self.adversaries, self.food, self.bounds)
        self.view = SimulationView(self.canvas, self.sim)
        self.populate_simulation()

    def populate_simulation(self):
        for _ in range(self.num_agents):
            rand_pos = self.generate_edge_position()
            new_agent = Agent(
                rand_pos,
                round(random.uniform(1.8, 2.2), 1),   # size
                round(random.uniform(1.8, 2.2), 1),   # speed
                round(random.uniform(7.0, 8.0), 1),   # vision
                round(random.uniform(1.0, 3.0), 1),   # strength
                self.bounds
            )
            self.agents.append(new_agent)

        for _ in range(self.num_adversaries):
            rand_pos = self.generate_center_position()
            new_adversary = Adversary(rand_pos, 5, 2.0, 20, 2.0, self.bounds)
            self.adversaries.append(new_adversary)

        self.generate_food_position()

    def generate_edge_position(self):
        return random.choice([
            Pos(random.choice([0, self.bounds[0]]), random.randint(0, self.bounds[1])),
            Pos(random.randint(0, self.bounds[0]), random.choice([0, self.bounds[1]]))
        ])

    def generate_center_position(self):
        return Pos(
            random.randint((self.bounds[0]/2)-10, (self.bounds[0]/2)+10),
            random.randint((self.bounds[1]/2)-10, (self.bounds[1]/2)+10),
        )

    def generate_food_position(self):
        x_min_bound = int(self.bounds[0] * 0.1)
        y_min_bound = int(self.bounds[1] * 0.1)

        while len(self.food) < self.food_amount:
            new_position = Pos(
                random.randint(x_min_bound, self.bounds[0]-x_min_bound),
                random.randint(y_min_bound, self.bounds[1]-y_min_bound)
            )
            if all(new_position != f.position for f in self.food):
                self.food.append(Food(new_position))

    def end_generation(self):
        self.view.clear_canvas()

        next_generation_agents = [agent for agent in self.agents if agent.consumed >= 1]
        next_generation_adversaries = [adversary for adversary in self.adversaries if adversary.consumed >= 1]

        for agent in self.agents:
            if agent.consumed >= 2 and agent.is_safe():
                offspring = agent.reproduce()
                next_generation_agents.append(offspring)

        self.agents[:] = next_generation_agents
        self.adversaries[:] = next_generation_adversaries
        self.food[:] = []

        for agent in self.agents:
            agent.reset_for_new_generation()
            agent.position = self.generate_edge_position()

        for adversary in self.adversaries:
            adversary.reset_for_new_generation()
            adversary.position = self.generate_center_position()

        self.generate_food_position()

        if self.current_generation < self.num_generations:
            self.root.after(self.delay_between_generations, self.start_generation)
        else:
            print(f"Simulation finished after {self.num_generations} generations")

    def start_generation(self):
        self.game_tick = 0
        self.current_generation += 1
        print(f"Starting generation {self.current_generation}")
        self.root.after(self.tick_rate, self.run_game_tick)

    def run_game_tick(self):
        self.game_tick += 1

        self.sim.update_environment()
        self.view.update_view()

        if all(agent.is_safe() or agent.energy <= 0 for agent in self.agents):
            print(f"All agents are done for generation {self.current_generation}. Ending generation.")
            self.root.after(self.delay_between_generations, self.end_generation)
            return

        if self.game_tick >= self.max_ticks:
            print(f"Reached max ticks for generation {self.current_generation}. Ending generation.")
            self.end_generation()
            return

        self.root.after(self.tick_rate, self.run_game_tick)

    def run(self):
        self.start_generation()
