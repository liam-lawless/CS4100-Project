"""
File name: simulation.py
Author(s): Liam Lawless
Date created: November 26, 2023
Last modified: November 26, 2023

Description:

Dependencies:

"""

import random
import os
from model.agent import Agent
from model.adversary import Adversary
from model.environment import Environment
from model.food import Food
from model.pos import Pos
from model.q_learning_model import train_q_network, ReplayBuffer, build_q_network
from view.simulation_view import SimulationView
from view.visualize import Visualize
from keras.models import load_model

class SimulationRunner:
    INITIAL_TRAIT_VALUE = 2.0
    TRAIT_VARIANCE = 0.3
    ADVERSARY_ATTACK = 3.0
    ADVERSARY_SPEED = 0.75
    ADVERSARY_VISION = 10

    BATCH_SIZE = 64
    DISCOUNT_FACTOR = 0.95


    def __init__(self, root, canvas, bounds, num_agents, num_adversaries, food_amount, max_ticks, tick_rate, num_generations, delay_between_generations, training_enabled):
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
        self.trait_history = {'population': [],'size': [], 'speed': [], 'vision': [], 'strength': []}
        self.trait_distribution = {'size': [], 'speed': [], 'vision': [], 'strength': []}

        self.general_model = self.load_or_create_model()
        self.training_enabled = training_enabled

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
            # position, size, speed, vision, strength, bounds
            new_agent = Agent(
                rand_pos,
                round(random.uniform(
                    SimulationRunner.INITIAL_TRAIT_VALUE-SimulationRunner.TRAIT_VARIANCE,
                    SimulationRunner.INITIAL_TRAIT_VALUE+SimulationRunner.TRAIT_VARIANCE), 1),
                round(random.uniform(
                    SimulationRunner.INITIAL_TRAIT_VALUE-SimulationRunner.TRAIT_VARIANCE,
                    SimulationRunner.INITIAL_TRAIT_VALUE+SimulationRunner.TRAIT_VARIANCE), 1),
                round(random.uniform(
                    SimulationRunner.INITIAL_TRAIT_VALUE-SimulationRunner.TRAIT_VARIANCE,
                    SimulationRunner.INITIAL_TRAIT_VALUE+SimulationRunner.TRAIT_VARIANCE), 1),
                round(random.uniform(
                    SimulationRunner.INITIAL_TRAIT_VALUE-SimulationRunner.TRAIT_VARIANCE,
                    SimulationRunner.INITIAL_TRAIT_VALUE+SimulationRunner.TRAIT_VARIANCE), 1),
                self.bounds
            )
            self.agents.append(new_agent)
            new_agent.q_network = self.general_model

        for _ in range(self.num_adversaries):
            rand_pos = self.generate_center_position()
            # position, size, speed, vision, attack_power, bounds
            new_adversary = Adversary(rand_pos, 5, SimulationRunner.ADVERSARY_SPEED, SimulationRunner.ADVERSARY_VISION, SimulationRunner.ADVERSARY_ATTACK, self.bounds)
            self.adversaries.append(new_adversary)

        self.generate_food_position()

    def generate_edge_position(self):
        return random.choice([
            Pos(random.choice([0, self.bounds[0]]), random.randint(0, self.bounds[1])),
            Pos(random.randint(0, self.bounds[0]), random.choice([0, self.bounds[1]]))
        ])

    def generate_center_position(self):
        return Pos(
            random.randint((self.bounds[0]/2)-50, (self.bounds[0]/2)+50),
            random.randint((self.bounds[1]/2)-50, (self.bounds[1]/2)+50),
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

        # Increment age and filter agents for the next generation
        for agent in self.agents:
            agent.age += 1  # Increment agent age
            if agent.consumed and agent.age < Agent.MAX_AGE:
                self.sim.next_gen_population.append(agent)
        
        next_generation_adversaries = [adversary for adversary in self.adversaries if adversary.consumed >= 1]

        self.agents[:] = self.sim.next_gen_population
        self.adversaries[:] = next_generation_adversaries
        self.food[:] = []

        # Train Q-networks of each agent
        self.train_agents()

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

            # Save the general model
            self.general_model.save('/Users/liamlawless/Desktop/2023-2024 School Year/CS4100/NSS no AI copy/agents/general_model.keras')

            # When the simulation ends, visualize the data 
            if self.current_generation == self.num_generations:
                self.collect_data()  # Call after the last generation
                visualization = Visualize(self.trait_distribution, self.trait_history)
                visualization.visualize_history(self.trait_history.keys())
        
        # clear the list for the next simulation
        self.sim.next_gen_population.clear()

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

            # Check if all agents who are safe have also successfully reproduced
            all_safe_agents_reproduced = all(agent.successfully_reproduced for agent in self.agents if agent.is_safe())

            if all_safe_agents_reproduced:
                print(f"All agents are done for generation {self.current_generation}. Ending generation.")
                self.collect_data() # collect data from each generation
                self.root.after(self.delay_between_generations, self.end_generation)
                return

        if self.game_tick >= self.max_ticks:
            print(f"Reached max ticks for generation {self.current_generation}. Ending generation.")
            self.end_generation()
            return

        self.root.after(self.tick_rate, self.run_game_tick)
        

    def run(self):
        self.start_generation()

    def collect_data(self):
        # Calculate the average traits of agents for the line chart
        if len(self.agents) > 0:
            data = {
                'population': len(self.agents),
                'size': sum(agent.size for agent in self.agents) / len(self.agents),
                'speed': sum(agent.speed for agent in self.agents) / len(self.agents),
                'vision': sum(agent.vision for agent in self.agents) / len(self.agents),
                'strength': sum(agent.strength for agent in self.agents) / len(self.agents)
            }

            # Append the average of each trait to its respective history list
            for trait, average in data.items():
                self.trait_history[trait].append(average)

            # Collect the distribution of each trait for the bar chart
            # Do this only at the end of the simulation
            if self.current_generation == self.num_generations:
                for trait in self.trait_distribution.keys():
                    self.trait_distribution[trait] = [getattr(agent, trait) for agent in self.agents]

    def train_agents(self):
        if not self.training_enabled:
            return  # Skip training if it's disabled

        for agent in self.agents:
            if len(agent.replay_buffer.buffer) >= self.BATCH_SIZE:
                train_q_network(agent.q_network, agent.replay_buffer, self.BATCH_SIZE, self.DISCOUNT_FACTOR)
    
    def load_or_create_model(self):
        if os.path.exists('/Users/liamlawless/Desktop/2023-2024 School Year/CS4100/Natural Selection Simulator/agents/general_model.keras'):
            print("Loading existing model...")
            model = load_model('/Users/liamlawless/Desktop/2023-2024 School Year/CS4100/Natural Selection Simulator/agents/general_model.keras')
            self.training_enabled = False  # Flag to disable further training
            return model
        else:
            print("Creating new model...")
            self.training_enabled = True
            state_size = 4
            action_size = 4
            return build_q_network(state_size, action_size)