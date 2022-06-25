"""
Takes Rush hour puzzle in the command line and solves it.
Usage: main.py [PUZZLE_NAME.CSV]
"""

import csv
#from code.algorithms.depth_first import Depth_first as dfs
#from code.algorithms.breadth_first import BreadthFirst
from code.algorithms.depth_first import DepthFirst
#from code.algorithms.DFA import DepthFirst as DF
#from code.algorithms.random import Random
from code.classes.car import Car
from code.helpers import loader, solution_to_csv, load_solution
from code.classes.grid import Grid
#from code.algorithms.improving_algorithm import Improving_algorithm
from code.visualization.visualization import main as visual
import argparse
import copy
import time


def main(input_file_name):
    grid = loader(input_file_name)

    # depth first
    # depth_first = dfs(grid)
    # solution = depth_first.run()

    # random
    # random_alg = Random(grid)
    # solution = random_alg.random_algorithm()

    # breadth first
    #breadth_first = BreadthFirst(grid)
    grid.print_grid()
    #solution = load_solution("data/Rushhour12x12_7_randopt_solution_optimized.csv")
    solution = load_solution("data/Rushhour6x6_1_solution.csv")
    dfs = DepthFirst(grid, best_solution = 29, solutions = [solution])
    start_time = time.perf_counter()
    solution = dfs.run()
    #print(grid.solution_list_to_steps(solution))
    #print(len(solution))
    end_time = time.perf_counter()
    print(solution)
    # print(solution)
    duration = round((end_time - start_time)/60, 2)

    print(f'Algorithm took around {duration} minutes')

if __name__ == "__main__":
    # set-up parsing command line arguments
    parser = argparse.ArgumentParser(description="Solve a Rush hour puzzle.")

    # adding arguments
    parser.add_argument("input", help="input file (csv)")

    # read arguments from command line
    args = parser.parse_args()

    # run main with provided arguments
    main(args.input)
