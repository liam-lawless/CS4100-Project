"""
File name: agent.py
Author(s): Liam Lawless
Date created: November 10, 2023
Last modified: November 24, 2023

Description:
    The Agent class encapsulates the attributes and behaviors of agents in a natural selection simulation. It handles their movement, interaction with food, energy levels, and reproduction, simulating evolutionary processes.

Dependencies:
    - random
    - numpy
    - math
    - pos
"""

import random
import numpy as np
import math
from pos import Pos

class Agent:
    DEFAULT_ENERGY = 10000
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

        # Calculate the initial facing direction towards the center of the canvas
        center = Pos(bounds[0] / 2, bounds[1] / 2)
        self.heading = math.atan2(center.y - position.y, center.x - position.x)

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
        self.wander()

    def move(self, delta_x=None, delta_y=None):
        if self.energy > 0:
            # If specific movements are not specified, use random movement
            if delta_x is None:
                delta_x = random.randint(-self.speed, self.speed)
            if delta_y is None:
                delta_y = random.randint(-self.speed, self.speed)
            
            # Update position with boundary checks
            new_x = max(0, min(self.position.x + delta_x, self.bounds[0]))
            new_y = max(0, min(self.position.y + delta_y, self.bounds[1]))

            # Apply the movement
            self.position.x = new_x
            self.position.y = new_y

            # Deduct energy for the movement
            self.energy -= 1

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

    def wander(self):
        if self.energy <= 0:
            return

        # The maximum change in angle per move
        max_angle_change = math.radians(15)  # 10 degrees for example

        # Randomly change the heading by a small amount
        self.heading += random.uniform(-max_angle_change, max_angle_change)

        # Calculate the new position based on the heading
        delta_x = math.cos(self.heading)
        delta_y = math.sin(self.heading)

        # Boundary check and update position
        new_x = max(0, min(self.position.x + delta_x, self.bounds[0]))
        new_y = max(0, min(self.position.y + delta_y, self.bounds[1]))

        # If the agent would hit a boundary, reflect the heading off the boundary
        if new_x == 0 or new_x == self.bounds[0]:
            self.heading = math.pi - self.heading
        if new_y == 0 or new_y == self.bounds[1]:
            self.heading = -self.heading

        # Normalize the heading to keep it between 0 and 2*pi
        self.heading %= 2 * math.pi

        # Move the agent
        self.move(delta_x, delta_y)
