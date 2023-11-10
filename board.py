import tkinter as tk
import random

from animal import Animal
from pos import pos

class VirtualAnimal:
    def __init__(self, x, y):
        self.position = (x, y)

class SimulationVisualizer:
    def __init__(self, master, population):
        self.master = master
        self.master.title("Animal Simulation")

        self.canvas = tk.Canvas(master, width=400, height=400, bg='white')
        self.canvas.pack()

        self.population = population
        self.draw_animals()

    def draw_animals(self):
        for animal in self.population:
            pos = animal.position
            x = pos.x
            y = pos.y
            self.canvas.create_oval(x-5, y-5, x+5, y+5, fill='blue')  # Assuming radius is 5, change accordingly

    def update_visualization(self):
        # Implement update logic as needed
        pass

# Example usage:
# Assuming you have a list called 'population' containing VirtualAnimal objects
# and each VirtualAnimal object has a 'position' attribute of type tuple (x, y)
c1 = pos(50,50)
c2 = pos(70,50)
animal1 = Animal(name="Animal1", position = c1, size=10, speed=5, vision=8, strength=7, reproduction_rate=0.2, energy=50)
animal2 = Animal(name="Animal2", position = c2, size=12, speed=10, vision=7, strength=6, reproduction_rate=0.18, energy=45)

population = [animal1, animal2]

root = tk.Tk()
simulation_visualizer = SimulationVisualizer(root, population)
root.mainloop()