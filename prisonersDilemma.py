import random

def random_choice(p: float = 0.5):
    if p == 0:
        return 'D'
    if p == 1:
        return 'C'
    
    r = random.random()
    if r < p:
        return 'C'
    return 'D'


class Tournament:
    def __init__(self, strategies, rounds):
        self.strategies = strategies
        self.rounds = rounds

    def run(self):
        for round in range(self.rounds):
            # for i in range\
            pass


class Strategy:
    def __init__(self, name):
        self.name = name
        self.history = []

    def choose_action(self, opponent_history):
        pass


class AlwaysCooperate(Strategy):
    def choose_action(self, opponent_history):
        return 'C'


class AlwaysDefect(Strategy):
    def choose_action(self, opponent_history):
        return 'D'


class TitForTat(Strategy):
    def choose_action(self, opponent_history):
        if not opponent_history:
            return 'C'
        return opponent_history[-1]


class Grofman(Strategy):
    '''
    Submitted by Bernard Grofman.
    
    description:
    > "If the players did different things on the previous move, this rule
    > cooperates with probability 2/7. Otherwise this rule always cooperates."
    
    This strategy came 4th in Axelrod's original tournament.
    '''
    
    def choose_action(self, opponent_history):
        if not opponent_history or self.history[-1] == opponent_history[-1]:
            return 'C'
        return random_choice(2 / 7)