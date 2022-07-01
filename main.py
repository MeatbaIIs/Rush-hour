"""
Authors: Anneloes van Schaik and Leon Schuijtvlot
Student numbers: 10981268 and 14291584

This program lets the user go through a short menu to use the algorithms made in this project
"""

import csv
from code.algorithms.beam_search import BeamSearch as BS
from code.algorithms.breadth_first import BreadthFirst as BF
from code.algorithms.depth_first import DepthFirst as DF
from code.algorithms.improving_random import ImprovingRandom as IR
from code.algorithms.remove_useless import RemoveUseless as RU
from code.algorithms.random import Random
from code.algorithms.take_out_loops import TakeOutLoops as TOL
from code.helpers import loader, solution_to_csv, check_filename, ask_for_solution, load_solution
from code.visualization.visualization import main as visual
from code.visualization.generate_runtimes import generate_runtimes as GR
from code.visualization.experiment import main as experiment
import os
import time


def main():
    while True:
        print("Algorithm names:\n \
BeamSearch (BS) \n \
BreadthFirst (BF) \n \
DepthFirst (DF) \n \
Random (R) \n \
ImprovingRandom (IR) \n \
RemoveUseless (RU) \n \
TakeOutLoops (TOL) \n \n\
Experiments: \n \
Generate_Runtimes (GR) \n \
Experiment (E)")

        # asks to choose an algorithm and what problem to use it on
        algorithm = input("What algorithm would you like to use? ").upper()

        # gives option to quit
        if algorithm == "QUIT" or algorithm == 'Q':
            break

        input_filename = input("What problem would you like to use it on? ")

        if input_filename.upper() == "QUIT" or input_filename.upper() == 'Q':
            break

        puzzle_numbers = range(1, 8)
        if input_filename.isnumeric():
            number = int(input_filename)

            # allow user to only input the puzzle number
            if number in puzzle_numbers or number == 10:
                if number <= 3 or number == 10:
                    input_filename = "Rushhour6x6_" + str(number)
                elif number <= 6:
                    input_filename = "Rushhour9x9_" + str(number)
                elif number == 7:
                    input_filename = "Rushhour12x12_" + str(number)

        # check if the filename points to the right folder and has the .csv extension, and adds them if not
        input_filename = check_filename(input_filename)

        # get the list of all the files in the data folder
        files = os.listdir("data")

        # check if the file exists
        if input_filename[5:] not in files:
            print("\n No such file \n")
            time.sleep(1)
            continue

        # load corresponding grid
        grid = loader(input_filename)

        start_time = time.perf_counter()

        if algorithm == "BREADTHFIRST" or algorithm == "BF":
            bf = BF(grid)
            solution = bf.run()

        elif algorithm == "BEAMSEARCH" or algorithm == "BS":
            bs = BS(grid)
            solution = bs.run()

        elif algorithm == "DEPTHFIRST" or algorithm == 'DF':
            answer = input(
                "Would you like to give a solution to quicken the process? (yes/no) ").upper()
            method = ""
            while method != "furthest" and method != "optimal":
                print("Methods:\n \
furthest (f) \n \
optimal (o) \n ")
                method = input("What method would you like to use? ").lower()

                if method == 'f':
                    method = "furthest"

                elif method == "o":
                    method = "optimal"

            if answer == "YES" or answer == 'Y':
                filename = ask_for_solution()

                # if the file does not exist print message and return to start
                if filename[5:] not in files:
                    print("\nNo such file\n")
                    time.sleep(1)
                    continue

                start_time = time.perf_counter()
                old_solution = load_solution(filename)
                df = DF(grid, best_solution = len(old_solution) - 1, solution = old_solution)
                solution = df.run(method)

            else:
                start_time = time.perf_counter()
                DepthFirst = DF(grid)
                solution = DepthFirst.run(method)

        elif algorithm == "RANDOM" or algorithm == 'R':
            method = ""
            while method != "random" and method != "max_random" and method != "random_not_prev":
                print("Methods: \n \
random (r)\n \
max_random (mr)\n \
random_not_prev (rnp)")

                method = input("Choose your method: ").lower()

                if method == 'r':
                    method = "random"
                elif method == "mr":
                    method = "max_random"
                elif method == "rnp":
                    method = "random_not_prev"

                if method != "random" and method != "max_random" and method != "random_not_prev":
                    print("\nPick a correct method\n")
                    time.sleep(1)

            start_time = time.perf_counter()
            Rand = Random(grid)
            solution, time_taken = Rand.run(method)

        elif algorithm == "IMPROVINGRANDOM" or algorithm == "IR":
            method = ""
            random_method = ""
            while (method != 'time' and method != "iterations") or \
                    (random_method != "random" and random_method != "max_random" and random_method != "random_not_prev"):
                print("Methods: \n \
time (t)\n \
iterations (i)")
                method = input(
                    "Would you like to stop on time or iterations? ").lower()

                if method == 'i':
                    method = "iterations"

                elif method == 't':
                    method = "time"

                else:
                    print("\nPick a correct method\n")
                    time.sleep(1)

                print("Methods: \n \
random (r)\n \
max_random (mr)\n \
random_not_prev (rnp)")

                random_method = input(
                    "Choose your method for random: ").lower()

                if random_method == 'r':
                    random_method = "random"

                elif random_method == "mr":
                    random_method = "max_random"

                elif random_method == "rnp":
                    random_method = "random_not_prev"

            amount = input(
                "How many iterations or how long would you like to run the algorithm? ").lower()
            start_time = time.perf_counter()
            ir = IR(grid)
            solution = ir.run_improving(method, amount, random_method=random_method)

        elif algorithm == "REMOVEUSELESS" or algorithm == "RU":
            filename = ask_for_solution()

            if filename[5:] not in files:
                print("\nNo such file\n")
                time.sleep(1)
                continue

            start_time = time.perf_counter()
            old_solution = load_solution(filename)
            ru = RU(grid, old_solution)
            solution = ru.run()

        elif algorithm == "TAKEOUTLOOPS" or algorithm == "TOL":
            filename = ask_for_solution()

            if filename[5:] not in files:
                print("\nNo such file\n")
                time.sleep(1)
                continue

            start_time = time.perf_counter()
            old_solution = load_solution(filename)
            tol = TOL(grid, old_solution)
            solution = tol.run()

        elif algorithm == "GENERATERUNTIMES" or algorithm == "GR":
            output_filename = input(
                "What name would you like to give your graph? ")
            if not (".png" in output_filename or ".jpg" in output_filename):
                output_filename = output_filename + ".png"

            if not "data/" in output_filename:
                output_filename = "data/" + output_filename

            GR(input_filename, output_filename)

            # no files to save as for algorithm
            continue

        elif algorithm == "EXPERIMENT" or algorithm == "E":
            method = ""
            while method != "generate_solutions" and method != "optimize" and method != "plot_improvingrandom" and \
                    method != "plot_iteration_steps" and method != "plot_iteration_time":
                print("Methods: \n \
generate_solution (gs) \n \
optimize (o) \n \
plot_improvingrandom (pi) \n \
plot_iteration_steps (pis) \n \
plot_iteration_time (pit)")

                method = input("What method would you like to use? ").lower()

                if method == "gs":
                    method = "generate_solutions"

                elif method == "o":
                    method = "optimize"

                elif method == "pi":
                    method = "plot_improvingrandom"

                elif method == "pis":
                    method = "plot_iteration_steps"

                elif method == "pit":
                    method = "plot_iteration_time"

                if method != "generate_solutions" and method != "optimize" and method != "plot_improvingrandom" and \
                        method != "plot_iteration_steps" and method != "plot_iteration_time":
                    print("\nPick a valid method\n")

                experiment(input_filename, method)
                continue

        # message if algorithm is not in list
        else:
            print("\nNo such algorithm\n")
            time.sleep(1)
            continue

        print(f"Best solution found was of {len(solution)} steps")

        if len(solution) < 100:
            print(solution)

        time_ran = time.perf_counter() - start_time

        print(f"Algorithm ran for {round(time_ran / 60, 2)} minutes")

        save_file = input("Would you like to save the file? (yes/no)").upper()

        # lets the user save the solution
        while save_file == "YES" or save_file == 'Y':
            save_filename = input(
                "What name would you choose for your save file? ")
            save_filename = check_filename(save_filename)

            # checks if file already exists
            if save_filename[5:] in files:
                answer = input("File already exists, are you sure? ").upper()

                # overwrites file
                if answer == "YES" or answer == "Y":
                    solution_to_csv(solution, save_filename)
                    break

                # asks whether user still wants to save the file
                else:
                    save_file = input(
                        "Want to pick a new name? (yes/no)").upper()

            # if no such file exists it saves the solution
            else:
                solution_to_csv(solution, save_filename)
                break

        # if the solution is saved there is an option to create a corresponding visual
        if save_file == "YES" or save_file == 'Y':
            answer = input(
                "Do you want a visual of the solution? (yes/no)").upper()
            if answer == "YES" or answer == "Y":
                visual(save_filename, len(solution) + 1, input_filename)


if __name__ == "__main__":
    main()
