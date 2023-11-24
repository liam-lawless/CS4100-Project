import tkinter as tk
import random
from pos import Pos

class Environment:
    ENTITY_RADIUS = 5  # Constant for the size of entities

    def __init__(self, master, population, food, bounds):
        self.master = master
        self.master.title("Natural Selection Simulation")
        self.canvas = tk.Canvas(master, width=bounds[0], height=bounds[1], bg='white')
        self.canvas.pack()

        self.population = population
        self.food = food
        self.bounds = bounds
        self.agent_shapes = {}  # Maps agents to their canvas shapes
        self.food_shapes = {}   # Map Food objects to their canvas shapes

        self.tick_rate = 100    # how many ms between each update on the canvas

    def run(self):
        self.draw_initial_state()

    def draw_initial_state(self):
        self.draw_entities(self.population, 'blue')
        self.draw_entities(self.food, 'green')

    def draw_entities(self, entities, color):
        for entity in entities:
            x, y = entity.position.x, entity.position.y
            shape = self.canvas.create_oval(
                x - Environment.ENTITY_RADIUS,
                y - Environment.ENTITY_RADIUS,
                x + Environment.ENTITY_RADIUS,
                y + Environment.ENTITY_RADIUS,
                fill=color
            )
            if color == 'blue':
                self.agent_shapes[entity] = shape
            elif color == 'green':
                self.food_shapes[entity] = shape

    def update_environment(self):
        # Updates the environment without rescheduling itself
        for agent, shape in self.agent_shapes.items():
            if agent.energy > 0:
                delta_x, delta_y = self.calculate_movement_delta(self.canvas.coords(shape))
                self.canvas.move(shape, delta_x, delta_y)
                # Update the agent's position
                agent.position.x += delta_x
                agent.position.y += delta_y

        self.check_for_collisions()

    def calculate_movement_delta(self, current_coords):
        # Calculate the movement delta for the shape while keeping it within bounds 
        entity_radius = 5
        x1, y1, x2, y2 = current_coords
        width, height = self.bounds

        # Random movement delta
        delta_x = random.randint(-10, 10)
        delta_y = random.randint(-10, 10)

        # Correct movement to ensure the shape stays within the canvas bounds
        new_x1 = max(entity_radius, min(width - entity_radius, x1 + delta_x))
        new_y1 = max(entity_radius, min(height - entity_radius, y1 + delta_y))

        # Calculate the actual delta to apply
        adjusted_delta_x = new_x1 - x1
        adjusted_delta_y = new_y1 - y1

        return adjusted_delta_x, adjusted_delta_y
    
    def check_for_collisions(self):
        for agent in self.population:
            agent_shape = self.agent_shapes[agent]
            agent_coords = self.canvas.coords(agent_shape)
            for food_item in self.food[:]:  # Copy the list to avoid modification during iteration
                food_coords = self.canvas.coords(self.food_shapes[food_item])
                if self.is_collision(agent_coords, food_coords):
                    agent.consume_food()
                    self.remove_food(food_item)

    def is_collision(self, agent_coords, food_coords):
        # Check if agent and food coordinates overlap (simple bounding-box collision detection)
        agent_left, agent_top, agent_right, agent_bottom = agent_coords
        food_left, food_top, food_right, food_bottom = food_coords
        return not (agent_right < food_left or agent_left > food_right or
                    agent_bottom < food_top or agent_top > food_bottom)

    def remove_food(self, food_item):
        # Remove the food item from the canvas and the food list
        shape_to_delete = self.food_shapes[food_item]
        self.canvas.delete(shape_to_delete)
        self.food.remove(food_item)
        del self.food_shapes[food_item]
    