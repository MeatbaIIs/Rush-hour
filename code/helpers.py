import csv
from typing import Dict
from .classes.grid import Grid
import re
from typing import List, Dict
import copy
from .algorithms.breadth_first import BreadthFirst as BF
from .algorithms.beam_search import BeamSearch as BFF
from .algorithms.depth_first import DepthFirst as DF
from .algorithms.random import Random
from csv import reader


# class MethodInputError(Exception):
#     """Raised when a method input is wrong for batchrunner"""
#     """possible inputs are 'DF', 'BF', 'BFF', 'Random' and 'MaxRandom'"""
#     pass


def loader(input_file_name):
    """
    Initialize a grid with the Rush Hour puzzle given as argument
    """
    size = re.search(
        "Rushhour.+x", input_file_name).group().lstrip("Rushhour").rstrip("x")

    grid = Grid(int(size))

    # Load cars in the grid
    with open(input_file_name) as f:

        f.readline()
        car_num = 0

        while True:
            line = f.readline().strip().split(",")

            if line == [""]:
                break

            grid.add_car(line[0], line[1], int(line[2]) - 1,
                         int(line[3]) - 1, int(line[4]), car_num)

            car_num += 1

    return grid


# def dict_compare(new_dict, list_of_grids: List[Dict]) -> bool:
#     """
#     returns true if 2 dictionaries of the grid movements per car are the same
#     """
#     for dict in list_of_grids:
#         if new_dict == dict:
#             return True
#     return False


def solution_to_csv(solution, filename):
    """ Takes a solution and outputs this to a csv file """
    with open(filename, 'w') as csvfile:
        csvwriter = csv.writer(csvfile, delimiter=',')
        csvwriter.writerow(['car', 'move'])

        for step in solution:

            # Write step to csv
            csvwriter.writerow(step)


def load_solution(filename):
    """ Loads solution from csv file and returns it """
    solution = []
    # Load solution in list of lists
    with open(filename, 'r') as f:
        file_reader = csv.reader(f)
        next(file_reader)
        for line in file_reader:
            solution.append([line[0], int(line[1])])
    return solution


# def batchrunner(file: str, method: str, N_times: int):
#     """
#     Runs a certain algorithm for a certain file N times
#     It returns the total moves done, the steps for all the moves and the time it took to run per iteration
#     """
#     grid = loader(file)
#     # keep track of number of moves until solution (not number of steps!)
#     total_moves = []
#     # the exact moves done
#     total_movement_list = []
#     # time it took for solve
#     total_times = []

#     # batchrun the algorithm N times
#     for i in range(N_times):
#         # copy the greed so it remains unsolved every iteration
#         input_grid = copy.deepcopy(grid)
#         done_steps = []
#         time_taken = 0
#         # translate the method to the algorithms
#         if method == "Random":
#             algorithm = Random(input_grid)
#             done_steps, time_taken = algorithm.run("random_not_prev")
#         elif method == "MaxRandom":
#             algorithm = Random(input_grid)
#             done_steps, time_taken = algorithm.run("max_random")
#         elif method == "DF":
#             algorithm = DF(input_grid)
#             done_steps, time_taken = algorithm.run()
#         elif method == "BF":
#             algorithm = BF(input_grid)
#             done_steps, time_taken = algorithm.run()
#         elif method == "BFF":
#             algorithm = BFF(input_grid)
#             done_steps, time_taken = algorithm.run()
#         # return an error if method is incorrect
#         # if more methods are added like breath-first then depth first, make sure an elif statement is added
#         else:
#             raise MethodInputError

#         # add the info per algorithm iteration to total batchrun data
#         total_movement_list.append(done_steps)
#         total_moves.append(len(done_steps))
#         total_times.append(time_taken)

#     return total_moves, total_movement_list, total_times
