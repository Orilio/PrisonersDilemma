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
    def choose_action(self, opponent_history) -> Action:
        return random_choice()


class AlwaysCooperate(Strategy):
    def choose_action(self, opponent_history) -> Action:
        return C


class AlwaysDefect(Strategy):
    def choose_action(self, opponent_history) -> Action:
        return D


class TitForTat(Strategy):
    def choose_action(self, opponent_history) -> Action:
        if not opponent_history:
            return C
        return opponent_history[-1]


class TidemanAndChieruzzi(Strategy):
    pass


class Nydegger(Strategy):
    '''
    Submitted by Rudy Nydegger.

    description:

    > "The program begins with tit for tat for the first three moves,
    > except that if it was the only one to cooperate on the first move
    > and the only one to defect on the second move, it defects on the
    > third move. After the third move, its choice is determined from
    > the 3 preceding outcomes in the following manner. Let A be the
    > sum formed by counting the other's defection as 2 points and one's
    > own as 1 point, and giving weights of 16, 4, and 1 to the
    > preceding three moves in chronological order. The choice can be
    > described as defecting only when A equals
    > 1, 6, 7, 17, 22, 23, 26, 29, 30, 31, 33, 38, 39, 45, 49, 54, 55, 58, or 61.
    > Thus if all three preceding moves are mutual defection,
    > A = 63 and the rule cooperates. This rule was designed for use
    > in laboratory experiments as a stooge which had a memory and
    > appeared to be trustworthy, potentially cooperative, but
    > not gullible (Nydegger, 1978)"

    .. math::

        A = 16 a_1 + 4 a_2 + a_3
    '''
    @staticmethod
    def get_points(interaction: tuple[Action, Action]):
        return interaction[0].value + (2 * interaction[1].value)

    @staticmethod
    def is_a(prev_3_interactions: list[tuple[Action, Action]]):
        A = 0
        for i, weight in [(-1, 16), (-2, 4), (-3, 1)]:
            A += weight * Nydegger.get_points(prev_3_interactions[i])

        return A in [1, 6, 7, 17, 22, 23, 26, 29, 30, 31, 33, 38, 39, 45, 49, 54, 55, 58, 61]

    def choose_action(self, opponent_history) -> Action:
        if not self.history:
            return C
        elif len(self.history) < 3:
            return opponent_history[-1]
        elif len(self.history) == 3:
            if (self.history[0] == C and opponent_history[0] == D and
                    self.history[1] == D and opponent_history[1] == C):
                return D
            return C
        elif Nydegger.is_a(list(zip(self.history, opponent_history))[-3:]):
            return D
        else:
            return C


class Grofman(Strategy):
    '''
    Submitted by Bernard Grofman.

    description:

    > "If the players did different things on the previous move, this rule
    > cooperates with probability 2/7. Otherwise this rule always cooperates."

    This strategy came 4th in Axelrod's original tournament.
    '''

    def choose_action(self, opponent_history) -> Action:
        if not self.history or self.history[-1] == opponent_history[-1]:
            return C
        return random_choice(2 / 7)


class Shubik(Strategy):
    '''
    Submitted by Martin Shubik.

    description:

    > "This rule cooperates until the other defects, and then defects
    > once. If the other defects again after the rule's cooperation is
    > resumed, the rule defects twice. In general, the length of
    > retaliation is increased by one for each departure from mutual
    > cooperation. This rule is described with its strategic implications
    > in Shubik (1970). Further treatment of its is given in Taylor (1976)."


    > Note that this rule's retaliation streak is re-activated and its
    > retaliation length is raised only when the opponent defects on
    > this rule's cooperation.

    > This means that the rule is indifferent to
    > opponent moves while on a retaliatory streak. 

    This strategy came 5th in Axelrod's original tournament.
    '''

    def __init__(self, name):
        super().__init__(name)
        self.is_retaliating = False
        self.retaliations_left = 0
        self.retaliation_length = 0

    def choose_action(self, opponent_history) -> Action:
        if not self.history:
            return C

        if self.is_retaliating:
            self.retaliations_left -= 1
            self.is_retaliating = self.retaliations_left > 0
            return D

        if self.history[-1] == C and opponent_history[-1] == D:
            self.is_retaliating = True
            self.retaliation_length += 1
            self.retaliations_left = self.retaliation_length - 1
            self.is_retaliating = self.retaliations_left > 0
            return D
        return C


class SteinAndRapoport(Strategy):
    pass


class Friedman(Strategy):
    '''
    Submitted by James W. Friedman.
    (aka Grudger)

    description:

    > "This rule cooperates until the other player defects, and then
    > defects until the end of the game. This strategy was described in
    > the context of the Prisoner's Dilemma by Harris (1969). Its 
    > properties in a broader class of games have been developed by
    > Friedman (1971)."

    This strategy came 7th in Axelrod's original tournament.
    '''

    def __init__(self, name):
        super().__init__(name)
        self.is_retaliating = False

    def choose_action(self, opponent_history) -> Action:
        if self.is_retaliating:
            return D
        if self.history and opponent_history[-1] == D:
            self.is_retaliating = True
            return D
        return C


class Davis(Strategy):
    '''
    Submitted by Morton Davis.

    description:

    > "This rule cooperates on the first ten moves, and then if there is
    > a defection it defects until the end of the game."

    This strategy came 8th in Axelrod's original tournament.
    '''

    def __init__(self, name):
        super().__init__(name)
        self.beginning_moves_left = 10
        self.is_retaliating = False

    def choose_action(self, opponent_history) -> Action:
        if self.beginning_moves_left > 0:
            self.beginning_moves_left -= 1
            return C

        if self.is_retaliating:
            return D
        if self.history and opponent_history[-1] == D:
            self.is_retaliating = True
            return D
        return C


class Graaskamp(Strategy):
    pass


class Downing(Strategy):
    pass


class Feld(Strategy):
    pass


class Joss(Strategy):
    '''
    Submitted by Johann Joss.

    description:

    > "This rule cooperates 90% of the time after a cooperation by the other.
    > It always defects after a defection by the other."
    '''

    def choose_action(self, opponent_history) -> Action:
        if not self.history or opponent_history[-1] == C:
            return random_choice(0.9)
        return D


class Tullock(Strategy):
    pass


class NameWithheld(Strategy):
    pass
