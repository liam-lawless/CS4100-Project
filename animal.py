import random
from utils import random_name
from pos import pos

class Animal:
    def __init__(self, name, position, size, speed, vision, strength, reproduction_rate, energy):
        self.name = name
        self.position = position
        self.size = size
        self.speed = speed
        self.vision = vision
        self.strength = strength # enough strength strength to survive n amount of attacks
        self.reproduction_rate = reproduction_rate # needs deciding
        self.energy = energy

        # Mutation parameters
        self.mutation_probability = 0.1     # the probability of a trait mutating
        self.mutation_amount = 1.0         # the amount a trait can possibly mutate +/-
        

    def mutate_trait(self, trait_value):
        if random.random() < self.mutation_probability:
            mutation = random.uniform(-self.mutation_amount, self.mutation_amount)
            return trait_value + mutation
        return trait_value

    # ensure traits are all rounded to the nearest tenth
    def inherit_traits(self, trait1, trait2, inheritance_method='random'):
        if inheritance_method == 'random':
            return random.uniform(min(trait1, trait2), max(trait1, trait2))
        elif inheritance_method == 'average':
            return ((trait1 + trait2) / 2)
        # Add more inheritance methods as needed

    def print_stats(self):
        print("Name: ", self.name)
        print("Size: ", self.size)
        print("Speed: ", self.speed)
        print("Vision: ", self.vision)
        print("Strength: ", self.strength)
        print("Reproduction rate: ", self.reproduction_rate)
        print("Energy: ", self.energy)

    def explore(self):
        # Implement explore logic
        pass

    def go_to_food(self):
        # Implement go_to_food logic
        pass

    def search_for_mate(self):
        # Implement search_for_mate logic
        pass
    
    # one thing we have to be careful about is not allowing each individual to mate, which would each spawn an offspring
    # how can we make it such that only one offspring is spawned from each mating interaction
    def mate(self, partner, inheritence_method="random"):
        size = round(self.mutate_trait(self.inherit_traits(self.size, partner.size, inheritence_method)), 1)
        speed = round(self.mutate_trait(self.inherit_traits(self.speed, partner.speed, inheritence_method)), 1)
        vision = round(self.mutate_trait(self.inherit_traits(self.vision, partner.vision, inheritence_method)), 1)
        strength = round(self.mutate_trait(self.inherit_traits(self.strength, partner.strength, inheritence_method)), 1)

        return Animal(name=random_name(), position= self.position, size=size, speed=speed, vision=vision, strength=strength,
                       reproduction_rate=0.2, energy=50)

    def eat(self):
        # Implement eat logic
        pass

    def rest(self):
        # Implement rest logic
        pass

    def none(self):
        # Implement default action logic
        pass

    def death(self):
        # Implement death logic, e.g., based on energy depletion, environmental factors, etc.
        pass

    def reproduce(self):
        # Implement logic for reproducing given each animal is asexual in nature
        pass

# Examples & other stuff
c1 = pos(0,0)
animal1 = Animal(name="Animal1", position = c1, size=10, speed=5, vision=8, strength=7, reproduction_rate=0.2, energy=50)
animal2 = Animal(name="Animal2", position = c1, size=12, speed=10, vision=7, strength=6, reproduction_rate=0.18, energy=45)

# Mutation example
mutated_size = animal1.mutate_trait(animal1.size)

# Inheritence example
animal3 = animal1.mate(animal2)
animal3.print_stats()

# Checking how often a child has a trait value greater or less than that of their parents
if animal3.size < 10 or animal3.size > 12:
    print("SIZE OUTLIER")

if animal3.speed < 5 or animal3.speed > 10:
    print("SPEED OUTLIER")

if animal3.vision < 7 or animal3.vision > 8:
    print("VISION OUTLIER")

if animal3.strength < 6 or animal3.strength > 7:
    print("STRENGTH OUTLIER")