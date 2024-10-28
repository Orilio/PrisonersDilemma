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

# ------------------------------------------------------------------------


class TidemanAndChieruzzi(Strategy):
    '''
    Submitted by Nicolas Tideman and Paula Chieruzzi.

    description:

    > "This rule begins with cooperation and tit for tat. However, when
    > the other player finishes his second run of defections, an extra
    > punishment is instituted, and the number of punishing defections
    > is increased by one with each run of the other's defections.
    > The other player is given a fresh start if he is 10 or more points
    > behind, if he has not just started a run of defections, if it has
    > been at least 20 moves since a fresh start, if there are at
    > least 10 moves remaining, and if the number of defections differs
    > from a 50-50 random generator by at least 3.0 standard deviations.
    > A fresh start involves two cooperations and then play as if
    > the game had just started. The program defects automatically
    > on the last two moves."

    This strategy came 2nd in Axelrod's original tournament.
    '''

    def __init__(self, name):
        super().__init__(name)
        self.is_fresh_start = True
        self.rounds_since_fresh_start = 0
        self.rounds_remaining = 200
        self.number_of_opponent_defections = 0
        
    def choose_action(self, opponent_history) -> Action:
        if self.rounds_remaining <=


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
    '''
    Submitted by James Graaskamp.

    description:

    > "This rule plays tit for tat for 50 moves, defects on move 51, and
    > then plays 5 more moves of tit for tat. A check is then made to
    > see if the player seems to be RANDOM, in which case it defects
    > from then on. A check is also made to see if the other is TIT
    > FOR TAT, ANALOGY (a program from the preliminary tournament),
    > and its own twin, in which case it plays tit for tat. Otherwise
    > it randomnly defects every 5 to 15 moves, hoping that enough trust
    > has been built up so that the other player will not notice
    > these defections."

    This strategy came 9th in Axelrod's original tournament.
    '''


'''
    # Initialize move history
    my_moves = []
    opponent_moves = []

    # Initialize flags and counters
    is_random = False
    identified_opponent_type = False
    defection_interval = random.randint(5, 15)  # Random interval for defection between 5 and 15 moves

    # Main function for each round
    def graaskamp_strategy(round_num, opponent_move):
        global is_random, identified_opponent_type, defection_interval
        
        # Update history
        if round_num > 0:
            my_moves.append(last_move)
            opponent_moves.append(opponent_move)
        
        # Initial Tit-for-Tat for the first 50 moves
        if round_num == 0:
            last_move = "cooperate"
            return last_move
        
        if round_num <= 50:
            last_move = opponent_moves[-1]  # Tit-for-Tat (mimic opponent's last move)
            return last_move
        
        # Move 51: Test Defection
        if round_num == 51:
            last_move = "defect"
            return last_move
        
        # Moves 52-56: Return to Tit-for-Tat after defection test
        if round_num <= 56:
            last_move = opponent_moves[-1]  # Tit-for-Tat
            return last_move
        
        # Detect opponent type after 56 moves
        if not identified_opponent_type:
            # Detect if opponent is RANDOM or a known type (Tit-for-Tat, Analogy, or Graaskamp's Twin)
            if detect_random_behavior(opponent_moves):  # Define a function to detect randomness
                is_random = True
                identified_opponent_type = True
            elif detect_known_type(opponent_moves):  # Define a function to detect known types
                identified_opponent_type = True
        
        # If opponent is detected as random, defect continuously
        if is_random:
            last_move = "defect"
            return last_move
        
        # If opponent is identified as known type, continue Tit-for-Tat
        if identified_opponent_type:
            last_move = opponent_moves[-1]
            return last_move
        
        # If opponent type is neither random nor known, defect randomly every 5-15 moves
        if round_num % defection_interval == 0:
            last_move = "defect"
            defection_interval = random.randint(5, 15)  # Recalculate the interval for next random defection
        else:
            last_move = opponent_moves[-1]  # Otherwise, play Tit-for-Tat
        
        return last_move

    # Helper function to detect if opponent is RANDOM (dummy example function)
    def detect_random_behavior(opponent_moves):
        # Implement statistical test for randomness, e.g., calculate variance in opponent's moves
        pass
    
    import numpy as np
    from scipy.stats import chi2

    def detect_random_behavior(opponent_moves):
        """
        Detects if the opponent's moves are random based on variance, autocorrelation, and runs test.
        
        Parameters:
            opponent_moves (list of str): List of opponent's moves where 'cooperate' is represented by 1 and 'defect' by 0.

        Returns:
            bool: True if opponent behavior is detected as random, False otherwise.
        """
        # Convert moves to numeric form: 'cooperate' = 1, 'defect' = 0
        moves = [1 if move == "cooperate" else 0 for move in opponent_moves]
        
        # Check if we have enough moves to analyze
        if len(moves) < 10:
            return False  # Not enough data to make a determination

        # 1. Variance Check
        move_variance = np.var(moves)
        if 0.2 < move_variance < 0.8:
            # Variance in a random binary sequence is typically around 0.25 (for equal 1s and 0s).
            variance_check = True
        else:
            variance_check = False

        # 2. Autocorrelation Check (Lag-1)
        mean_moves = np.mean(moves)
        autocorrelation = np.corrcoef(moves[:-1], moves[1:])[0, 1] if len(moves) > 1 else 0
        if abs(autocorrelation) < 0.1:
            autocorrelation_check = True
        else:
            autocorrelation_check = False

        # 3. Runs Test
        # Count runs in the sequence
        runs = 1  # Start with 1 run
        for i in range(1, len(moves)):
            if moves[i] != moves[i - 1]:
                runs += 1

        n1 = sum(moves)  # Count of cooperate moves
        n2 = len(moves) - n1  # Count of defect moves
        expected_runs = (2 * n1 * n2) / (n1 + n2) + 1
        variance_runs = (2 * n1 * n2 * (2 * n1 * n2 - n1 - n2)) / ((n1 + n2) ** 2 * (n1 + n2 - 1))
        z_score = (runs - expected_runs) / np.sqrt(variance_runs) if variance_runs != 0 else 0

        # The 95% confidence interval for a standard normal distribution is roughly [-1.96, 1.96]
        if abs(z_score) < 1.96:
            runs_test_check = True
        else:
            runs_test_check = False

        # If all tests suggest randomness, we classify the behavior as random
        return variance_check and autocorrelation_check and runs_test_check


    # Helper function to detect if opponent is a known type
    def detect_known_type(opponent_moves):
        # Implement checks for specific patterns for known types like Tit-for-Tat, Analogy, or Graaskamp's Twin
        pass

'''


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
