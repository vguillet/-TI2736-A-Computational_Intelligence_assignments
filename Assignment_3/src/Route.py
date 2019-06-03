import os
import sys
import traceback

from Assignment_3.src.Coordinate import Coordinate

sys.path.append(os.path.dirname(os.path.dirname(os.path.realpath(__file__))))

from Assignment_3.src.Direction import Direction


# Class representing a route.
class Route:

    # Route takes a starting coordinate to initialize
    # @param start starting coordinate
    def __init__(self, start, route=None, reduced=None):
        self.route = route or []
        self.start = start
        self.reduced = reduced or []

    # After taking a step we add the direction we moved in
    # @param dir Direction we moved in
    def add(self, dir):
        self.route.append(dir)
        return

    # Returns the length of the route
    # @return length of the route
    def size(self):
        return len(self.reduced)

    # Getter for the list of directions
    # @return list of directions
    def get_route(self):
        return self.route

    # Getter for the starting coordinate
    # @return the starting coordinate
    def get_start(self):
        return self.start

    # Function that checks whether a route is smaller than another route
    # @param other the other route
    # @return whether the route is shorter
    def shorter_than(self, other):
        return self.size() < other.size()

    # Take a step back in the route and return the last direction
    # @return last direction
    def remove_last(self):
        return self.route.pop()

    def reduce(self):
        """
        Reduces the cells visited in the route. If a cell is visited twice, all steps between the two visits are removed.
        For example: the route covering cells [a, b, c, d, e, b, f] will be reduced to [a, b, f].
        The reduced route is stored in self.reduced
        """
        # print("reducing, start at ", len(self.route))

        reduced_route = []
        cell = self.start
        index = 0
        # Visited maps the cell to the index in the route list
        visited = {cell: index}

        for direction in self.route:
            cell = cell.add_direction(direction)
            if cell in visited:
                # Cell was already visited. Get the index of the step taken after the cell was visited
                index = visited[cell]
                # Invalidate all steps after this cell was visited
                del reduced_route[index:]
                # Invalidate all visited cells with a higher index
                visited = {k: v for k, v in visited.items() if v <= index}

            else:
                # Cell was not visited, so add to new route
                reduced_route.append(direction)
                index = index + 1
                visited[cell] = index
        self.reduced = reduced_route

    def reverse(self):
        # Find end of route (= start of new route)
        end = self.start
        for direction in self.route:
            end = end.add_direction(direction)

        new_route = []
        for direction in reversed(self.route):
            new_route.append(Direction.opposite_direction(direction))

        new_reduced = []
        for direction in reversed(self.reduced):
            new_reduced.append(Direction.opposite_direction(direction))

        return Route(end, route=new_route, reduced=new_reduced)

    # Build a string representing the route as the format specified in the manual.
    # @return string with the specified format of a route
    def __str__(self):
        string = ""
        # for dir in self.route:
        for dir in self.reduced:
            string += str(Direction.dir_to_int(dir))
            string += ";\n"
        return string

    # Equals method for route
    # @param other Other route
    # @return boolean whether they are equal
    def __eq__(self, other):
        return self.start == other.start and self.route == other.route

    # Method that implements the specified format for writing a route to a file.
    # @param filePath path to route file.
    # @throws FileNotFoundException
    def write_to_file(self, file_path):
        f = open(file_path, "w")
        string = ""
        string += str(self.size())
        string += ";\n"
        string += str(self.start)
        string += ";\n"
        string += str(self)
        f.write(string)


def read_route(file_name):
    try:
        f = open(file_name, "r")
        raw_lines = f.read().splitlines()
        route_size = int(raw_lines[0].strip(";"))

        start_coordinates = [int(num.strip()) for num in raw_lines[1].split(";")[0].split(",")]
        steps = []
        for i in range(2, route_size + 2):
            direction = Direction(int(raw_lines[i].strip(";")))
            steps.append(direction)

        route = Route(Coordinate(start_coordinates[0], start_coordinates[1]), route=steps, reduced=steps)
        return route
    except FileNotFoundError:
        print("Error reading coordinate file " + file_name)
        traceback.print_exc()
        print("Returning none")
        return None
