import random
import sys

from Assignment_2.src.main.QLearning import QLearning


class MyEGreedy:

    def __init__(self):
        self.previous_action_opposite = None

    def get_random_action(self, agent, maze):
        # Select a random action (1)
        actions = maze.get_valid_actions(agent)
        return random.choice(actions)

    def get_best_action(self, agent, maze, q_learning):
        # Get all possible actions
        actions = maze.get_valid_actions(agent)

        # Remove the opposite of the previous action from the possible actions to prevent the agent going back on itself
        if self.previous_action_opposite in actions:
            actions.remove(self.previous_action_opposite)
        if len(actions) is 0:
            action = self.previous_action_opposite
            self.previous_action_opposite = maze.get_opposite_action(action)
            return action

        best_actions = []
        best_action_value = -1
        # Get the values associated to all possible actions
        for (action, value) in q_learning.get_action_values(agent.get_state(maze), actions):
            if value > best_action_value:
                best_actions = [action]
                best_action_value = value
            elif value is best_action_value:
                best_actions.append(action)

        # Pick random action from the best actions
        best_action = random.choice(best_actions)
        self.previous_action_opposite = maze.get_opposite_action(best_action)
        return best_action

    def get_egreedy_action(self, agent, maze, q_learning, epsilon):
        # Select a random action (1)
        if random.random() > epsilon:
            return self.get_best_action(agent, maze, q_learning)
        return self.get_random_action(agent, maze)
