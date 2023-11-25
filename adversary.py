
"""
File name: adversary.py
Author(s): Liam Lawless
Date created: November 25, 2023
Last modified: November 25, 2023

Description:
    The Adversary class encapsulates the attributes and behaviors of predators in a natural selection simulation. It handles their movement, interaction with agents (prey), energy levels, simulating evolutionary processes.

Dependencies:
    - random
    - numpy
    - math
    - pos
"""
import random
import math
from pos import Pos

class Adversary:
    ENTITY_RADIUS = 5
    COLOR = 'red'
    SPEED = 1.5
    VISION_RANGE_MULTIPLIER = 5

    def __init__(self, position, bounds):
        self.position = position
        self.bounds = bounds
        self.energy = 500
        self.vision = 20
        self.cooldown = 0  # Cooldown timer after eating
        self.consumed = 0

        # Calculate the initial facing direction towards the center of the canvas
        center = Pos(bounds[0] / 2, bounds[1] / 2)
        self.heading = math.atan2(center.y - position.y, center.x - position.x)

    def move(self, delta_x, delta_y):
        # Predators use energy to move
        if self.energy > 0:
            # Move a distance proportional to the agent's speed
            delta_x *= Adversary.SPEED
            delta_y *= Adversary.SPEED

            # Update position
            self.position.x = max(0, min(self.position.x + delta_x, self.bounds[0]))
            self.position.y = max(0, min(self.position.y + delta_y, self.bounds[1]))

            self.energy -= 1

    def wander(self):
        if self.energy <= 0:
            return

        # The maximum change in angle per move
        max_angle_change = math.radians(15)     # 15 degrees

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

    def seek_agents(self, agents):
        # Only sense agents within the vision range
        agents_in_range = [
            agent for agent in agents
            if self.position.distance_to(agent.position) <= self.vision * Adversary.VISION_RANGE_MULTIPLIER
        ]
        # Find the closest agent
        if agents_in_range and self.cooldown == 0:
            closest_agent = min(agents_in_range, key=lambda a: self.position.distance_to(a.position))
            self.move_towards(closest_agent.position)

        else:
            self.wander()

    def move_towards(self, target_position):
        # Calculate the direction towards the target
        direction_to_target = math.atan2(target_position.y - self.position.y, target_position.x - self.position.x)

        # Move one step in the direction of the target
        delta_x = math.cos(direction_to_target)
        delta_y = math.sin(direction_to_target)

        self.move(delta_x, delta_y)

    def update(self):
        # Call this method each simulation tick
        if self.cooldown > 0:
            self.cooldown -= 1  # Decrease cooldown over time

    def eat(self):
        # Call this method when the predator eats an agent
        self.cooldown = 150  # Set the cooldown
        self.consumed += 1

