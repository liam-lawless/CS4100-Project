## Priority List
*What needs to be accomplished next?*

**TODO**
- ~~Abstract adversary and agent classes, extract commonalities/methods or make an abstract class that they both extend from. Many similar methods~~
- ~~Implement adversaries~~
    - ~~Adversary needs to eat N amount of agents per day to survive, otherwise dies.~~
- ~~Implement size functionality~~
- Implement QLearning
- ~~Implement more actions~~
    - ~~flee~~ 
    - ~~return home~~
    - ~~die of old age~~
    - ~~sated (or should it be kept as greedy i.e. agents eat as much as they want)~~
    - ~~reproduce~~
    - ~~big agents eat little agents~~
- ~~Implement generations~~
- ~~Implement graphs and visualizations~~
- Document code
- Unit Test
- Unrelated to code base, create powerpoint presentation for project
- Get rid of dots on the graphs
- negative reward for staying in place for too long

Presentation:
- Populations converging towards specific situations

Needs to happen eventually in no apparent order:
- ~~Circle back to the cost function to determine how much energy is used per step~~
- Make a central place where game characteristics can be manipulated easily by the user
    - Food count
    - Adversary count
    - Agent count
    - Mutation probability
    - Mutation amount
    - Number of generations
    - Delay between generations (that might want to be somehow calculated based on the number of generations. e.g. low number is slow, high number is fast)
    - Tick speed (similar idea to the latter. Lower tick speed value the more generations that pass)

Bonus:
- Implement clicking on an agent and getting its stats relayed back to the user
- Imbed the histogram into the bottom of the canvas mid simulation
    - demonstrated partially in test.py

### Bugs
- ~~If all the agents die in a generation, the next generation crashed because div by 0~~

#### Notes
- Should agents that have run out of energy and are stuck in place be vulnerable to adversaries?
- How many generations before agents die of old age?
- What is a good mutation rate? Find the balance between number of generations and number of mutations