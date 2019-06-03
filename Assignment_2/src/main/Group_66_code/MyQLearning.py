from Assignment_2.src.main.QLearning import QLearning


class MyQLearning(QLearning):

    def __init__(self):
        QLearning.__init__(self)

    def update_q(self, state, action, r, state_next, possible_actions, alpha, gamma):
        old_value = self.get_q(state, action)

        next_state_values = [self.get_q(state_next, a) for a in possible_actions]
        max_q = 0
        for value in next_state_values:
            if value > max_q:
                max_q = value

        delta = (alpha * (r + (gamma * max_q) - old_value))
        if delta < 0.0001:
            return

        self.set_q(state, action, old_value + delta)
        return
