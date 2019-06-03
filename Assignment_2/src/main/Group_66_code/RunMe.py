import math

from Assignment_2.src.main.Maze import Maze
from Assignment_2.src.main.Agent import Agent
from Assignment_2.src.main.Group_66_code.MyQLearning import MyQLearning
from Assignment_2.src.main.Group_66_code.MyEGreedy import MyEGreedy
import matplotlib.pyplot as plt
import matplotlib.colors


def found_optimum(steps, nr_lookback):
    if len(steps) < nr_lookback:
        return False
    reference = sum(steps[-nr_lookback:]) / nr_lookback
    for s in steps[-nr_lookback:]:
        if abs(s - reference) >= 0.1 * reference:
            return False
    return True


def parameterized_run(file, alpha, gamma, epsilon, nr_trials):
    """
    Run the learning algorithm using the given parameters.
    :param file: File of the maze to use
    :param alpha: alpha to use
    :param gamma: gamma to use
    :param epsilon: epsilon to use
    :param nr_trials: Number of trials before stopping the process
    :return: List of runs per trial for each trial
    """
    steps_per_trial = []

    maze = Maze(file)
    final_states = [
        maze.get_state(len(maze.states) - 1, len(maze.states[0]) - 1),
        maze.get_state(9, 0),
    ]

    maze.set_reward(maze.get_state(9, 9), 10)
    maze.set_reward(maze.get_state(9, 0), 5)
    agent = Agent(0, 0)
    greedy = MyEGreedy()
    q_learning = MyQLearning()

    base_epsilon = epsilon
    epsilon_reset = 0
    while len(steps_per_trial) < nr_trials:
        # Select EGreedy action
        current_state = agent.get_state(maze)
        action = greedy.get_egreedy_action(agent, maze, q_learning, epsilon)

        # Execute action
        state_next = agent.do_action(action, maze)

        # Update learning
        possible_actions = maze.get_valid_actions(agent)
        q_learning.update_q(current_state, action, maze.get_reward(state_next), state_next, possible_actions, alpha,
                            gamma)

        # Check if agent reached goal
        if state_next in final_states:
            steps_per_trial.append(agent.nr_of_actions_since_reset)
            agent.reset()

            # Check if last two runs were similar
            if found_optimum(steps_per_trial, 3):
                # Explore at least 5 runs
                if epsilon_reset > 5:
                    epsilon_reset = 0
                    epsilon = base_epsilon
                else:
                    epsilon = 0.8
                    epsilon_reset += 1
            else:
                if epsilon_reset > 5:
                    # If no optimum has been found, reset the epsilon to the original value
                    epsilon_reset = 0
                    epsilon = base_epsilon

    # Do greedy run (epsilon = 0) to determine if the higher reward (10) has been found
    while True:
        # Select EGreedy action
        current_state = agent.get_state(maze)
        action = greedy.get_egreedy_action(agent, maze, q_learning, 0)

        # Execute action
        state_next = agent.do_action(action, maze)

        # Update learning
        possible_actions = maze.get_valid_actions(agent)
        q_learning.update_q(current_state, action, maze.get_reward(state_next), state_next, possible_actions, alpha,
                            gamma)

        if state_next in final_states:
            print("reached final state with reward 10:", state_next == final_states[0])
            return steps_per_trial, state_next == final_states[0]


def compute_averages(items):
    """
    Input is a list containing multiple, equal lengh lists. The element-wise average for each list is computed.
    :param items: 2d list of numbers
    :return: list of averages of all input lists
    """
    list_averages = []
    for index in range(len(items[0])):
        t = 0
        for item in items:
            t += item[index]
        list_averages.append(t / len(items))
    return list_averages


def execute():
    file = "..\\..\\..\\resources\\toy_maze.txt"
    number_of_trials = 100  # Number of times the maze is completed each run
    number_of_runs = 50  # Number of times the run is repeated. Used to compute averages

    runs = []
    labels = []

    # Test different values for alpha, epsilon and gamma
    for alpha in [0.7]:
        for epsilon in [0.2]:
            for gamma in [0.9]:
                print("Alpha = {}, Epsilon = {}, Gamma = {}".format(alpha, epsilon, gamma))
                labels.append("Alpha = {}, Epsilon = {}, Gamma = {}".format(alpha, epsilon, gamma))

                count_preferred_10 = 0
                # Run 50 times to get smoothed results
                parameterized_runs = []
                for i in range(number_of_runs):
                    # print("Doing run ", i)
                    steps, preferred_10 = parameterized_run(file, alpha, gamma, epsilon, number_of_trials)
                    parameterized_runs.append(steps)
                    if preferred_10:
                        count_preferred_10 += 1

                # Store the average of the 50 runs
                print("Preferred reward 10: ", count_preferred_10, " out of ", number_of_runs)
                runs.append(compute_averages(parameterized_runs))

    # Plot the averages of all runs
    for run in runs:
        plt.plot(run)

    # Compute the averages per trial for each run
    # DISABLED AS IT DOESN'T MAKE SENSE IN THIS CASE

    # total_averages = []
    # for i in range(number_of_trials):
    #     total = 0
    #     for run in runs:
    #         total += run[i]
    #     total_averages.append(total / len(runs))

    # Plot the averages for each run
    # plt.plot(total_averages, color='tab:red', linewidth=3)
    # labels.append("Average")

    plt.legend(labels)
    plt.title('easy_maze' if file.endswith("easy_maze.txt") else "toy_maze")
    plt.xlabel('Trial')
    plt.ylabel('Steps in trial')
    plt.show()
    print("Done")


if __name__ == "__main__":
    execute()
