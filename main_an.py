"""
Takes Rush hour puzzle in the command line and solves it.
Usage: main.py [PUZZLE_NAME.CSV]
"""

import csv
from code.algorithms.depth_first import Depth_first as dfs
from code.algorithms.breadth_first import BreadthFirst
from code.algorithms.DFA import DepthFirst
from code.algorithms.take_out_loops import TakeOutLoops
from code.algorithms.random import Random
from code.helpers import loader, solution_to_csv
from code.classes.grid import Grid
from code.algorithms.improving_algorithm import Improving_algorithm
import argparse
import copy
import time


def main(input_file_name):
    grid = loader(input_file_name)
    start_time = time.perf_counter()

    # depth first
    # depth_first = dfs(grid)
    # solution = depth_first.run()

    # random
    # random_alg = Random(grid)
    # solution = random_alg.random_algorithm()

    # breadth first
    breadth_first = BreadthFirst(grid)
    solution = breadth_first.run()

    # depth first Duncan
    # depth_first = DepthFirst('data/Rushhour6x6_1.csv')
    # solution = depth_first

    end_time = time.perf_counter()
    # print(solution)
    sol_len = len(solution)
    duration = round((end_time - start_time)/60, 2)

    print(
        f'Algorithm took around {duration} minutes and found solution of {sol_len} steps')

    # IA = Improving_algorithm(grid, solution)
    # new_solution = IA.run()
    # print(
    #     f'Improving algorithm lead to a solution of {len(new_solution)} steps.')

    # Take out loops
    # tol = TakeOutLoops(grid, solution)
    # new_solution = tol.run()
    # print(f'solution length after take out loops: {len(new_solution)}')

    # histogram(input_file_name)
    # dfs.run(grid)
    # print('found a solution!')
    #algorithm = Random(grid)
    # print(algorithm.other_random_algorithm())
    # dfs.run(grid)
    # print('found a solution!')
    # algorithm = dfs(grid)
    # algorithm.run()

    # algorithm = DF("data/Rushhour6x6_1.csv")
    # algorithm.run()

    solution_to_csv(solution, input_file_name)


if __name__ == "__main__":
    # set-up parsing command line arguments
    parser = argparse.ArgumentParser(description="Solve a Rush hour puzzle.")

    # adding arguments
    parser.add_argument("input", help="input file (csv)")

    # read arguments from command line
    args = parser.parse_args()

    # run main with provided arguments
    main(args.input)
