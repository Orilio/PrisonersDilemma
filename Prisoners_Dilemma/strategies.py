from typing import Type
from abc import ABC, abstractmethod
from Prisoners_Dilemma.utils import random_choice
from Prisoners_Dilemma.utils import Action

C, D = Action.C, Action.D


class Strategy(ABC):
    def __init__(self, name):
        self.name = name
        self.history = []

    @abstractmethod
    def choose_action(self, opponent_history) -> Action:
        pass


class Random(Strategy):
    def choose_action(self, opponent_history):
        return random_choice()


class AlwaysCooperate(Strategy):
    def choose_action(self, opponent_history):
        return C


class AlwaysDefect(Strategy):
    def choose_action(self, opponent_history):
        return D


class TitForTat(Strategy):
    def choose_action(self, opponent_history):
        if not opponent_history:
            return C
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
            return C
        return random_choice(2 / 7)


class Joss(Strategy):
    '''
    Submitted by Johann Joss.

    description:
    > "This rule cooperates 90% of the time after a cooperation by the other.
    > It always defects after a defection by the other."
    '''
    
    def choose_action(self, opponent_history):
        if opponent_history[-1]
