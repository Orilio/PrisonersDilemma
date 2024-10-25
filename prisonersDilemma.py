import random
import networkx as nx
from itertools import combinations
import numpy as np
from enum import Enum


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
    def __init__(self, strategies, turns):
        self.strategies = strategies
        self.turns = turns
        self.graph = nx.DiGraph()
        self.graph.add_nodes_from(self.strategies)

    def run(self):
        for (u, v) in combinations(self.strategies, 2):
            print(f'u: {u},\t v: {v}')
            p1 = u()
            p2 = v()

            for round in range(self.turns):
                p1c = p1.choose_action(p2.history)
                p2c = p2.choose_action(p1.history)


class Match:
    def __init__(self, s1: Strategy, s2: Strategy, turns):
        pass


