"""
File name: agent.py
Author(s): Liam Lawless
Date created: November 10, 2023
Last modified: November 23, 2023

Description:
    The Agent class encapsulates the attributes and behaviors of agents in a natural selection simulation. It handles their movement, interaction with food, energy levels, and reproduction, simulating evolutionary processes.

Dependencies:
    - random
"""

import random

class Agent:
    DEFAULT_ENERGY = 100
    MUTATION_PROBABILITY = 0.1
    MUTATION_AMOUNT = 1
    ENTITY_RADIUS = 5  # Size of the agent for collision detection

    def __init__(self, position, size, speed, vision, strength, bounds):
        self.position = position
        self.size = size
        self.speed = speed
        self.vision = vision
        self.strength = strength
        self.energy = Agent.DEFAULT_ENERGY
        self.bounds = bounds
        self.food_consumed = 0

    def mutate_trait(self, trait_value):
        if random.random() < Agent.MUTATION_PROBABILITY:
            mutation = random.choice([i for i in range(-Agent.MUTATION_AMOUNT, Agent.MUTATION_AMOUNT + 1) if i != 0])
            result = trait_value + mutation
            return max(result, 0)  # Ensure we don't get negative traits
        return trait_value

    def print_stats(self):
        print("Size: ", self.size)
        print("Speed: ", self.speed)
        print("Vision: ", self.vision)
        print("Strength: ", self.strength)
        print("Energy: ", self.energy)

    def perform_action(self):
        self.move()

    def move(self):
        if self.energy > 0:
            self.energy -= 1
            self.position.x = random.randint(0, self.bounds[0])
            self.position.y = random.randint(0, self.bounds[1])

    def consume_food(self):
        self.food_consumed += 1

    def reproduce(self):
        size = self.mutate_trait(self.size)
        speed = self.mutate_trait(self.speed)
        vision = self.mutate_trait(self.vision)
        strength = self.mutate_trait(self.strength)
        return Agent(self.position, size, speed, vision, strength, self.bounds)

    def reset_energy(self):
        self.energy = Agent.DEFAULT_ENERGY
