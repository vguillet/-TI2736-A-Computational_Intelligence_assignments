import os
import sys

from Assignment_3.src.Ant import Ant
from Assignment_3.src.Route import Route

sys.path.append(os.path.dirname(os.path.dirname(os.path.realpath(__file__))))

import time
from Assignment_3.src.Maze import Maze
from Assignment_3.src.PathSpecification import PathSpecification

import matplotlib.pyplot as plt
import numpy as np
import matplotlib.colors as colors


# Class representing the first assignment. Finds shortest path between two points in a maze according to a specific
# path specification.
class AntColonyOptimization:

    # Constructs a new optimization object using ants.
    # @param maze the maze .
    # @param antsPerGen the amount of ants per generation.
    # @param generations the amount of generations.
    # @param Q normalization factor for the amount of dropped pheromone
    # @param evaporation the evaporation factor.
    def __init__(self, maze, ants_per_gen, generations, q, evaporation, plotting=False):
        self.maze = maze
        self.ants_per_gen = ants_per_gen
        self.generations = generations
        self.q = q
        self.rho = evaporation
        self.plotting = plotting

    # Loop that starts the shortest path process
    # @param spec Specification of the route we wish to optimize
    # @return ACO optimized route
    def find_shortest_route(self, path_specification):
        self.maze.reset()
        shortest_route = None

        # Plot the base pheromones (just a map of the maze)
        if self.plotting:
            show_pheromones(self.maze, 0)

        # Run all generations
        for gen in range(self.generations):
            print("Running generation", gen)
            generation_routes = []

            # Release a ants per generation
            for a in range(self.ants_per_gen):
                ant = Ant(self.maze, path_specification)
                new_route = ant.find_route()
                # print("route length:", len(new_route.reduced))
                generation_routes.append(new_route)

                # Update the shortest route if the new route is shorter
                if shortest_route is None or new_route.shorter_than(shortest_route):
                    shortest_route = new_route

            # Update pheromones at the end of the generation
            self.maze.evaporate(self.rho)
            self.maze.add_pheromone_routes(generation_routes, self.q)

            # Plot the pheromones after this generation
            if self.plotting and gen % 5 == 0:
                show_pheromones(self.maze, gen)
        if self.plotting:
            show_pheromones(self.maze, "final pheromones")
        return shortest_route


def show_pheromones(maze, generation):
    """
    Plot the distribution of the pheromones in a heatmap.
    :param maze: The maze to plot the pheromones of
    :return: nothing
    """
    # Find minimal and maximal pheromone for normalization in the heatmap
    min_pheromone = 100000
    max_pheromone = 0
    for row in maze.pheromones:
        for p in row:
            if p <= 1:
                # Don't cover cells with at most the base pheromone
                continue
            max_pheromone = max(max_pheromone, p)
            min_pheromone = min(min_pheromone, p)

    # Handle base case where no pheromone has been dropped yet
    if max_pheromone == 0:
        max_pheromone = 1
    if min_pheromone == 100000:
        min_pheromone = 1

    # Show the pheromones in a heatmap, normalized for the minimal and maximal non-default values
    fig, ax = plt.subplots()
    ax.imshow(np.array(maze.pheromones).transpose(), norm=colors.LogNorm(vmin=min_pheromone, vmax=max_pheromone))
    ax.set_title("Generation " + str(generation))
    fig.tight_layout()
    plt.show()


def run():
    # Maze to run
    maze_type = "hard"

    # parameters
    ants_per_generation = 25
    number_generations = 30
    q = 1600
    evaporation_rate = 0.35

    # construct the optimization objects
    maze = Maze.create_maze("./../resources/{} maze.txt".format(maze_type))
    spec = PathSpecification.read_coordinates("./../resources/{} coordinates.txt".format(maze_type))
    aco = AntColonyOptimization(maze, ants_per_generation, number_generations, q, evaporation_rate, plotting=True)

    # save starting time
    start_time = int(round(time.time() * 1000))

    # run optimization
    shortest_route = aco.find_shortest_route(spec)

    # print time taken
    print("Time taken: " + str((int(round(time.time() * 1000)) - start_time) / 1000.0))

    # save solution
    shortest_route.write_to_file("./../solutions/{}_solution.txt".format(maze_type))

    # print route size
    print("Route size: " + str(shortest_route.size()))


# Driver function for Assignment 1
if __name__ == "__main__":
    run()
