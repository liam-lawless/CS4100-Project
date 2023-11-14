class Food:
    def __init__(self, position, energy):
        self.position = position
        self.energy = energy

    def __repr__(self):
        return f"Food(Position: ({self.position.x}, {self.position.y}), Energy: {self.energy})"
