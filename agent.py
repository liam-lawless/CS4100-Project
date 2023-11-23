import random
from utils import random_name
from pos import pos

class Agent:
    def __init__(self, position, size, speed, vision, strength):
        # (X, Y) position represented by pos class
        self.position = position

        # traits
        self.size = size
        self.speed = speed
        self.vision = vision
        self.strength = strength # enough strength strength to survive n amount of attacks, might have to be cut based on how much time we have

        self.energy = 50    # default 50 (for now)
        self.mutation_probability = 0.1
        self.mutation_amount = 1


    def mutate_trait(self, trait_value):
        if random.random() < self.mutation_probability:
            mutation = 0
            # ensures that a mutation amount of 0 can not be selected
            # prevents genes from not mutating even if they were selected to mutate
            while mutation == 0:
                mutation = random.randint(-self.mutation_amount, self.mutation_amount)
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

    def move(self):
        # Implement logic to move 1 tile around
        pass

    def explore(self):
        # Implement explore logic
        pass

    def go_to_food(self):
        # Implement go_to_food logic
        pass

    def eat(self):
        # Implement eat logic
        pass
    
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
    
    def reset_energy(self, default=50):
        self.energy = default

# Examples & other stuff
# c1 = pos(0,0)
# animal1 = Agent(position = c1, size=10, speed=0, vision=8, strength=7)
# animal2 = Agent(position = c1, size=12, speed=10, vision=7, strength=6)

# # Mutation example
# mutated_size = animal1.mutate_trait(animal1.size)

# # Inheritence example (offspring of animal1)
# animal3 = animal1.reproduce()
# animal3.print_stats()

# # Checking how often a child has a trait value greater or less than that of their parent
# if animal3.size != 10:
#     print("SIZE OUTLIER")

# if animal3.speed != 5:
#     print("SPEED OUTLIER")

# if animal3.vision != 8:
#     print("VISION OUTLIER")

# if animal3.strength != 7:
#     print("STRENGTH OUTLIER")
