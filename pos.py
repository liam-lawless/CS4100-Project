class pos:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __repr__(self):
        return f"Coordinate(x={self.x}, y={self.y})"

    def tup(self):
        return (self.x, self.y)

    def distance_to(self, other_coordinate):
        """
        Calculate the Euclidean distance between two coordinates.
        """
        return ((self.x - other_coordinate.x) ** 2 + (self.y - other_coordinate.y) ** 2) ** 0.5

# # Example usage:
# coord1 = Coordinate(0, 0)
# coord2 = Coordinate(3, 4)

# distance = coord1.distance_to(coord2)
# print(f"The distance between {coord1} and {coord2} is {distance}.")