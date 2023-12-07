"""
File name: pos.py
Author(s): Liam Lawless
Date created: November 10, 2023
Last modified: November 23, 2023

Description:
    This file provides the Pos class, which defines a position with x and y coordinates and supports distance calculations.

"""

class Pos:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __repr__(self):
        return f"Coordinate(x={self.x}, y={self.y})"

    def tup(self):
        return (self.x, self.y)

    # Calculate the Euclidean distance between two coordinates.
    def distance_to(self, other_coordinate):

        return ((self.x - other_coordinate.x) ** 2 + (self.y - other_coordinate.y) ** 2) ** 0.5
