"""
File name: food.py
Author(s): Liam Lawless
Date created: November 14, 2023
Last modified: November 24, 2023

Description:
    This file defines the Food class, representing consumable items in the simulation that agents can eat.

Dependencies:

"""

class Food:
    ENTITY_RADIUS = 5  # Size of the food for collision detection

    def __init__(self, position):
        self.position = position

    def __repr__(self):
        return f"Food(Position: ({self.position.x}, {self.position.y}), Energy: {self.energy})"
