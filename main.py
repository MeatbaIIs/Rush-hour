"""
Authors: Anneloes van Schaik and Leon Schuijtvlot
Student numbers: 10981268 and 14291584

This program lets the user go through a short menu to use the algorithms made in this project
"""

import csv
from code.algorithms.beam_search import BeamSearch as BS
from code.algorithms.breadth_first import BreadthFirst as BF
from code.algorithms.breadth_first_iter import BreadthFirstIter as BFI
from code.algorithms.depth_first import DepthFirst as DF
from code.algorithms.improving_random import ImprovingRandom as IR
from code.algorithms.remove_useless import RemoveUseless as RU
from code.algorithms.random import Random
from code.algorithms.take_out_loops import TakeOutLoops as TOL
from code.helpers import loader, solution_to_csv, check_filename, ask_for_solution, load_solution
from code.visualization.visualization import main as visual

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
BreadthFirstIterating (BFI) \n \
RemoveUseless (RU) \n \
TakeOutLoops (TOL) ")

        # asks to choose an algorithm and what problem to use it on
        algorithm = input("What algorithm would you like to use? ").upper()

        # gives option to quit
        if algorithm == "QUIT" or algorithm == 'Q':
            break

        input_filename = input("What problem would you like to use it on? ")

        if input_filename.upper() == "QUIT" or input_filename.upper() == 'Q':
            break

        puzzle_numbers = range(1, 7).append(10)
        number = int(input_filename)

        # allow user to only input the puzzle number
        if number in puzzle_numbers:
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

        if algorithm == "BREADTHFIRST" or algorithm =="BF":
            bf = BF(grid)
            solution = bf.run()
            print(solution)

        elif algorithm == "BEAMSEARCH" or algorithm == "BS":
            bs = BS(grid)
            solution = bs.run()
            print(solution)

        elif algorithm == "DEPTHFIRST" or algorithm == 'DF':
            answer = input("Would you like to give a solution to quicken the process? (yes/no) ").upper()
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

                old_solution = load_solution(filename)
                df = DF(grid, best_solution = len(old_solution) -1, solution = old_solution)
                solution = df.run(method)
                print(solution)

            else:

                DepthFirst = DF(grid)
                solution = DepthFirst.run(method)
                print(solution)

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

            Rand = Random(grid)
            solution, time_taken = Rand.run(method)
            print(solution)

        elif algorithm == "IMPROVINGRANDOM" or algorithm == "IR":
            method = ""
            while method != 'time' and method != "iterations":
                print("Methods: \n \
time (t)\n \
iterations (i)")
                method = input("Would you like to stop on time or iterations? ").lower()

                if method == 'i':
                    method = "iterations"

                elif method == 't':
                    method = "time"

                else:
                    print("\nPick a correct method\n")
                    time.sleep(1)

            amount = input("How many iterations or how long would you like to run the algorithm? ").lower()
            ir = IR(grid)
            solution = ir.run(method, amount)
            print(solution)

        elif algorithm == "BREADTHFIRSTITERATING" or algorithm == "BFI":
            filename = ask_for_solution()

            if filename[5:] not in files:
                print("\nNo such file\n")
                time.sleep(1)
                continue

            old_solution = load_solution(filename)

            bfi = BFI(grid, old_solution)
            solution = bfi.run()

        elif algorithm == "REMOVEUSELESS" or algorithm == "RU":
            filename = ask_for_solution()

            if filename[5:] not in files:
                print("\nNo such file\n")
                time.sleep(1)
                continue

            old_solution = load_solution(filename)

            ru = RU(grid, old_solution)
            solution = ru.run()
            print(solution)

        elif algorithm == "TAKEOUTLOOPS" or algorithm == "TOL":
            filename = ask_for_solution()

            if filename[5:] not in files:
                print("\nNo such file\n")
                time.sleep(1)
                continue

            old_solution = load_solution(filename)
            tol = TOL(grid, old_solution)
            solution = tol.run()
            print(solution)

        # message if algorithm is not in list
        else:
            print("\nNo such algorithm\n")
            time.sleep(1)
            continue

        save_file = input("Would you like to save the file? (yes/no)").upper()

        # lets the user save the solution
        while save_file == "YES" or save_file == 'Y':
            save_filename = input("What name would you choose for your save file? ")
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
                    save_file = input("Want to pick a new name? (yes/no)").upper()

            # if no such file exists it saves the solution
            else:
                solution_to_csv(solution, save_filename)
                break

        # if the solution is saved there is an option to create a corresponding visual
        if save_file == "YES" or save_file == 'Y':
            answer = input("Do you want a visual of the solution? (yes/no)").upper()
            if answer == "YES" or answer == "Y":
                visual(save_filename, len(solution) + 1, input_filename)


if __name__ == "__main__":
    main()
