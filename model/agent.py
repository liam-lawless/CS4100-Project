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

from model.entity import Entity
from model.pos import Pos
import math
import random

class Agent(Entity):
    DEFAULT_ENERGY = 15000  # Overriding the default energy level for agents
    MUTATION_PROBABILITY = 0.4  # Probability a trait will mutate on reproduction
    MUTATION_AMOUNT = 0.2     # Amount a trait will mutate +/-
    MAX_AGE = 5
    GREEDY = False  # Agents will continue to eat after 2 food, do not need to return home

    def __init__(self, position, size, speed, vision, strength, bounds):
        super().__init__(position, size, speed, vision, bounds)
        self.energy = Agent.DEFAULT_ENERGY
        self.strength = strength
        self.satisfied = False
        self.at_edge = False
        self.age = 0

    def calculate_energy_cost(self):
        # Agents might have a different energy cost calculation
        return (self.speed ** 2) * (self.size ** 2) * self.strength + self.vision
    
    def perform_action(self, environment):
        # If the agent is satisfied and at the edge, do nothing
        if self.satisfied and self.at_edge:
            return  # Agent does nothing
        
        # Check if the agent is satisfied and needs to return to the edge
        if self.consumed >= 2 and not Agent.GREEDY:
            self.satisfied = True

        if self.satisfied:
            self.return_home()
        else:
            # Check if the agent has enough energy to act
            if self.energy <= 0:
                return  # Could also handle death or inactive state here

            # Sense the environment and make decisions based on it
            self.sense_environment(environment)
    
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

        # Detect other agents within the sensing radius
        agents_in_sight = []
        for other_agent in environment.population:
            if self is not other_agent and self.position.distance_to(other_agent.position) <= vision_radius:
                agents_in_sight.append(other_agent)
        
                
        # Perform actions based on the sensed environment
        # For example, move towards the closest food item
        if adversary_in_sight:
            closest_adversary = min(adversary_in_sight, key=lambda f: self.position.distance_to(f.position))
            self.flee(closest_adversary.position)
        elif food_in_sight:
            closest_food = min(food_in_sight, key=lambda f: self.position.distance_to(f.position))
            self.move_towards(closest_food.position)
        elif agents_in_sight:
            small_agents_in_sight = []
            for agent in agents_in_sight:
                if self.size - agent.size >= 0.75:
                    small_agents_in_sight.append(agent)

            if small_agents_in_sight:
                closest_agent = min(small_agents_in_sight, key=lambda f: self.position.distance_to(f.position))

                self.move_towards(closest_agent.position)
            
            else:
                self.wander()  

        # If no food is in sight, continue wandering
        else:
            self.wander()

    def flee(self, target_position):
        # Calculate the direction towards the target
        direction_to_target = math.atan2(target_position.y - self.position.y, target_position.x - self.position.x)
        
        # Set the heading directly opposite the target
        self.heading = (direction_to_target + math.pi) % (2 * math.pi)
        self.move(math.cos(self.heading), math.sin(self.heading))

    def return_home(self):
        # Determine the closest edge of the canvas to the agent's current position
        edges = [Pos(0, self.position.y), Pos(self.bounds[0], self.position.y),
                 Pos(self.position.x, 0), Pos(self.position.x, self.bounds[1])]
        closest_edge = min(edges, key=lambda edge: self.position.distance_to(edge))
        
        # Check if the agent is already at the edge
        if self.position.distance_to(closest_edge) < self.ENTITY_RADIUS:
            self.at_edge = True
            return
        
        # Move towards the edge if not there yet
        self.move_towards(closest_edge)

    def is_safe(self):
        # Returns True if the agent is at the edge and has eaten enough food to be safe
        return self.at_edge and self.satisfied

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
    
    def reset_for_new_generation(self):
        super().reset_for_new_generation()  # Reset common entity properties
        self.energy = Agent.DEFAULT_ENERGY
        self.satisfied = False
        self.at_edge = False
        # Add any other future properties that need to be reset for a new generation

    def print_stats(self):
        print(self)     # Helps identify  agents when testing with small amounts
        print("Size: ", self.size)
        print("Speed: ", self.speed)
        print("Vision: ", self.vision)
        print("Strength: ", self.strength)
        print("Energy: ", self.energy)
        print(f'Food Eaten: {self.consumed}')