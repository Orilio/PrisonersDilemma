import random
from enum import Enum
import numpy as np


class Action(Enum):
    """Actions in the Prisoner's Dilemma"""
    C = 0
    D = 1

C, D = Action.C, Action.D

# class Score():
#     def __init__(self, r, s, t, p ) -> None:
#         pass
#     pass

"""
T R S P dictionary:

    If both players cooperate, they both receive the reward R for cooperating.
    If both players defect, they both receive the punishment payoff P.
    If Blue defects while Red cooperates, then Blue receives the temptation payoff T,
    while Red receives the "sucker's" payoff, S.
"""
r = 3  # Score obtained by both players for mutual cooperation
s = 0  # Score obtained by a player for cooperating against a defector
t = 5  # Score obtained by a player for defecting against a cooperator
p = 1  # Score obtained by both players for mutual defection

SCORE = np.array([[r, s], [t, p]])


def random_choice(p: float = 0.5) -> Action:
    return C if random.random() < p else D
