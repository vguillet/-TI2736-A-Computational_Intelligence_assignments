import os
import sys

sys.path.append(os.path.dirname(os.path.dirname(os.path.realpath(__file__))))

import random
from Assignment_3.src.Route import Route


# Class that represents the ants functionality.
class Ant:

    # Constructor for ant taking a Maze and PathSpecification.
    # @param maze Maze the ant will be running in.
    # @param spec The path specification consisting of a start coordinate and an end coordinate.
    def __init__(self, maze, path_specification):
        self.maze = maze
        self.start = path_specification.get_start()
        self.end = path_specification.get_end()
        self.current_position = self.start
        self.rand = random
        self.previous_direction_opposite = None

    # Method that performs a single run through the maze by the ant.
    # @return The route the ant found through the maze.
    def find_route(self):
        route = Route(self.start)

        # Keep stepping as long as the ant isn't at the end
        while self.current_position != self.end:
            step = self.get_step()
            self.previous_direction_opposite = step[1].opposite_direction()
            route.add(step[1])
            self.current_position = step[0]

        route.reduce()
        return route

    def get_step(self):
        """
        Compute the step the ant will take based on the maze and the ant's current position.
        :return: A step triple: (new_coordinate, direction_taken, pheromone_at_new_coordinate)
        """
        possible_steps = self.maze.get_steps(self.current_position)

        # Remove previous direction as option
        viable_steps = []
        back_step = None
        total_surrounding_pheromone = 0

        for s in possible_steps:
            if self.previous_direction_opposite is not None and s[1] == self.previous_direction_opposite:
                back_step = s
            else:
                total_surrounding_pheromone += s[2]
                viable_steps.append(s)

        # If no other steps are present, allow stepping back
        if len(viable_steps) == 0:
            return back_step

        # Randomize the order in which possible steps will be evaluated
        random.shuffle(viable_steps)

        # Pick a step to take
        random_number = self.rand.random()
        for step in viable_steps:
            # Compute probability this step should be taken
            relative_pheromone = step[2] / total_surrounding_pheromone

            # Take this step if the probability roll picked this step
            if relative_pheromone >= random_number:
                return step
            else:
                random_number -= relative_pheromone

        # If for some reason no step was found, return the last step evaluated
        print("found no step")
        return viable_steps[len(viable_steps) - 1]
