# from Assignment_3.src.Coordinate import Coordinate
# from Assignment_3.src.Direction import Direction as D
#
# start = Coordinate(0, 0)
# route = [D.east, D.east, D.south, D.west, D.north, D.east, D.east]
# # route = [D.east, D.east, D.south, D.west, D.north,D.north]
# # route = [D.east, D.south, D.west, D.north, D.north]
#
#
# def print_route(r):
#     c = start
#     print(c)
#     for d in r:
#         c = c.add_direction(d)
#         print(c)
#
#
# # ATTEMPT 1
#
# new_route = []
# cell = start
# index = 0
# # Visited maps the cell to the index in the route list
# visited = {cell: index}
#
# for direction in route:
#     cell = cell.add_direction(direction)
#     if cell in visited:
#         # Invalidate all cells previously visited
#         index = visited[cell]
#         del new_route[index:]
#         visited = {k: v for k, v in visited.items() if v <= index}
#
#         for k in visited:
#             print(k, visited[k])
#     else:
#         new_route.append(direction)
#
#         index = index + 1
#         visited[cell] = index
#
# print("OLD")
# print_route(route)
# print("NEW")
# print_route(new_route)
# print(new_route)
# for k in visited:
#     print(k, visited[k])
#
# # ATTEMPT 2
# # cell = start
# # cells = [start]
# # for direction in route:
# #     cell = cell.add_direction(direction)
# #     cells.append(start)
# from Assignment_3.src.GeneticAlgorithm import TSPSolution
#
#
# def crossover_index(solution_1, solution_2, begin_index, end_index):
#     new_order = [-1] * len(solution_1.order)
#     taken_numbers = {}
#     for index in range(begin_index, end_index):
#         new_order[index] = solution_1.order[index]
#         taken_numbers[solution_1.order[index]] = True
#
#     # Add unvisited numbers in order of solution 1
#     index = 0
#     for number in solution_2.order:
#         if index == begin_index:
#             index = end_index
#         if number in taken_numbers:
#             continue
#
#         new_order[index] = number
#         index += 1
#
#     return TSPSolution(new_order)
#
#
# s1 = TSPSolution([1, 2, 3, 4, 5, 6, 7, 8, 9, 10])
# s2= TSPSolution([10, 9, 8, 7, 6, 5, 4, 3, 2, 1])
#
# new_1 = crossover_index(s1, s2, 4, 7)
# print("done")
# print(s1.order)
# print(new_1.order)
# print(s2.order)
import random

for _ in range(10):
    print(random.random())
