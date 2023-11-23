import tkinter as tk
import random

from agent import Agent
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

class Environment:
    def __init__(self, master, population, food):
        self.master = master
        self.master.title("Natural Selection Simulation")
        self.width = 400
        self.height = 400
        self.canvas = tk.Canvas(master, width=400, height=400, bg='white')
        self.canvas.pack()

        self.population = population
        self.food = food
        self.shapes = {} #use this to keep the shapes of animals so that it can be updated
        self.draw_agents()
        self.draw_food()
        self.update_visualization()

    def draw_agents(self):
        for animal in self.population:
            pos = animal.position
            x = pos.x
            y = pos.y
            circle = self.canvas.create_oval(x-5, y-5, x+5, y+5, fill='blue')  # Assuming radius is 5, change accordingly
            self.shapes.update({animal:circle})

    def update_visualization(self):
        # Implement update logic as needed
        for agent, shape in self.shapes.items():
                delx, dely = getMovement(self.canvas.coords(shape),(self.width, self.height))
                self.canvas.move(shape, delx, dely)
                #updating the value of our animal as well
                agent.position = pos(agent.position.x+delx, agent.position.y+dely)
        self.master.after(100, self.update_visualization)

    def draw_food(self):
        for item in self.food:
            pos = item.position
            x = pos.x
            y = pos.y
            circle = self.canvas.create_oval(x-5, y-5, x+5, y+5, fill='green')  # Assuming radius is 5, change accordingly

