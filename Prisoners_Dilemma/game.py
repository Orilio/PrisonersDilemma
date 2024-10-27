from typing import Type
import networkx as nx
from Prisoners_Dilemma.strategies import Strategy
from Prisoners_Dilemma.utils import Action, SCORE, match_score
from collections.abc import Iterator
from joblib import Parallel, delayed
import pandas as pd


C, D = Action.C, Action.D


def rr_tournament_pairings(strategies) -> Iterator[tuple[Type[Strategy], Type[Strategy]]]:
    """
    Generator for match pairings in a round robin tournament.
    """
    for i, s1 in enumerate(strategies):
        for s2 in strategies[i:]:
            yield (s1, s2)


class Tournament:
    def __init__(self, strategies: list[Type[Strategy]], turns, n_jobs=None):
        self.strategies = strategies
        self.turns = turns
        self.graph = nx.Graph()
        self.graph.add_nodes_from(self.strategies)
        self.n_jobs = n_jobs

    def match_up(self, s1, s2):
        match = Match(s1, s2, self.turns)
        self.graph.add_edge(s1, s2, match=match)
        match.play()
        match.score = match_score(match.history)

    def play(self):
        for s1, s2 in rr_tournament_pairings(self.strategies):
            # if self.n_jobs is not None:
            #     Parallel(n_jobs=self.n_jobs)(delayed(self.match_up(s1, s2)))
            # else:
            #     self.match_up(s1, s2)
            print(f's1: {s1},\t s2: {s2}')
            self.match_up(s1, s2)

    def show_scores(self):
        adj = nx.adjacency_data(self.graph)['adjacency']
        scores = [[match['match'].score for match in group]for group in adj]
        strategy_names = [s.__name__ for s in self.strategies]
        score_matrix = pd.DataFrame(
            scores, index=strategy_names, columns=strategy_names)
        return score_matrix


class Match:
    def __init__(self, s1: Type[Strategy], s2: Type[Strategy], turns):
        self.p1 = s1(s1.__name__)
        self.p2 = s2(s2.__name__)
        self.turns = turns
        self.history = []
        self.score = tuple()

    def play(self):
        for _ in range(self.turns):
            p1c, p2c = self.play_turn()

    def play_turn(self) -> tuple[Action, Action]:
        if self.history:
            p1h, p2h = zip(*self.history)
            p1h, p2h = list(p1h), list(p2h)
        else:
            p1h, p2h = [], []
        p1_action = self.p1.choose_action(p2h)
        p2_action = self.p2.choose_action(p1h)

        self.p1.history.append(p1_action)
        self.p2.history.append(p2_action)
        self.history.append((p1_action, p2_action))
        return p1_action, p2_action

    def __str__(self) -> str:
        s = f'{self.p1.name}  VS  {self.p2.name}\n'
        s += f'{self.turns} turns:\n'

        for t, (t1, t2) in enumerate(self.history):
            s += f'{t+1}:\t{t1.name} {t2.name}\n'
        return s
