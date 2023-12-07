"""
File name: visualize.py
Author(s): Liam Lawless
Date created: November 26, 2023
Last modified: November 26, 2023

Description:
Provides visualization functionality, offering methods to plot the distribution and historical trends of various traits among agents using matplotlib

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
    
    def plot_trait_history(self, ax, trait):
        # ax should be a single Axes object passed from the subplots
        ax.plot(self.trait_history[trait])
        ax.set_title(f'Average {trait.capitalize()} of Agents Over Generations')
        ax.set_xlabel('Generation')
        ax.set_ylabel(f'Average {trait.capitalize()}')
        ax.set_xticks(range(0, len(self.trait_history[trait]) + 1, 5))

    def visualize_history(self, traits):
        num_traits = len(traits)
        rows = 2
        cols = 3

        fig, axs = plt.subplots(rows, cols, figsize=(15, 10))  # Adjust the figsize as necessary

        # Flatten the axs array for easier indexing
        axs = axs.flatten()

        # Plot each trait in its respective subplot
        for i, trait in enumerate(traits):
            self.plot_trait_history(axs[i], trait)

        # If there are any empty subplots, turn them off
        for i in range(num_traits, rows * cols):
            axs[i].axis('off')

        plt.savefig("/Users/liamlawless/Desktop/2023-2024 School Year/CS4100/Natural Selection Simulator/figures/results.png")

        plt.tight_layout()  # Adjust the layout
        plt.show()


#self.plot_trait_distribution(trait)