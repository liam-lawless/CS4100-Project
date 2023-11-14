import tkinter as tk
import random

from animal import Animal
from pos import pos

def getMovement(coords, dimensions):
    #topleft coords
    x1 = coords[0]
    y1 = coords[1]
    #bottomright coords
    x2 = coords[2]
    y2 = coords[3]
    width = dimensions[0]
    height = dimensions[1]
    delx = random.randint(-10,10)
    dely = random.randint(-10,10)
    #make sure top left corner is not out of bounds
    if x1+delx < 0:
        delx = delx*(-1)
    if y1+dely < 0:
        dely = dely*(-1)
    #make sure bottom right corner is not out of bounds
    if x2+delx > width:
        delx = delx*(-1)
    if y2+dely > height:
        dely = dely*(-1)
    return delx, dely

class SimulationVisualizer:
    def __init__(self, master, population):
        self.master = master
        self.master.title("Animal Simulation")
        self.width = 400
        self.height = 400
        self.canvas = tk.Canvas(master, width=400, height=400, bg='white')
        self.canvas.pack()

        self.population = population
        self.shapes = {} #use this to keep the shapes of animals so that it can be updated
        self.draw_animals()
        self.update_visualization()

    def draw_animals(self):
        for animal in self.population:
            pos = animal.position
            x = pos.x
            y = pos.y
            circle = self.canvas.create_oval(x-5, y-5, x+5, y+5, fill='blue')  # Assuming radius is 5, change accordingly
            self.shapes.update({animal:circle})

    def update_visualization(self):
        # Implement update logic as needed
        for animal, shape in self.shapes.items():
                delx, dely = getMovement(self.canvas.coords(shape),(self.width, self.height))
                self.canvas.move(shape, delx, dely)
                #updating the value of our animal as well
                animal.position = pos(animal.position.x+delx, animal.position.y+dely)
        self.master.after(100, self.update_visualization)
            

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

