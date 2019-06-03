import os
import sys

from Assignment_3.src.Direction import Direction
from Assignment_3.src.SurroundingPheromone import SurroundingPheromone

sys.path.append(os.path.dirname(os.path.dirname(os.path.realpath(__file__))))

import traceback


# Class that holds all the maze data. This means the pheromones, the open and blocked tiles in the system as
# well as the starting and end coordinates.
class Maze:

    # Constructor of a maze
    # @param walls int array of tiles accessible (1) and non-accessible (0)
    # @param width width of Maze (horizontal)
    # @param length length of Maze (vertical)
    def __init__(self, walls, width, length):
        self.walls = walls
        self.length = length
        self.width = width
        self.start = None
        self.end = None
        self.pheromones = []
        self.initialize_pheromones()

    # Initialize pheromones to a start value.
    def initialize_pheromones(self):
        # Set all pheromones to 0 in the initial stage
        self.pheromones = [[self.walls[y][x] for x in range(self.length)] for y in range(self.width)]

        # self.pheromones = [[1] * self.length for _ in range(self.width)]
        return

    # Reset the maze for a new shortest path problem.
    def reset(self):
        self.initialize_pheromones()

    # Update the pheromones along a certain route according to a certain Q
    # @param r The route of the ants
    # @param Q Normalization factor for amount of dropped pheromone
    def add_pheromone_route(self, route, q):
        if len(route.route) == 0:
            return
        pheromone_update = q / route.size()

        cell = route.start
        self.pheromones[cell.x][cell.y] += pheromone_update

        for direction in route.reduced:
            cell = cell.add_direction(direction)
            self.pheromones[cell.x][cell.y] += pheromone_update
        return

    # Update pheromones for a list of routes
    # @param routes A list of routes
    # @param Q Normalization factor for amount of dropped pheromone
    def add_pheromone_routes(self, routes, q):
        # print("Adding on routes")
        for r in routes:
            self.add_pheromone_route(r, q)

    # Evaporate pheromone
    # @param rho evaporation factor
    def evaporate(self, rho):
        # print("Evaporating")
        for x in range(len(self.pheromones)):
            for y in range(len(self.pheromones[x])):
                if self.pheromones[x][y] <= 1:
                    continue
                else:
                    self.pheromones[x][y] = max(self.pheromones[x][y] * (1 - rho), 1)
        return

    # Width getter
    # @return width of the maze
    def get_width(self):
        return self.width

    # Length getter
    # @return length of the maze
    def get_length(self):
        return self.length

    # Returns a the amount of pheromones on the neighbouring positions (N/S/E/W).
    # @param position The position to check the neighbours of.
    # @return the pheromones of the neighbouring positions.
    def get_surrounding_pheromone(self, position):
        return SurroundingPheromone(
            self.get_pheromone(position.add_direction(Direction.north)),
            self.get_pheromone(position.add_direction(Direction.east)),
            self.get_pheromone(position.add_direction(Direction.south)),
            self.get_pheromone(position.add_direction(Direction.west)),
        )

    # Pheromone getter for a specific position. If the position is not in bounds returns 0
    # @param pos Position coordinate
    # @return pheromone at point
    def get_pheromone(self, pos):
        if not self.in_bounds(pos):
            return 0
        return self.pheromones[pos.x][pos.y]

    # Check whether a coordinate lies in the current maze.
    # @param position The position to be checked
    # @return Whether the position is in the current maze
    def in_bounds(self, position):
        return position.x_between(0, self.width) and position.y_between(0, self.length)

    def get_steps(self, position):
        """
        Finds all possible steps (not walls) from the given position
        :param position: coordinate object where to find steps from
        :return: list of (new_coordinate, direction, pheromone) triples for each possible step
        """
        possible_directions = [Direction.north, Direction.east, Direction.south, Direction.west]
        possible_steps = []

        for d in possible_directions:
            new_position = position.add_direction(d)
            if self.in_bounds(new_position) and self.get_pheromone(new_position) > 0:
                possible_steps.append((new_position, d, self.get_pheromone(new_position)))

        return possible_steps

    # Representation of Maze as defined by the input file format.
    # @return String representation
    def __str__(self):
        string = ""
        string += str(self.width)
        string += " "
        string += str(self.length)
        string += " \n"
        for y in range(self.length):
            for x in range(self.width):
                string += str(self.walls[x][y])
                string += " "
            string += "\n"
        return string

    # Method that builds a mze from a file
    # @param filePath Path to the file
    # @return A maze object with pheromones initialized to 0's inaccessible and 1's accessible.
    @staticmethod
    def create_maze(file_path):
        try:
            f = open(file_path, "r")
            lines = f.read().splitlines()
            dimensions = lines[0].split(" ")
            width = int(dimensions[0])
            length = int(dimensions[1])

            # make the maze_layout
            maze_layout = []
            for x in range(width):
                maze_layout.append([])

            for y in range(length):
                line = lines[y + 1].split(" ")
                for x in range(width):
                    if line[x] != "":
                        state = int(line[x])
                        maze_layout[x].append(state)
            print("Ready reading maze file " + file_path)
            return Maze(maze_layout, width, length)
        except FileNotFoundError:
            print("Error reading maze file " + file_path)
            traceback.print_exc()
            sys.exit()
