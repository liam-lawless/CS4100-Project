"""
File name: environment.py
Author(s): Liam Lawless
Date created: November 13, 2023
Last modified: November 24, 2023

Description:
    The environment.py file defines the Environment class, which manages the simulation space, orchestrates agent interactions, and maintains the overall state of the natural selection simulation.

Dependencies:

"""

class Environment:
    def __init__(self, population, food, bounds):
        self.population = population
        self.food = food
        self.bounds = bounds

    def update_environment(self):
        for agent in self.population:
            if agent.energy > 0:
                agent.perform_action(self)
        self.check_for_collisions()

    def check_for_collisions(self):
        for agent in self.population:
            for food_item in self.food[:]:  # Copy the list to avoid modification during iteration
                if agent.position.distance_to(food_item.position) <= agent.ENTITY_RADIUS + food_item.ENTITY_RADIUS:
                    agent.consume_food()
                    self.remove_food(food_item)

    def remove_food(self, food_item):
        self.food.remove(food_item)
