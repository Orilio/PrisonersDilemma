from typing import Type
import networkx as nx
from itertools import combinations
from Prisoners_Dilemma.strategies import Strategy
from Prisoners_Dilemma.utils import Action
from Prisoners_Dilemma.utils import SCORE


C, D = Action.C, Action.D


class Tournament:
    def __init__(self, strategies: list[Type[Strategy]], turns):
        self.strategies = strategies
        self.turns = turns
        self.graph = nx.DiGraph()
        self.graph.add_nodes_from(self.strategies)

    def run(self):
        for (u, v) in combinations(self.strategies, 2):
            print(f'u: {u},\t v: {v}')
            p1 = u()
            p2 = v()


class Match:
    def __init__(self, s1: Type[Strategy], s2: Type[Strategy], turns):
        self.p1 = s1(s1.__name__)
        self.p2 = s2(s2.__name__)
        self.turns = turns
        self.history = []

    def play(self):
        for _ in range(self.turns):
            p1c, p2c = self.play_turn()

    def play_turn(self) -> tuple[Action, Action]:
        p1h, p2h = zip(*self.history)
        p1h, p2h = list(p1h), list(p2h)

        p1_action = self.p1.choose_action(p2h)
        p2_action = self.p2.choose_action(p1h)

        self.p1.history.append(p1_action)
        self.p2.history.append(p2_action)
        self.history.append((p1_action, p2_action))
        return p1_action, p2_action

    def __str__(self) -> str:
        s = f"""{self.p1.name}  VS  {self.p2.name}
        {self.turns} turns:
        """

        for t, (t1, t2) in enumerate(self.history):
            s += f'{t+1}:\t{t1.name} {t2.name}\n'
        return s
