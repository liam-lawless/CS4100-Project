## Priority List
*What needs to be accomplished next?*

**TODO**
- ~~Abstract adversary and agent classes, extract commonalities/methods or make an abstract class that they both extend from. Many similar methods~~
- ~~Implement adversaries~~
    - ~~Adversary needs to eat N amount of agents per day to survive, otherwise dies.~~
- Implement QLearning
- Implement more actions
    - ~~flee~~ 
    - ~~return home~~
    - die of old age
    - ~~sated (or should it be kept as greedy i.e. agents eat as much as they want)~~
    - ~~reproduce~~
    - big agents eat little agents? Implement functionality for size
- ~~Implement generations~~
- Implement graphs and visualizations
- Document code
- Unit Test
- Unrelated to code base, create powerpoint presentation for project

Needs to happen eventually in no apparent order:
- Circle back to the cost function to determine how much energy is used per step

Bonus:
- Implement clicking on an agent and getting its stats relayed back to the user

#### Notes
- Should agents that have run out of energy and are stuck in place be vulnerable to adversaries?
- How many generations before agents die of old age?
- What is a good mutation rate? Find the balance between number of generations and number of mutations