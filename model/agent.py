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

from model.q_learning_model import build_q_network, ReplayBuffer
from model.entity import Entity
from model.pos import Pos
import numpy as np
import math
import random

class Agent(Entity):
    DEFAULT_ENERGY = 15000  # Overriding the default energy level for agents
    MUTATION_PROBABILITY = 0.4  # Probability a trait will mutate on reproduction
    MUTATION_AMOUNT = 0.2     # Amount a trait will mutate +/-
    MAX_AGE = 5
    ACTION_SIZE = 4
    STATE_SIZE = 4
    REPLAY_BUFFER_CAPACITY = 50000

    # Epsilon Decay Parameters
    EPSILON_INITIAL = 1.0
    EPSILON_MIN = 0.01
    EPSILON_DECAY = 1     # Use decay value of 1 if no longer training
    #EPSILON_DECAY = 0.9995

    def __init__(self, position, size, speed, vision, strength, bounds):
        super().__init__(position, size, speed, vision, bounds)
        self.energy = Agent.DEFAULT_ENERGY
        self.strength = strength
        self.satisfied = False
        self.at_edge = False
        self.age = 0

        # Q learning properties
        self.q_network = build_q_network(Agent.STATE_SIZE, Agent.ACTION_SIZE)
        self.epsilon = Agent.EPSILON_INITIAL
        self.replay_buffer = ReplayBuffer(self.REPLAY_BUFFER_CAPACITY)  # Initialize replay buffer with a certain capacity
        self.just_consumed_food = False
        self.successfully_evaded = False
        self.successfully_reproduced = False

    def calculate_energy_cost(self):
        # Agents might have a different energy cost calculation
        return (self.speed ** 2) * (self.size ** 2) * self.strength + self.vision

    def perform_action(self, environment):

        # Check if the agent is safe; if so, do nothing
        if self.is_safe():
            if not self.successfully_reproduced:
                self.reproduce_if_possible(environment)

            return

        # Current state
        current_state = self.get_current_state(environment)

        # Reshape the current state to match the input shape expected by the model
        current_state = np.array(current_state).reshape(1, -1)

        if np.random.rand() <= self.epsilon:
            action = np.random.randint(0, Agent.ACTION_SIZE)
        else:
            action_values = self.q_network.predict(current_state)
            action = np.argmax(action_values[0])

        # Execute the action and observe new state and reward
        reward, done = self.execute_action(action, environment)
        new_state = self.get_current_state(environment)

        # Store experience in replay buffer
        self.replay_buffer.add(current_state, action, reward, new_state, done)

        # Update epsilon with decay only if it's above the minimum threshold
        if self.epsilon > Agent.EPSILON_MIN:
            self.epsilon *= Agent.EPSILON_DECAY
    
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

    # Appends the newly born agent to the next_gen_population list in the environment
    def reproduce(self, environment):
        size = self.mutate_trait(self.size)
        speed = self.mutate_trait(self.speed)
        vision = self.mutate_trait(self.vision)
        strength = self.mutate_trait(self.strength)
        environment.next_gen_population.append(Agent(self.position, size, speed, vision, strength, self.bounds))
    
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

    def get_current_state(self, environment):
        # Implement logic to construct the current state vector
        # Calculate the sensing radius based on the vision trait
        vision_radius = self.vision * Agent.VISION_RANGE_MULTIPLIER

        # Prepare the state vector values
        energy = round(self.energy / Agent.DEFAULT_ENERGY, 2)
        presence_of_food = 0
        presence_of_adversaries = 0
        presence_of_agents = 0

        # Detect all food within the sensing radius
        for food in environment.food:
            if self.position.distance_to(food.position) <= vision_radius:
                #observation['food'].append(food)
                presence_of_food = 1

        # Detect all adversaries within the sensing radius
        for adversary in environment.adversaries:
            if self.position.distance_to(adversary.position) <= vision_radius:
                #observation['adversaries'].append(adversary)
                presence_of_adversaries = 1

        # Detect other agents within the sensing radius
        for other_agent in environment.population:
            if self is not other_agent and self.position.distance_to(other_agent.position) <= vision_radius:
                #observation['agents'].append(other_agent)
                presence_of_agents = 1

        # Return the observation vector
        vector = [energy, presence_of_food, presence_of_adversaries, presence_of_agents]

        return vector

    def execute_action(self, action, environment):
        if action < 0 or action >= Agent.ACTION_SIZE:
            print(f"Invalid action: {action}")
            action = 0  # Default action or handle error as needed
        reward = 0
        done = False

        if action == 0:  # Wander
            self.wander()
        elif action == 1:  # Flee
            self.flee_from_closest_adversary(environment)
            # Update reward and done based on fleeing outcome
            reward, done = self.calculate_reward(environment, action), False
        elif action == 2:  # Reproduce
            self.reproduce_if_possible(environment)
            # Update reward and done based on reproduction outcome
            reward, done = self.calculate_reward(environment, action), False
        elif action == 3:  # Consume
            self.consume_closest_food(environment)
            # Update reward and done based on consumption outcome
            reward, done = self.calculate_reward(environment, action), False

        # Reset flags
        self.just_consumed_food = False
        self.successfully_evaded = False
        self.successfully_reproduced = False

        return reward, done

    def flee_from_closest_adversary(self, environment):
        # Define the observable space of the agent
        vision_radius = self.vision * Agent.VISION_RANGE_MULTIPLIER

        # Find the closest adversary and flee
        adversary_in_sight = []
        for adversary in environment.adversaries:
            if self is not adversary and self.position.distance_to(adversary.position) <= vision_radius:
                adversary_in_sight.append(adversary)

        if adversary_in_sight:
            closest_adversary = min(adversary_in_sight, key=lambda f: self.position.distance_to(f.position))
            self.flee(closest_adversary.position)
            self.successfully_evaded = True


    def reproduce_if_possible(self, environment):
        # If the agent is satisfied and at the edge, do nothing
        if self.is_safe():
            self.reproduce(environment)
            self.successfully_reproduced = True

    # Consume either the closest food item or the closest small adversary
    def consume_closest_food(self, environment):
        # Define the observable space of the agent
        vision_radius = self.vision * Agent.VISION_RANGE_MULTIPLIER

        # Factor in agent size
        agent_size = self.ENTITY_RADIUS + self.size 

        # Detect all food within the sensing radius
        food_in_sight = []
        for food in environment.food:
            if self.position.distance_to(food.position) <= vision_radius:
                food_in_sight.append(food)

        small_agents_in_sight = []
        for other_agent in environment.population:
            # Check if the other agent is different and within the vision radius
            if self is not other_agent and self.position.distance_to(other_agent.position) <= vision_radius:
                # Check if the other agent is sufficiently smaller
                if self.size - other_agent.size >= 0.75:
                    small_agents_in_sight.append(other_agent)

        # if there is a small agent and food item, go to the closest one
        if small_agents_in_sight and food_in_sight:
            closest_agent = min(small_agents_in_sight, key=lambda f: self.position.distance_to(f.position))
            closest_food = min(food_in_sight, key=lambda f: self.position.distance_to(f.position))

            if self.position.distance_to(closest_agent.position) < self.position.distance_to(closest_food.position):
                self.move_towards(closest_agent.position)
                
                # Check if the predator is close enough to cannibalize the prey
                if self.position.distance_to(closest_agent.position) <= self.ENTITY_RADIUS + closest_agent.ENTITY_RADIUS:
                    # Cannibalize the agent
                    self.consume()
                    environment.remove_agent(closest_agent)
                    self.just_consumed_food = True
            else:
                self.move_towards(closest_food.position)

                if self.position.distance_to(closest_food.position) <= agent_size + closest_food.ENTITY_RADIUS:
                    # Eat the food
                    self.consume()
                    environment.remove_food(closest_food)
                    self.just_consumed_food = True

        elif small_agents_in_sight:
            closest_agent = min(small_agents_in_sight, key=lambda f: self.position.distance_to(f.position))
            self.move_towards(closest_agent.position)
            
            # Check if the predator is close enough to cannibalize the prey
            if self.position.distance_to(closest_agent.position) <= self.ENTITY_RADIUS + closest_agent.ENTITY_RADIUS:
                # Cannibalize the prey
                self.consume()
                environment.remove_agent(closest_agent)
                self.just_consumed_food = True

        elif food_in_sight:
            closest_food = min(food_in_sight, key=lambda f: self.position.distance_to(f.position))
            self.move_towards(closest_food.position)

            if self.position.distance_to(closest_food.position) <= agent_size + closest_food.ENTITY_RADIUS:
                self.consume()
                environment.remove_food(closest_food)
                self.just_consumed_food = True

        # tell the agent to return home if it has eaten 2 food
        if self.consumed >= 2:
            self.satisfied = True
            self.return_home()

    def calculate_reward(self, environment, action):
        # Initialize reward
        reward = 0

        # Define reward values
        REWARD_FOOD_CONSUMED = 15
        REWARD_SURVIVED_ADVERSARY = 5
        REWARD_REPRODUCED = 10
        PENALTY_LOST_ENERGY = -1
        PENALTY_CAUGHT_BY_ADVERSARY = -20
        PENALTY_FAILED_REPRODUCTION = -5

        # Check conditions and assign rewards/penalties
        if action == 3:  # Consume action
            if self.just_consumed_food:
                reward += REWARD_FOOD_CONSUMED
            else:
                reward += PENALTY_LOST_ENERGY

        if action == 1:  # Flee action
            if self.successfully_evaded:
                reward += REWARD_SURVIVED_ADVERSARY
            else:
                reward += PENALTY_CAUGHT_BY_ADVERSARY

        if action == 2:  # Reproduce action
            if self.successfully_reproduced:
                reward += REWARD_REPRODUCED
            else:
                reward += PENALTY_FAILED_REPRODUCTION

        # Deduct energy cost for all actions
        reward += PENALTY_LOST_ENERGY * self.calculate_energy_cost()

        return reward