"""
File name: environment.py
Author(s): Liam Lawless
Date created: November 13, 2023
Last modified: November 25, 2023

Description:
    The environment.py file defines the Environment class, which manages the simulation space, orchestrates agent interactions, and maintains the overall state of the natural selection simulation.

Dependencies:

"""

class Environment:
    def __init__(self, population, adversaries, food, bounds):
        self.population = population
        self.adversaries = adversaries
        self.food = food
        self.bounds = bounds
        self.next_gen_population = []   # stores all of the agents that have been born in a generation

    def update_environment(self):
        # Update agents
        for agent in self.population:
            if agent.energy > 0:
                agent.perform_action(self)

        # Update adversaries
        for adversary in self.adversaries:
            adversary.update()  # Decrease cooldown and recover energy if resting
            if adversary.energy > 0 and adversary.cooldown == 0:
                adversary.seek_agents(self.population)

        self.check_for_predation()

    def remove_food(self, food_item):
        self.food.remove(food_item)

    def remove_agent(self, agent):
        # Remove the agent from the population
        self.population.remove(agent)

    def check_for_predation(self):
        for adversary in self.adversaries:
            for agent in self.population[:]:  # Copy to avoid modification during iteration
                if adversary.position.distance_to(agent.position) <= adversary.ENTITY_RADIUS + agent.ENTITY_RADIUS and not agent.is_safe():

                    # check if the agent can defend the attack from the adversary
                    if agent.strength < adversary.attack_power:
                        # Handle the agent being eaten by the adversary
                        self.remove_agent(agent)
                        adversary.consume()
                        adversary.cooldown = adversary.COOLDOWN_AFTER_EATING
                    else:
                        adversary.defended_agents.append(agent)