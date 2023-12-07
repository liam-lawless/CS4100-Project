# Natural Selection Simulator

## Introduction
The "Natural Selection Simulator" is a computational project designed to explore the processes of evolution and adaptation in changing environments using reinforcement learning. This project combines generative machine learning with basic biological concepts to simulate and analyze species adaptation in various environmental conditions. It aims to provide insights for practical applications in optimization, design, and biological understanding.

## Usage
Run the main.py to view the simulation. In the configuration constants, adjust the number of agents, food, adversaries, and generations as well as the environment size as desired.

## Project Structure
- **adversary.py**: Defines adversaries in the simulation, such as predators or competitive species.
- **agent.py**: Describes the agents subjected to natural selection, including their genetic traits and behaviors.
- **entity.py**: Base class for various entities in the simulation, such as agents and environmental features.
- **environment.py**: Constructs the simulation environment, encompassing terrain, resources, and conditions.
- **q_learning_model.py**: Implements the Q-learning model for agent behavior adaptation and learning.
- **simulation_view.py**: Manages the visual representation of the simulation, showing the evolution of agents and environment.
- **visualize.py**: Supplementary visualization tools and methods.
- **simulation.py**: Coordinates the entire simulation process, integrating agents, environment, and learning models.
- **main.py**: Entry point of the application, initiating the simulation setup and execution.
- **food.py**: Defines food resources in the environment, critical for agent survival and reproduction.
- **pos.py**: Defines an (X, Y) position on the game board for simulation visualization.

## Methods
The project employs agent-based modeling and genetic algorithms. Agents in the simulation have unique genetic traits affecting survival and reproduction, influenced by environmental factors like predators, resource availability, and user-defined constraints.

## Evaluation
The simulation is evaluated using metrics such as genetic diversity, adaptation rates, and species fitness. Visualizations illustrate evolutionary trajectories and population patterns.

## Significance
This project has implications for artificial intelligence, optimization, and education, offering an interactive tool to teach evolutionary concepts and address complex optimization challenges.

## License
MIT License