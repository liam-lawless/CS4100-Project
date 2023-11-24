import random
from utils import random_name
from pos import Pos

class Agent:
    DEFAULT_ENERGY = 100
    MUTATION_PROBABILITY = 0.1
    MUTATION_AMOUNT = 1

    def __init__(self, position, size, speed, vision, strength, bounds):
        # (X, Y) position represented by pos class
        self.position = position

        # traits
        self.size = size
        self.speed = speed
        self.vision = vision
        self.strength = strength # enough strength strength to survive n amount of attacks, might have to be cut based on how much time we have

        self.energy = Agent.DEFAULT_ENERGY

        # bounds of the environment represented as a tuple (max_X, max_Y)
        # we can always assume that the min canvas bounds are (0, 0)
        self.bounds = bounds

        self.food_consumed = 0

    def mutate_trait(self, trait_value):
        if random.random() < Agent.MUTATION_PROBABILITY:
            mutation = 0
            # ensures that a mutation amount of 0 can not be selected
            # prevents genes from not mutating even if they were selected to mutate
            while mutation == 0:
                mutation = random.randint(-Agent.MUTATION_AMOUNT, Agent.MUTATION_AMOUNT)
                result = trait_value + mutation
                # prevents returning negative value traits (always mutates up if at 0)
                if result < 0:
                    mutation = 0
        
            return trait_value + mutation
    
    def print_stats(self):
        print("Size: ", self.size)
        print("Speed: ", self.speed)
        print("Vision: ", self.vision)
        print("Strength: ", self.strength)
        print("Energy: ", self.energy)

    def perform_action(self):
        # just have agents move at the moment (randomly)
        self.move()

    # move agent to the specified x, y position
    def move(self):
        if self.energy > 0:
            self.energy -= 1  # Deduct energy for movement
            self.position.x = random.randint(0, self.bounds[0])
            self.position.y = random.randint(0, self.bounds[1])

    def explore(self):
        # Implement explore logic
        pass

    def go_to_food(self):
        # Implement go_to_food logic
        pass

    def consume_food(self):
        self.food_consumed += 1
    
    def rest(self):
        # Implement rest logic
        pass

    def none(self):
        # Implement default action logic
        pass

    # This might have to go in environment class
    def death(self):
        # Implement death logic, e.g., based on energy depletion, environmental factors, etc.
        pass

    def reproduce(self):
        # Implement logic for reproducing given each animal is asexual in nature
        size = self.mutate_trait(self.size)
        speed = self.mutate_trait(self.speed)
        vision = self.mutate_trait(self.vision)
        strength = self.mutate_trait(self.strength)

        return Agent(position= self.position, size=size, speed=speed, vision=vision, strength=strength)
    
    def reset_energy(self):
        self.energy = Agent.DEFAULT_ENERGY
