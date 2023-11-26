"""
File name: visualize.py
Author(s): Liam Lawless
Date created: November 26, 2023
Last modified: November 26, 2023

Description:

Dependencies:

"""

import matplotlib.pyplot as plt
import numpy as np

class Visualize:

    def __init__(self, trait_distribution, trait_history):
        self.trait_distribution = trait_distribution
        self.trait_history = trait_history

    def plot_trait_distribution(self, trait):
        max_trait_value = max(self.trait_distribution[trait])
        bins = np.arange(0, max_trait_value + 1.1, 0.1)  # Bins from 0 to max value + 1, with step size 0.1

        plt.figure()
        plt.hist(self.trait_distribution[trait], bins=bins, edgecolor='black')
        plt.xticks(np.arange(0, max_trait_value + 1, 0.5))  # Ticks every 0.5
        plt.title(f'Distribution of {trait.capitalize()} Among Agents')
        plt.xlabel(trait.capitalize())
        plt.ylabel('Number of Agents')
        plt.show()

    def plot_trait_history(self, trait):
        plt.figure()
        plt.plot(self.trait_history[trait], marker='o')
        plt.title(f'Average {trait.capitalize()} of Agents Over Generations')
        plt.xlabel('Generation')
        plt.ylabel(f'Average {trait.capitalize()}')
        plt.xticks(range(0, len(self.trait_history[trait]) + 1, 5))
        plt.show()

    def visualize(self, trait):
        self.plot_trait_history(trait)
        self.plot_trait_distribution(trait)