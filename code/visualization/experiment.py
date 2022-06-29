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
import matplotlib.pyplot as plt


def main(input_file_name, method):
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
        "ALL"
    ]

    if method == "generate_solutions":

        # generates 10 solutions with improving random set to time = 60 seconds
        # Generate random solutions and save
    
        results = pd.DataFrame(columns=["puzzle", "iteration", "steps", "time"])
        for puzzle in puzzles:
            stable_grid = loader(puzzle)
            for i in range(N):
                print(f'Puzzle {puzzle} iteration {i}')
                grid = copy.deepcopy(stable_grid)
                start_time = time.perf_counter()

                IR = ImprovingRandom(grid)
                solution = IR.run_improving("time", 60)
                end_time = time.perf_counter()

                duration = end_time - start_time

                steps = len(solution)
                iteration = i
                puzzle_num = puzzle
                results.loc[len(results)] = [puzzle_num,
                                             iteration, steps, duration]

                output_file_name = "data/random" + puzzle.rstrip(
                    ".csv").lstrip("data") + "_IR_solution_" + str(i) + ".csv"
                solution_to_csv(solution, output_file_name)

        print(results)
        average_time = results["time"].mean()
        print(f'average time was {average_time}')
        average_steps = results["steps"].mean()
        print(f'average steps was {average_steps}')

        # Optimize the previously generated solutions with TakeOutLoops, RemoveUseless, and both each for 3 iterations
        results.to_csv("data/random/impro_random_results.csv", index=False)

    elif method == "optimize":


        iterative_results = pd.DataFrame(
            columns=["puzzle", "solution", "iteration", "algorithm", "steps", "time"])
        for puzzle in puzzles:

            grid = loader(puzzle)

            for i in range(N):

                input_file_name = "data/random" + \
                    puzzle.rstrip(".csv").lstrip("data") + \
                    "_IR_solution_" + str(i) + ".csv"
                solution = load_solution(input_file_name)

                for j in range(3):

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

                        elif algorithm == "ALL":
                            print('Taking out loops.')
                            TOL = TakeOutLoops(grid, solution)
                            new_solution = TOL.run()
                            print('Seeing if any useless steps can be left out.')
                            RU = RemoveUseless(grid, new_solution)
                            new_solution = RU.run()

                        duration = time.perf_counter() - start_time

                        print(f'The solution is {len(new_solution)} steps.')
                        filename = input_file_name.rstrip(
                            ".csv") + "_optimized.csv"
                        solution_to_csv(new_solution, filename)
                        print(filename)

                        steps = len(new_solution)
                        iteration = i
                        puzzle_num = puzzle
                        iterative_results.loc[len(iterative_results)] = [puzzle_num, j,
                                                                         iteration, algorithm, steps, duration]

        iterative_results.to_csv("data/random/iterative_results.csv", index=False)


    elif method == "plot_improvingrandom":
        # Plot the length of the solutions generated with ImprovingRandom
        results = pd.read_csv("data/random/impro_random_results.csv")
        means = results.groupby("puzzle").mean()
        xs = pd.Series([7, 1, 2, 3, 4, 5, 6])
        puzzles = means.index
        steps = means["steps"]
        fig, ax = plt.subplots()

        ax.bar(xs, steps)
        ax.set_xticklabels([0, 1, 2, 3, 4, 5, 6, 7])

        ax.set_xlabel('Puzzle number', labelpad=15)
        ax.set_ylabel('Steps', labelpad=15)
        ax.set_title(
            'Solution length after running Improving Random for 1 minute', pad=15)
        plt.show()

    elif method == "plot_iteration_steps":

        # Plot the length of the solutions after optimization

        solution_results = pd.read_csv("data/random/iterative_results.csv")
        # print(solution_results)

        means = solution_results.groupby("puzzle").mean()
        print(means)
        puzzles = means.index
        fig, ax = plt.subplots()

        xs = pd.Series([7, 1, 2, 3, 4, 5, 6])

        filtered = solution_results[solution_results.algorithm == "TOL"]
        tol = filtered.groupby("puzzle").mean()
        tol_sd = filtered.groupby("puzzle").std()
        tol_steps_sd = tol_sd['steps']
        tol_steps = tol['steps']

        filtered = solution_results[solution_results.algorithm == "RU"]
        ru = filtered.groupby("puzzle").mean()
        ru_sd = filtered.groupby("puzzle").std()
        ru_steps_sd = ru_sd['steps']
        ru_steps = ru['steps']

        filtered = solution_results[solution_results.algorithm == "ALL"]
        al = filtered.groupby("puzzle").mean()
        all_sd = filtered.groupby("puzzle").std()
        all_steps_sd = all_sd['steps']
        all_steps = al['steps']

        bar_width = 0.2

        ax.bar(xs - bar_width, tol_steps, width=bar_width)
        ax.bar(xs, ru_steps, width=bar_width)
        ax.bar(xs + bar_width, all_steps, width=bar_width)
        ax.errorbar(xs - bar_width, tol_steps,
                    yerr=tol_steps_sd, fmt="o", color='black')
        ax.errorbar(xs, ru_steps,
                    yerr=ru_steps_sd, fmt="o", color='black')
        ax.errorbar(xs + bar_width, all_steps,
                    yerr=all_steps_sd, fmt="o", color='black')
        ax.set_xticklabels([0, 1, 2, 3, 4, 5, 6, 7])

        ax.set_xlabel('Puzzle number', labelpad=15)
        ax.set_ylabel('Steps', labelpad=15)
        ax.legend(['TakeOutLoops', 'RemoveUseless', 'Both'])
        ax.set_title(
            'Solution length after optimizing with different algorithms', pad=15)

        plt.show()

    elif method == "plot_iteration_time":

        # Plot the duration of the optimization
        solution_results = pd.read_csv("data/random/iterative_results.csv")

        means = solution_results.groupby("puzzle").mean()
        print(means)
        puzzles = means.index
        fig, ax = plt.subplots()

        xs = pd.Series([7, 1, 2, 3, 4, 5, 6])

        filtered = solution_results[solution_results.algorithm == "TOL"]
        tol = filtered.groupby("puzzle").mean()
        tol_sd = filtered.groupby("puzzle").std()
        tol_time = tol['time']
        tol_time_sd = tol_sd['time']

        filtered = solution_results[solution_results.algorithm == "RU"]
        ru = filtered.groupby("puzzle").mean()
        ru_sd = filtered.groupby("puzzle").std()
        ru_time = ru['time']
        ru_time_sd = ru_sd['time']

        filtered = solution_results[solution_results.algorithm == "ALL"]
        al = filtered.groupby("puzzle").mean()
        all_sd = filtered.groupby("puzzle").std()
        all_time_sd = all_sd['time']
        all_time = al['time']

        bar_width = 0.2

        ax.bar(xs - bar_width, tol_time, width=bar_width)
        ax.bar(xs, ru_time, width=bar_width)
        ax.bar(xs + bar_width, all_time, width=bar_width)
        ax.errorbar(xs - bar_width, tol_time,
                    yerr=tol_time_sd, fmt="o", color='black')
        ax.errorbar(xs, ru_time,
                    yerr=ru_time_sd, fmt="o", color='black')
        ax.errorbar(xs + bar_width, all_time,
                    yerr=all_time_sd, fmt="o", color='black')
        ax.set_xticklabels([0, 1, 2, 3, 4, 5, 6, 7])

        ax.set_xlabel('Puzzle number', labelpad=15)
        ax.set_ylabel('Time', labelpad=15)
        ax.legend(['TakeOutLoops', 'RemoveUseless', 'Both'])
        ax.set_title(
            'Optimization duration with different algorithms', pad=15)

        plt.show()


if __name__ == "__main__":
    # set-up parsing command line arguments
    parser = argparse.ArgumentParser(description="Solve a Rush hour puzzle.")

    # adding arguments
    parser.add_argument("input", help="input file (csv)")

    # read arguments from command line
    args = parser.parse_args()

    # run main with provided arguments
    main(args.input)
