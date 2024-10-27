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


def interaction_score(pair: tuple[Action, Action]):
    a1, a2 = (a.value for a in pair)
    return (SCORE[a1][a2], SCORE[a2][a1])


def match_score(match_history: list[tuple]):
    scores = [interaction_score(pair) for pair in match_history]
    return tuple(sum(player_score) for player_score in zip(*scores))
