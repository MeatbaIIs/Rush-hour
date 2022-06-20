"""
Initialize a grid with the Rush Hour puzzle given as command line argument, solve the puzzle, and visualize the solution.
Usage: loader.py [PUZZLE_NAME.CSV]
"""

import csv
from typing import Dict
from .classes.grid_clean import Grid
import re
from typing import List, Dict
import copy
from .algorithms.breadth_first_an import BreadthFirst as BF
from .algorithms.breadth_first_furthest import BreadthFirst as BFF
from .algorithms.depth_first import Depth_first as DF
from .algorithms.random import Random 


def loader(input_file_name):
    # Get grid size from the input file name
    size = re.search(
        "Rushhour.+x", input_file_name).group().lstrip("Rushhour").rstrip("x")

    # Load grid
    grid = Grid(int(size))

    # Load cars in the grid
    with open(input_file_name) as f:

        # Skip over first line
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

# function that returns true if 2 dictionaries of the grid movements per car are the same


def dict_compare(new_dict, list_of_grids: List[Dict]) -> bool:
    for dict in list_of_grids:
        if new_dict == dict:
            return True
    return False


def solution_to_csv(solution, input_file_name):
    """ takes a solution formatted as a list of steps and outputs this to a csv file """
    filename = input_file_name.rstrip(".csv") + "_solution.csv"
    with open(filename, 'w') as csvfile:
        csvwriter = csv.writer(csvfile, delimiter=',')
        csvwriter.writerow(['car', 'move'])

        for step in solution:
            # Write step to csv
            csvwriter.writerow(step)

"""
Runs a certain algorithm for a certain file N times
It returns the total moves done, the steps for all the moves and the time it took to run per iteration
"""
def batchrunner(file: str, method: str, N_times: int):
    grid = loader(file)
    total_steps = []
    total_movement_list = []
    total_times = []
    for i in range(N_times):
        input_grid = copy.deepcopy(grid)
        if method == "Random":
            algorithm = Random(input_grid)
            done_steps, time_taken = algorithm.run("random_not_prev")
        elif method == "MaxRandom":
            algorithm = Random(input_grid)
            done_steps, time_taken = algorithm.run("max_random")
        elif method == "DF":
            algorithm = DF(input_grid)
            done_steps, time_taken = algorithm.run()
        elif method == "BF":
            algorithm = BF(input_grid)
            done_steps, time_taken = algorithm.run()
        elif method == "BFF":
            algorithm = BFF(input_grid)
            done_steps, time_taken = algorithm.run()
            

        total_movement_list.append(done_steps)
        total_steps.append(len(done_steps))
        total_times.append(time_taken)  

    return total_steps, total_movement_list, total_times  

    

