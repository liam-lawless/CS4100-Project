"""
File name: simulation_view.py
Author(s): Liam Lawless
Date created: November 23, 2023
Last modified: November 23, 2023

Description:
    This file contains the SimulationView class, which handles all the graphical representations of the simulation on the Tkinter canvas.

Dependencies:

"""

class SimulationView:
    def __init__(self, canvas, environment):
        self.canvas = canvas
        self.environment = environment
        self.agent_shapes = {}  # Maps agents to their canvas shapes
        self.food_shapes = {}   # Maps Food objects to their canvas shapes
        self.draw_initial_state()

    def draw_initial_state(self):
        self.draw_agents()
        self.draw_food()

    def draw_agents(self):
        for shape in self.agent_shapes.values():
            self.canvas.delete(shape)
        self.agent_shapes = {}

        for agent in self.environment.population:
            x, y = agent.position.x, agent.position.y
            shape = self.canvas.create_oval(
                x - agent.ENTITY_RADIUS, y - agent.ENTITY_RADIUS,
                x + agent.ENTITY_RADIUS, y + agent.ENTITY_RADIUS,
                fill='blue'
            )
            self.agent_shapes[agent] = shape

    def draw_food(self):
        for shape in self.food_shapes.values():
            self.canvas.delete(shape)
        self.food_shapes = {}

        for food_item in self.environment.food:
            x, y = food_item.position.x, food_item.position.y
            shape = self.canvas.create_oval(
                x - food_item.ENTITY_RADIUS, y - food_item.ENTITY_RADIUS,
                x + food_item.ENTITY_RADIUS, y + food_item.ENTITY_RADIUS,
                fill='green'
            )
            self.food_shapes[food_item] = shape

    def update_view(self):
        self.draw_agents()
        self.draw_food()
