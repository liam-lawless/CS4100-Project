## Priority List
*What needs to be accomplished next?*

**TODO**
- Implmenent speed system for animals traversing around board
- Implement agent thought process
    - agents going from moving in a calculated manner to searching for food


Needs to happen in no apparent order:


#### Notes

- What acual generative ML model are we going to implement for all of these agents?
    - Is there some pre-defined package we could already utilize that will run our simulation a given number of times? Qlearning & pytorch
- Weather? Probs not
- Reproducing:
    - Asexual: 1 food = survive, 2 food = reproduction 
    - CANCELLED Sexual: 2 mates, offspring inherits combination of traits from each parent
- Array mapped to the board size
- speed is a measurement of how many ticks have to pass before an animal can move again
    - e.g. default speed  = 50 max (fastest speed) = 1

- Once all food is gone from a level, the generation stops