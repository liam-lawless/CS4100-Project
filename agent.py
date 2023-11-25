"""
File name: agent.py
Author(s): Liam Lawless
Date created: November 10, 2023
Last modified: November 25, 2023

Description:
    The Agent class encapsulates the attributes and behaviors of prey in a natural selection simulation. It handles their movement, interaction with food, energy levels, and reproduction, simulating evolutionary processes.

Dependencies:
    - random
    - math
    - entity
"""

from entity import Entity
import math
import random

class Agent(Entity):
    DEFAULT_ENERGY = 12500  # Overriding the default energy level for agents
    MUTATION_PROBABILITY = 0.1  # Probability a trait will mutate on reproduction
    MUTATION_AMOUNT = 1     # Amount a trait will mutate +/-

    def __init__(self, position, size, speed, vision, strength, bounds):
        super().__init__(position, size, speed, vision, bounds)
        self.energy = Agent.DEFAULT_ENERGY
        self.strength = strength
        #self.food_consumed = 0

    def calculate_energy_cost(self):
        # Agents might have a different energy cost calculation
        return (self.speed ** 2) * (self.size ** 2) + self.vision + self.strength
    
    def perform_action(self, environment):
        # Check if the agent has enough energy to act
        if self.energy <= 0:
            return  # Could also handle death or inactive state here

        # Sense the environment and make decisions based on it
        self.sense_environment(environment)

        # Additional actions can be implemented here
    
    def sense_environment(self, environment):
        # Calculate the sensing radius based on the vision trait
        vision_radius = self.vision * Agent.VISION_RANGE_MULTIPLIER

        # Detect all food within the sensing radius
        food_in_sight = []
        for food in environment.food:
            if self.position.distance_to(food.position) <= vision_radius:
                food_in_sight.append(food)

        # Detect all adversaries within the sensing radius
        adversary_in_sight = []
        for adversary in environment.adversaries:
            if self is not adversary and self.position.distance_to(adversary.position) <= vision_radius:
                adversary_in_sight.append(adversary)

        # Optionally, detect other agents within the sensing radius
        # agents_in_sight = []
        # for other_agent in environment.population:
        #     if self is not other_agent and self.position.distance_to(other_agent.position) <= vision_radius:
        #         agents_in_sight.append(other_agent)

        # Perform actions based on the sensed environment
        # For example, move towards the closest food item
        if adversary_in_sight:
            closest_adversary = min(adversary_in_sight, key=lambda f: self.position.distance_to(f.position))
            self.flee(closest_adversary.position)
        elif food_in_sight:
            closest_food = min(food_in_sight, key=lambda f: self.position.distance_to(f.position))
            self.move_towards(closest_food.position)

        # If no food is in sight, continue wandering
        else:
            self.wander()

    def flee(self, target_position):
        # Calculate the direction towards the target
        direction_to_target = math.atan2(target_position.y - self.position.y, target_position.x - self.position.x)
        
        # Set the heading directly opposite the target
        self.heading = (direction_to_target + math.pi) % (2 * math.pi)
        self.move(math.cos(self.heading), math.sin(self.heading))

    def reproduce(self):
        size = self.mutate_trait(self.size)
        speed = self.mutate_trait(self.speed)
        vision = self.mutate_trait(self.vision)
        strength = self.mutate_trait(self.strength)
        return Agent(self.position, size, speed, vision, strength, self.bounds)
    
    def mutate_trait(self, trait_value):
        if random.random() < Agent.MUTATION_PROBABILITY:
            #mutation = random.choice([i for i in range(-Agent.MUTATION_AMOUNT, Agent.MUTATION_AMOUNT + 1) if i != 0])
            mutation = random.uniform(-Agent.MUTATION_AMOUNT, Agent.MUTATION_AMOUNT)
            result = round(trait_value + mutation, 1) # Avoid float inaccuracies 
            return max(result, 1.0)  # Ensure we don't get negative or 0 value traits
        return trait_value

    def print_stats(self):
        print(self)     # Helps identify  agents when testing with small amounts
        print("Size: ", self.size)
        print("Speed: ", self.speed)
        print("Vision: ", self.vision)
        print("Strength: ", self.strength)
        print("Energy: ", self.energy)
        print(f'Food Eaten: {self.consumed}')
