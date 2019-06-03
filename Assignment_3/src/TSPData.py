import os
import sys

from Assignment_3.src.Route import Route, read_route

sys.path.append(os.path.dirname(os.path.dirname(os.path.realpath(__file__))))

import pickle
import re
import traceback
from Assignment_3.src.AntColonyOptimization import AntColonyOptimization
from Assignment_3.src.Coordinate import Coordinate
from Assignment_3.src.Maze import Maze
from Assignment_3.src.PathSpecification import PathSpecification


# Class containing the product distances. Can be either build from a maze, a product
# location list and a PathSpecification or be reloaded from a file.
class TSPData:

    # Constructs a new TSP data object.
    # @param productLocations the product locations.
    # @param spec the path specification.
    def __init__(self, product_locations, spec):
        self.product_locations = product_locations
        self.spec = spec

        self.distances = None
        self.start_distances = None
        self.end_distances = None
        self.product_to_product = None
        self.start_to_product = None
        self.product_to_end = None

    # Calculate the routes from the product locations to each other, the start, and the end.
    # Additionally generate arrays that contain the length of all the routes.
    # @param maze
    def calculate_routes(self, aco):
        self.product_to_product = self.build_distance_matrix(aco)
        self.start_to_product = self.build_start_to_products(aco)
        self.product_to_end = self.build_products_to_end(aco)
        self.build_distance_lists()
        return

    # Build a list of integer distances of all the product-product routes.
    def build_distance_lists(self):
        number_of_products = len(self.product_locations)
        self.distances = []
        self.start_distances = []
        self.end_distances = []

        for i in range(number_of_products):
            self.distances.append([])
            for j in range(number_of_products):
                self.distances[i].append(self.product_to_product[i][j].size())
            self.start_distances.append(self.start_to_product[i].size())
            self.end_distances.append(self.product_to_end[i].size())
        return

    # Distance product to product getter
    # @return the list
    def get_distances(self):
        return self.distances

    # Distance start to product getter
    # @return the list
    def get_start_distances(self):
        return self.start_distances

    # Distance product to end getter
    # @return the list
    def get_end_distances(self):
        return self.end_distances

    # Equals method
    # @param other other TSPData to check
    # @return boolean whether equal
    def __eq__(self, other):
        return self.distances == other.distances \
               and self.product_to_product == other.product_to_product \
               and self.product_to_end == other.product_to_end \
               and self.start_to_product == other.start_to_product \
               and self.spec == other.spec \
               and self.product_locations == other.product_locations

    # Persist object to file so that it can be reused later
    # @param filePath Path to persist to
    def write_to_file(self, file_path):
        pickle.dump(self, open(file_path, "wb"))
        print("done writing")

    # Write away an action file based on a solution from the TSP problem.
    # @param productOrder Solution of the TSP problem
    # @param filePath Path to the solution file
    def write_action_file(self, product_order, file_path):
        total_length = self.start_distances[product_order[0]]
        for i in range(len(product_order) - 1):
            frm = product_order[i]
            to = product_order[i + 1]
            total_length += self.distances[frm][to]

        total_length += self.end_distances[product_order[len(product_order) - 1]] + len(product_order)

        string = ""
        string += str(total_length)
        string += ";\n"
        string += str(self.spec.get_start())
        string += ";\n"
        string += str(self.start_to_product[product_order[0]])
        string += "take product #"
        string += str(product_order[0] + 1)
        string += ";\n"

        for i in range(len(product_order) - 1):
            frm = product_order[i]
            to = product_order[i + 1]
            string += str(self.product_to_product[frm][to])
            string += "take product #"
            string += str(to + 1)
            string += ";\n"
        string += str(self.product_to_end[product_order[len(product_order) - 1]])

        f = open(file_path, "w")
        f.write(string)

    # Calculate the optimal routes between all the individual routes
    # @param maze Maze to calculate optimal routes in
    # @return Optimal routes between all products in 2d array
    def build_distance_matrix(self, aco):
        number_of_product = len(self.product_locations)
        # product_to_product = [[None] * number_of_product] * number_of_product
        product_to_product = []
        for i in range(number_of_product):
            product_to_product.append([])
            for j in range(number_of_product):
                print("i=", i, "j=", j)
                file_string = "./../solutions/tsp_routes/route_{}_{}.txt".format(i, j)
                start = self.product_locations[i]
                end = self.product_locations[j]
                if i == j:
                    print("equal")
                    # Distance between same point is 0
                    product_to_product[i].append(Route(start, route=[], reduced=[]))
                    continue
                elif i > j:
                    print("already discovered")
                    # Distance i -> j is equal to distance j -> i, route is the inverse
                    inverse_file_string = "./../solutions/tsp_routes/route_{}_{}.txt".format(j, i)
                    route_j_i = self.must_path(inverse_file_string, aco, end, start)

                    product_to_product[i].append(route_j_i.reverse())
                    # product_to_product[i].append(product_to_product[j][i])
                    continue
                else:
                    print("finding shortest route between", i, "and", j)
                    product_to_product[i].append(self.must_path(file_string, aco, start, end))

        print("Done computing distances between products")
        return product_to_product

    @staticmethod
    def must_path(file_string, aco, start, end):
        """
        Must path tries finding a path, even upon failures. If the path is already saved, it skips.
        If a path is found ,it is written to the file and returned
        :param file_string: filename to write to
        :param aco: ant colony optimization
        :param start: start coordinates
        :param end: end coordinates
        :return: route between start and end
        """
        existing_route = None
        if os.path.isfile(file_string):
            print("File known, loading")
            existing_route = read_route(file_string)
            return existing_route
        while True:
            try:
                route_i_j = aco.find_shortest_route(PathSpecification(start, end))
                # product_to_product[i][j] = route_i_j
                if route_i_j.size() < existing_route.size():
                    print("Improved on route:", file_string, existing_route.size(), " -> ", route_i_j.size())
                    route_i_j.write_to_file(file_string)
                    return route_i_j
                else:
                    print("No improvement", existing_route.size(), " -> ", route_i_j.size())
                    return existing_route
            except Exception as e:
                traceback.print_exc()
                print("failed, retrying")

    # Calculate optimal route between the start and all the products
    # @param maze Maze to calculate optimal routes in
    # @return Optimal route from start to products
    def build_start_to_products(self, aco):
        start = self.spec.get_start()
        start_to_products = []
        for i in range(len(self.product_locations)):
            file_string = "./../solutions/tsp_routes/route_start_{}.txt".format(i)

            print("finding shortest route between start and", i)
            found_route = self.must_path(file_string, aco, start, self.product_locations[i])
            start_to_products.append(found_route)
        return start_to_products

    # Calculate optimal routes between the products and the end point
    # @param maze Maze to calculate optimal routes in
    # @return Optimal route from products to end
    def build_products_to_end(self, aco):
        end = self.spec.get_end()
        products_to_end = []
        for i in range(len(self.product_locations)):
            file_string = "./../solutions/tsp_routes/route_{}_end.txt".format(i)

            print("finding shortest route between", i, "and end")
            found_route = self.must_path(file_string, aco, self.product_locations[i], end)

            products_to_end.append(found_route)
        return products_to_end

    # Load TSP data from a file
    # @param filePath Persist file
    # @return TSPData object from the file
    @staticmethod
    def read_from_file(file_path):
        return pickle.load(open(file_path, "rb"))

    # Read a TSP problem specification based on a coordinate file and a product file
    # @param coordinates Path to the coordinate file
    # @param productFile Path to the product file
    # @return TSP object with uninitiatilized routes
    @staticmethod
    def read_specification(coordinates, product_file):
        try:
            f = open(product_file, "r")
            lines = f.read().splitlines()

            firstline = re.compile("[:,;]\\s*").split(lines[0])
            product_locations = []
            number_of_products = int(firstline[0])
            for i in range(number_of_products):
                line = re.compile("[:,;]\\s*").split(lines[i + 1])
                product = int(line[0])
                x = int(line[1])
                y = int(line[2])
                product_locations.append(Coordinate(x, y))
            spec = PathSpecification.read_coordinates(coordinates)
            return TSPData(product_locations, spec)
        except FileNotFoundError:
            print("Error reading file " + product_file)
            traceback.print_exc()
            sys.exit()


def run():
    # parameters
    ants_per_generation = 25
    number_generations = 25
    q = 1000
    evap = 0.2
    persist_file = "./../tmp/productMatrixDist"
    tsp_path = "./../resources/tsp products.txt"
    coordinates = "./../resources/hard coordinates.txt"

    # construct optimization
    maze = Maze.create_maze("./../resources/hard maze.txt")
    pd = TSPData.read_specification(coordinates, tsp_path)
    aco = AntColonyOptimization(maze, ants_per_generation, number_generations, q, evap, plotting=False)

    # run optimization and write to file
    pd.calculate_routes(aco)
    pd.write_to_file(persist_file)

    # read from file and print
    pd2 = TSPData.read_from_file(persist_file)
    print(pd == pd2)


# Assignment 2.a
if __name__ == "__main__":
    run()
