"""
File name: entity.py
Author(s): Liam Lawless
Date created: November 25, 2023
Last modified: November 25, 2023

Description:
    The Entity class encapsulates the abstract attributes and behaviors of both agents and adversaries in the selection simulation. It handles their movement, interaction with food, and energy levels.

Dependencies:
    - random
    - math
    - pos
"""

import random
import math
from pos import Pos

class Entity:
    ENTITY_RADIUS = 5
    VISION_RANGE_MULTIPLIER = 5
    MAX_ANGLE_CHANGE = math.radians(15)  # 15 degrees
    DEFAULT_ENERGY = 500  # Set a default value to be overridden by subclasses

    def __init__(self, position, size, speed, vision, bounds):
        self.position = position
        self.size = size
        self.speed = speed
        self.vision = vision
        self.bounds = bounds
        self.energy = Entity.DEFAULT_ENERGY
        self.heading = self.calculate_initial_heading()
        self.consumed = 0

    def calculate_initial_heading(self):
        # Calculate the initial facing direction towards the center of the canvas
        center = Pos(self.bounds[0] / 2, self.bounds[1] / 2)
        return math.atan2(center.y - self.position.y, center.x - self.position.x)

    def move(self, delta_x, delta_y):
        if self.energy <= 0:
            return
        
        # Normalize and scale the direction vector
        magnitude = math.sqrt(delta_x ** 2 + delta_y ** 2)
        if magnitude != 0:
            delta_x = (delta_x / magnitude) * self.speed
            delta_y = (delta_y / magnitude) * self.speed

        # Update position with boundary checks
        self.position.x = max(0, min(self.position.x + delta_x, self.bounds[0]))
        self.position.y = max(0, min(self.position.y + delta_y, self.bounds[1]))

        # Deduct energy based on movement
        self.energy -= self.calculate_energy_cost()

    def calculate_energy_cost(self):
        # Define the cost of moving; this can be overridden by subclasses
        return (self.speed ** 2) * (self.size ** 2)

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

    def move_towards(self, target_position):
        # Calculate the direction towards the target
        direction_to_target = math.atan2(target_position.y - self.position.y, target_position.x - self.position.x)

        # Set the heading towards the target
        self.heading = direction_to_target

        # Move one step in the direction of the target
        delta_x = math.cos(direction_to_target)
        delta_y = math.sin(direction_to_target)

        self.move(delta_x, delta_y)

    # Consume either a food item or an agent
    def consume(self):
        self.consumed += 1

    def reset_energy(self):
        # This might set the inherited energies too low
        self.energy = Entity.DEFAULT_ENERGY 