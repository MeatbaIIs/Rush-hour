"""
Takes Rush hour puzzle in the command line and solves it.
Usage: main.py [PUZZLE_NAME.CSV]
"""

import csv
from code.algorithms.depth_first import Depth_first as dfs
from code.classes.car import Car
from code.helpers import loader, save_solution
from code.classes.grid import Grid
from code.algorithms.random import Random
from code.visualization.histogram import histogram
from code.algorithms.improving_algorithm import Improving_algorithm
import argparse
import copy


def main(input_file_name):
    grid = loader(input_file_name)
    gridcopy = copy.deepcopy(grid)
    depth_first = dfs(grid)
    solution = depth_first.run()

    IA = Improving_algorithm(gridcopy, solution)
    new_solution = IA.run()
    print(new_solution)
    print(len(new_solution))

    # histogram(input_file_name)
    # dfs.run(grid)
    # print('found a solution!')
    #algorithm = Random(grid)
    # print(algorithm.other_random_algorithm())


if __name__ == "__main__":
    # set-up parsing command line arguments
    parser = argparse.ArgumentParser(description="Solve a Rush hour puzzle.")

    # adding arguments
    parser.add_argument("input", help="input file (csv)")

    # read arguments from command line
    args = parser.parse_args()

    # run main with provided arguments
    main(args.input)
