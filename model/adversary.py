"""
File name: adversary.py
Author(s): Liam Lawless
Date created: November 25, 2023
Last modified: November 25, 2023

Description:
    The Adversary class encapsulates the attributes and behaviors of predators in a natural selection simulation. It handles their movement, interaction with agents (prey), energy levels, simulating evolutionary processes.

"""

from model.entity import Entity

class Adversary(Entity):
    DEFAULT_ENERGY = 500
    COOLDOWN_AFTER_EATING = 500  # Cooldown period after eating

    def __init__(self, position, size, speed, vision, attack_power, bounds):
        super().__init__(position, size, speed, vision, bounds)
        self.cooldown = 0
        self.attack_power = attack_power
        self.defended_agents = []

    def calculate_energy_cost(self):
        # Agents might have a different energy cost calculation
        return 0.25

    def update(self):
        # Decrease cooldown over time, recover energy if not in cooldown
        if self.cooldown > 0:
            self.cooldown -= 1  # Rate at which an adversary recovers after eating

    def seek_agents(self, agents):
        # Only sense agents within the vision range
        # Filter out agents that are satisfied and at the edge (safe agents)
        targetable_agents = [
            agent for agent in agents
            if not (agent.satisfied and agent.at_edge) and
            self.position.distance_to(agent.position) <= self.vision * Adversary.VISION_RANGE_MULTIPLIER and
            agent not in self.defended_agents
        ]
        # Find the closest agent
        if targetable_agents and self.cooldown == 0:
            closest_agent = min(targetable_agents, key=lambda a: self.position.distance_to(a.position))
            self.move_towards(closest_agent.position)
        else:
            self.wander()

    def reset_for_new_generation(self):
        super().reset_for_new_generation()  # Reset common entity properties
        self.energy = Adversary.DEFAULT_ENERGY
        self.cooldown = 0  # Reset the cooldown for the new generation
        self.defended_agents.clear()
        # Add any other future properties that need to be reset for a new generation

    def print_stats(self):
        print(f'Agents Eaten: {self.consumed}')
    