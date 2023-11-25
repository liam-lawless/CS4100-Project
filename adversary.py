
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

class Adversary:
    ENTITY_RADIUS = 5
    COLOR = 'red'

    def __init__(self, position, speed, bounds):
        self.position = position
        self.speed = speed
        self.bounds = bounds

    def seek_agents(self, agents):
        # Find the closest agent
        closest_agent = min(agents, key=lambda a: self.position.distance_to(a.position))
        self.move_towards(closest_agent.position)

    def move_towards(self, target_position):
        # Calculate the direction towards the target
        direction_to_target = math.atan2(target_position.y - self.position.y, target_position.x - self.position.x)

        # Move one step in the direction of the target
        delta_x = math.cos(direction_to_target)
        delta_y = math.sin(direction_to_target)
        self.position.x += delta_x * self.speed
        self.position.y += delta_y * self.speed
        # Here you should add boundary checks and other considerations as needed

    # ... Additional methods for drawing, updating state, etc. ...
