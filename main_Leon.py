"""
Takes Rush hour puzzle in the command line and solves it.
Usage: main.py [PUZZLE_NAME.CSV]
"""

import csv
#from code.algorithms.depth_first import Depth_first as dfs
#from code.algorithms.breadth_first import BreadthFirst
from code.algorithms.depth_first import Depth_first
#from code.algorithms.DFA import DepthFirst as DF
#from code.algorithms.random import Random
from code.classes.car import Car
from code.helpers import loader, solution_to_csv
from code.classes.grid_clean import Grid
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
    dfs = Depth_first(grid, best_solution = 29)
    start_time = time.perf_counter()
    solution = dfs.run()
    #print(grid.solution_list_to_steps(solution))
    #print(len(solution))
    end_time = time.perf_counter()
    print(solution)
    # print(solution)
    duration = round((end_time - start_time)/60, 2)

    print(f'Algorithm took around {duration} minutes')

    # IA = Improving_algorithm(grid, solution)
    # new_solution = IA.run()

    # print(len(new_solution))

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
    #
    # filename = input_file_name.rstrip(".csv") + "_solution.csv"
    # with open(filename, 'w') as csvfile:
    #     csvwriter = csv.writer(csvfile, delimiter=',')
    #     csvwriter.writerow(['car', 'move'])
    #
    #     for step in solution:
    #         # Write step to csv
    #         csvwriter.writerow(step)
    #
    # visual(filename, 100)

if __name__ == "__main__":
    # set-up parsing command line arguments
    parser = argparse.ArgumentParser(description="Solve a Rush hour puzzle.")

    # adding arguments
    parser.add_argument("input", help="input file (csv)")

    # read arguments from command line
    args = parser.parse_args()

    # run main with provided arguments
    main(args.input)
