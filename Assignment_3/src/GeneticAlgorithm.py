import os, sys

sys.path.append(os.path.dirname(os.path.dirname(os.path.realpath(__file__))))

import random
from Assignment_3.src.TSPData import TSPData


class TSPSolution:
    def __init__(self, order):
        self.order = order
        self.length = compute_distance(order)
        self.fitness = 1000 / self.length

    def compute_fitness(self, min_length, max_length):
        return
        # self.fitness = 1000 / self.length
        # self.fitness = min_length + max_length - self.length
        # print("Setting fitness", min_length, max_length, self.length, self.fitness)
        # self.fitness = max(max_length - self.length, 0.0000001)

    def __eq__(self, other):
        for index in range(len(self.order)):
            if self.order[index] != other.order[index]:
                return False
        return True


# TSP problem solver using genetic algorithms.
class GeneticAlgorithm:

    # Constructs a new 'genetic algorithm' object.
    # @param generations the amount of generations.
    # @param popSize the population size.
    def __init__(self, generations, pop_size, mutation_rate=0.015, crossover_rate=0.7):
        self.generations = generations
        self.pop_size = pop_size
        self.mutation_rate = mutation_rate
        self.crossover_rate = crossover_rate

    # Knuth-Yates shuffle, reordering an array randomly
    # @param chromosome array to shuffle.
    def shuffle(self, chromosome):
        n = len(chromosome)
        for i in range(n):
            r = i + int(random.uniform(0, 1) * (n - i))
            swap = chromosome[r]
            chromosome[r] = chromosome[i]
            chromosome[i] = swap
        return chromosome

    # This method should solve the TSP.
    # @param pd the TSP data.
    # @return the optimized product sequence.
    def solve_tsp(self):
        # Create starting population
        population = []
        for _ in range(self.pop_size):
            population.append(TSPSolution(self.shuffle([0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17])))

        print("Starting length:", get_shortest(population).length)

        for generation in range(self.generations):
            print("Running generation", generation)

            num_duplicates = 0
            for i in range(self.pop_size):
                for j in range(i, self.pop_size):
                    if i == j:
                        continue
                    if population[i].__eq__(population[j]):
                        # print(population[i].order, population[j].order)
                        num_duplicates += 1
            # print("Generation contains duplicates:", num_duplicates)

            # Compute fitness for each route
            min_length = min([solution.length for solution in population])
            max_length = max([solution.length for solution in population])

            for solution in population:
                solution.compute_fitness(min_length, max_length)

            new_population = []

            while len(new_population) < self.pop_size:
                # Select two random routes using roulette selection
                # TODO: Pick parents via tournament selection (and implement tournament selection)
                # parent_1, parent_2 = roulette_selection(population)
                parent_1, parent_2 = naive_tournament(population)
                (new_1, new_2) = self.crossover(parent_1, parent_2)
                new_population.append(new_1)
                new_population.append(new_2)

            # Mutate entire new population
            population = [self.mutate(solution) for solution in new_population]

            # Print new lengths
            best_solution = population[0]
            for solution in population:
                if solution.length < best_solution.length:
                    best_solution = solution
            print("Best solution, length:", best_solution.length, "fitness:", best_solution.fitness)

        return get_shortest(population).order

    def crossover(self, solution_1, solution_2):
        """
        Compute a crossover of this solution with another solution
        :param solution_1: First solution
        :param solution_2: Second solution
        :return: One new solution
        """
        if random.random() >= self.crossover_rate:
            # RNJesus decided no crossover is going to take place
            return solution_1, solution_2

        # Possible improvements:
        #  - Only select the two most fit routes from the four
        random_index_1 = random.randint(0, len(solution_1.order) - 1)
        random_index_2 = random_index_1
        while random_index_1 == random_index_2:
            random_index_2 = random.randint(0, len(solution_1.order) - 1)

        begin_index = min(random_index_1, random_index_2)
        end_index = max(random_index_1, random_index_2)

        return self.crossover_index(solution_1, solution_2, begin_index, end_index), \
               self.crossover_index(solution_2, solution_1, begin_index, end_index)

    @staticmethod
    def crossover_index(solution_1, solution_2, begin_index, end_index):
        """
        Regular crossover cannot be used as it might introduce duplicate products.
        This method takes a begin and end index and copies the sub-route from solution_1 corresponding to these indices
        directly to the new route. The rest of the route is filled up with the remaining products, in the order in which
        they appear in solution_2
        :param solution_1: First solution
        :param solution_2: Second solution
        :param begin_index: Starting index for copying route
        :param end_index: Ending index for copying route
        :return: New route with the ordering copied
        """
        new_order = [-1] * len(solution_1.order)
        taken_numbers = {}
        for index in range(begin_index, end_index):
            new_order[index] = solution_1.order[index]
            taken_numbers[solution_1.order[index]] = True

        # Add unvisited numbers in order of solution 1
        index = 0
        for number in solution_2.order:
            if index == begin_index:
                index = end_index
            if number in taken_numbers:
                continue

            new_order[index] = number
            index += 1

        return TSPSolution(new_order)

    def mutate(self, solution):
        """
        Mutation is done by swapping two random products in the ordering. Swapping occurs with a set probability
        :param solution: Base solution
        :return: Solution with two products swapped
        """
        if random.random() >= self.mutation_rate:
            # RNJesus decided no mutation is going to take place
            return solution

        random_index_1 = random.randint(0, len(solution.order) - 1)
        random_index_2 = random.randint(0, len(solution.order) - 1)

        print("Mutating:", random_index_1, random_index_2, len(solution.order))
        swap = solution.order[random_index_1]
        solution.order[random_index_1] = solution.order[random_index_2]
        solution.order[random_index_2] = swap
        return solution


def compute_distance(order):
    """
    Computes the total distance of the given ordering
    :param order: Oder of product indices (0 to 17) to visit
    :return: Total distance of the given ordering
    """
    total_distance = tsp_data.start_distances[order[0]]
    for i in range(len(order) - 1):
        total_distance += tsp_data.distances[i][i + 1]
    total_distance += tsp_data.end_distances[len(order) - 1]
    return total_distance


def roulette_selection(population):
    """
    Select two random routes from the population, based on a weighted sum over the fitness
    :param population: list of (route, fitness) tuples
    :return: two random tuples selected on weighted fitness (high fitness = high probability)
    """
    total_fitness = sum([solution.fitness for solution in population])
    parent_1_index = roulette_selection_weighted(population, total_fitness)
    parent_2_index = parent_1_index
    while parent_2_index == parent_1_index:
        parent_2_index = roulette_selection_weighted(population, total_fitness)

    # print("Selected indices:", parent_1_index, parent_2_index)
    return population[parent_1_index], population[parent_2_index]


def roulette_selection_weighted(population, total_fitness):
    """
    Select one random index from the population based on weighted fitness
    :param population: list of (route, fitness) tuples
    :param total_fitness: total fitness of all solutions
    :return: random index from 0 to len(population)-1
    """
    random_number = random.random()
    # Find first index
    for index in range(len(population)):
        relative_probability = population[index].fitness / total_fitness
        if relative_probability >= random_number:
            return index
        else:
            random_number -= relative_probability

    # Return last item if no match was found
    return population[len(population) - 1]


def naive_tournament(population, tournament_size=5):
    """
    Performs the naive tournament selection twice to get two distinct parents to use
    :param population: List of solutions to pick from
    :param tournament_size: Number of solutions randomly picked
    :return: Two randomly picked solutions
    :return:
    """
    # TODO: Implement proper tournament selection
    parent_1 = naive_tournament_select(population, tournament_size)
    parent_2 = parent_1
    while parent_1 == parent_2:
        parent_2 = naive_tournament_select(population, tournament_size)
    print("picked", parent_1.order, parent_2.order)
    return parent_1, parent_2


def naive_tournament_select(population, tournament_size=5):
    """
    Perform a naive tournament selection: first pick tournament_size random solutions form the population.
    This selection might include duplicates. Then, pick the solution with the shortest path from the selection.
    :param population: List of solutions to pick from
    :param tournament_size: Number of solutions randomly picked
    :return: Shortest randomly picked solution
    """
    tournament = []
    for _ in range(tournament_size):
        tournament.append(random.choice(population))
    return get_shortest(tournament)


def get_shortest(population):
    best_solution = population[0]
    for solution in population:
        if solution.length < best_solution.length:
            best_solution = solution
    return best_solution


def run():
    # parameters
    population_size = 50
    generations = 100
    # persist_file = "./../tmp/productMatrixDist"

    # setup optimization
    # tsp_data = TSPData.read_from_file(persist_file)
    ga = GeneticAlgorithm(generations, population_size)

    # run optimization and write to file
    solution = ga.solve_tsp()
    # solution = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17]
    print("Found solution:", solution, compute_distance(solution))
    if len(solution) != 18:
        print("SOMETHING BADLY WRONG")
        raise Exception
    tsp_data.write_action_file(solution, "./../solutions/TSP solution.txt")


# Assignment 2.b
if __name__ == "__main__":
    # Initialize tsp_data to be widely available
    persist_file = "./../tmp/productMatrixDist"
    tsp_data = TSPData.read_from_file(persist_file)

    run()
