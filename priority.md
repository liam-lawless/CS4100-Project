## Priority List
*What needs to be accomplished next?*

1. Set up a controller (main.py)
2. Implement game tick system that allows animals to move (set up in controller), add tick to animal class

Needs to happen in no apparent order:
- Implement food items (file and class structure {pos, energy_amount}) **WIP**
- Change to asexual reproduction for offspring (makes the project much easier long term) **DONE**
- Switch trait mutation from floats to int & mutation either by +1 or -1, no floats **DONE**
- Implmenent speed system for animals traversing around board

#### Notes

- What acual generative ML model are we going to implement for all of these agents?
    - Is there some pre-defined package we could already utilize that will run our simulation a given number of times?
- Weather?
- Reproducing:
    - Asexual: 1 food = survive, 2 food = reproduction
    - CANCELLED Sexual: 2 mates, offspring inherits combination of traits from each parent
- Array mapped to the board size
- speed is a measurement of how many ticks have to pass before an animal can move again
    - e.g. default speed  = 50 max (fastest speed) = 1

- Once all food is gone from a level, the generation stops