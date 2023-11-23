from agent import Agent

class QLearningAgent(Agent):
    def __init__(self, traits, energy, q_table=None):
        ...

    def get_state(self, environment):
        ...

    def choose_action(self, state):
        ...

    def update_q_table(self, state, action, reward, next_state):
        ...

    def act(self, environment):
        ...
