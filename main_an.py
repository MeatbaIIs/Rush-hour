"""
Takes Rush hour puzzle in the command line and solves it.
Usage: main.py [PUZZLE_NAME.CSV]
"""

import csv
from code.algorithms.depth_first import DepthFirst
from code.algorithms.breadth_first import BreadthFirst
from code.algorithms.beam_search import BeamSearch
from code.algorithms.take_out_loops import TakeOutLoops
from code.algorithms.random import Random
from code.helpers import loader, solution_to_csv
from code.classes.grid import Grid
from code.algorithms.remove_useless import RemoveUseless
from code.algorithms.improving_random import ImprovingRandom
from code.algorithms.breadth_first_iter import BreadthFirstIter
import argparse
import copy
import time
import pandas as pd
import re
from code.helpers import load_solution, solution_to_csv


def main(input_file_name):
    # grid = loader(input_file_name)
    # start_time = time.perf_counter()

    # depth first
    # depth_first = dfs(grid)
    # solution = depth_first.run()

    # random
    # random_alg = Random(grid)
    # solution, time_sth = random_alg.random_algorithm()

    # breadth first
    # breadth_first = BreadthFirst(grid)
    # solution = breadth_first.run()

    # Random optimizing
    # randopt = ImprovingRandom(input_file_name)
    # solution = randopt.run()

    # Beam Search
    # beam_search = BeamSearch(grid)
    # solution = beam_search.run()

    # depth first Duncan
    # depth_first = DepthFirst('data/Rushhour6x6_1.csv')
    # solution = depth_first

    # end_time = time.perf_counter()
    # sol_len = len(solution)
    # duration = round((end_time - start_time)/60, 2)

    # print(
    #     f'Algorithm took around {duration} minutes and found solution of {sol_len} steps')

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

    # output_file_name = input_file_name.rstrip(".csv") + "_solution.csv"
    # solution_to_csv(solution, output_file_name)

    # Generate random solutions and save
    N = 10
    puzzles = [
        "data/Rushhour6x6_1.csv",
        "data/Rushhour6x6_2.csv",
        "data/Rushhour6x6_3.csv",
        "data/Rushhour9x9_4.csv",
        "data/Rushhour9x9_5.csv",
        "data/Rushhour9x9_6.csv",
        "data/Rushhour12x12_7.csv"
    ]
    algorithms = [
        "TOL",
        "RU",
        "BFI",
        "ALL"
    ]
    # results = pd.DataFrame(columns=["puzzle", "iteration", "steps", "time"])
    # for puzzle in puzzles:
    #     stable_grid = loader(puzzle)
    #     for i in range(N):
    #         print(f'Puzzle {puzzle} iteration {i}')
    #         grid = copy.deepcopy(stable_grid)
    #         start_time = time.perf_counter()

    #         IR = ImprovingRandom(input_file_name)
    #         solution = IR.run()
    #         end_time = time.perf_counter()

    #         duration = end_time - start_time

    #         steps = len(solution)
    #         iteration = i
    #         puzzle_num = puzzle
    #         results.loc[len(results)] = [puzzle_num,
    #                                      iteration, steps, duration]

    #         output_file_name = "data/random" + puzzle.rstrip(
    #             ".csv").lstrip("data") + "_IR_solution_" + str(i) + ".csv"
    #         solution_to_csv(solution, output_file_name)

    # print(results)
    # average_time = results["time"].mean()
    # print(f'average time was {average_time}')
    # average_steps = results["steps"].mean()
    # print(f'average steps was {average_steps}')

    # results.to_csv("data/random/impro_random_results.csv", index=False)

    iterative_results = pd.DataFrame(
        columns=["puzzle", "iteration", "algorithm", "steps", "time"])
    for puzzle in puzzles:

        grid = loader(puzzle)

        for i in range(N):

            input_file_name = "data/random" + \
                puzzle.rstrip(".csv").lstrip("data") + \
                "_IR_solution_" + str(i) + ".csv"
            solution = load_solution(input_file_name)

            print(f'Optimizing a solution of {len(solution)} steps.')

            for algorithm in algorithms:

                start_time = time.perf_counter()
                if algorithm == "TOL":
                    print('Taking out loops.')
                    TOL = TakeOutLoops(grid, solution)
                    new_solution = TOL.run()
                elif algorithm == "RU":
                    print('Seeing if any useless steps can be left out.')
                    RU = RemoveUseless(grid, solution)
                    new_solution = RU.run()
                elif algorithm == "BFI":
                    print('Iterating with Breadth First')
                    BFI = BreadthFirstIter(grid, solution)
                    new_solution = BFI.run()
                elif algorithm == "ALL":
                    print('Taking out loops.')
                    TOL = TakeOutLoops(grid, solution)
                    new_solution = TOL.run()
                    print('Seeing if any useless steps can be left out.')
                    RU = RemoveUseless(grid, new_solution)
                    new_solution = RU.run()
                    print('Iterating with Breadth First')
                    BFI = BreadthFirstIter(grid, new_solution)
                    new_solution = BFI.run()

                duration = time.perf_counter() - start_time

                print(f'The solution is {len(new_solution)} steps.')
                filename = input_file_name.rstrip(".csv") + "_optimized.csv"
                solution_to_csv(new_solution, filename)
                print(filename)

                steps = len(new_solution)
                iteration = i
                puzzle_num = puzzle
                iterative_results.loc[len(iterative_results)] = [puzzle_num,
                                                                 iteration, algorithm, steps, duration]

    iterative_results.to_csv("data/random/iterative_results.csv", index=False)


if __name__ == "__main__":
    # set-up parsing command line arguments
    parser = argparse.ArgumentParser(description="Solve a Rush hour puzzle.")

    # adding arguments
    parser.add_argument("input", help="input file (csv)")

    # read arguments from command line
    args = parser.parse_args()

    # run main with provided arguments
    main(args.input)
