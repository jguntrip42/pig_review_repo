class Pig:
    """
    Simple value-iteration solver for the dice game Pig.

    State:
        (i, j, k)

    where:
        i = current player's score
        j = opponent's score
        k = current player's turn total

    Value:
        V[(i, j, k)] = probability that the current player wins
                      from this state, assuming optimal play.
    """

    def __init__(self, target=100):
        self.target = target

        # All non-terminal states.
        # i and j are both below target.
        # k can go from 0 up to target - i - 1.
        self.states = []

        for i in range(target):
            for j in range(target):
                for k in range(target - i):
                    self.states.append((i, j, k))

        # Reverse order helps because high-score states are updated earlier.
        self.states.reverse()

        # Initial value estimates.
        self.values = {}

        for state in self.states:
            self.values[state] = 0.0

        # Policy will store either "roll" or "hold" for each state.
        self.policy = {}

        for state in self.states:
            self.policy[state] = None

    def is_winning_state(self, state):
        """
        A state is winning if current score + turn total reaches the target.
        """
        i, j, k = state
        return i + k >= self.target

    def is_losing_state(self, state):
        """
        A state is losing if the opponent has already reached the target.
        """
        i, j, k = state
        return j >= self.target

    def value(self, state):
        """
        Return the probability of winning from a state.

        Terminal cases:
            If current player can win, value = 1.
            If opponent has already won, value = 0.
        """
        if self.is_winning_state(state):
            return 1.0

        if self.is_losing_state(state):
            return 0.0

        return self.values[state]

    def hold_value(self, state):
        """
        Value if the current player holds.

        If current player holds:
            current player's score becomes i + k
            opponent becomes the current player
            turn total resets to 0

        New state from opponent's point of view:
            (j, i + k, 0)

        Opponent's win probability:
            value((j, i + k, 0))

        Current player's win probability:
            1 - opponent's win probability
        """
        i, j, k = state

        opponent_state = (j, i + k, 0)

        return 1.0 - self.value(opponent_state)

    def roll_value(self, state):
        """
        Value if the current player rolls.

        Six possible die results:

            roll 1:
                lose turn total
                opponent's turn starts from (j, i, 0)

            roll 2,3,4,5,6:
                add roll to turn total
                state becomes (i, j, k + roll)

        The expected value is the average over all six outcomes.
        """
        i, j, k = state

        # Case: roll a 1
        value_if_roll_1 = 1.0 - self.value((j, i, 0))

        # Cases: roll 2, 3, 4, 5, 6
        value_if_roll_2_to_6 = 0.0

        for roll in range(2, 7):
            next_state = (i, j, k + roll)
            value_if_roll_2_to_6 += self.value(next_state)

        # Average over six equally likely die results
        return (value_if_roll_1 + value_if_roll_2_to_6) / 6.0

    def best_action_and_value(self, state):
        """
        Compare rolling and holding.
        Return the better action and its value.
        """
        roll = self.roll_value(state)
        hold = self.hold_value(state)

        if roll > hold:
            return "roll", roll
        else:
            return "hold", hold

    def value_iteration(self, tolerance=1e-8, max_iterations=10000, print_its=True):
        """
        Repeatedly update values until they stop changing much.
        """
        for iteration in range(1, max_iterations + 1):
            biggest_change = 0.0

            for state in self.states:
                old_value = self.values[state]

                best_action, new_value = self.best_action_and_value(state)

                self.values[state] = new_value
                self.policy[state] = best_action

                change = abs(new_value - old_value)

                if change > biggest_change:
                    biggest_change = change
            
            if print_its == True:
                print(f"Iteration {iteration}, biggest change = {biggest_change}")

            if biggest_change < tolerance:
                print("Converged!")
                print(f"Number of iterations: {iteration}")
                return

        print("Warning: value iteration did not converge.")

    def get_value(self, i, j, k):
        """
        Easy way to access a value.
        """
        return self.value((i, j, k))

    def get_policy(self, i, j, k):
        """
        Easy way to access the optimal action.
        """
        return self.policy[(i, j, k)]