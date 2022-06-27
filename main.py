"""
Takes Rush hour puzzle in the command line and solves it.
Usage: main.py [PUZZLE_NAME.CSV]
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

import argparse
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
        algorithm = input("What algorithm would you like to use? ").upper()

        if algorithm == "QUIT" or algorithm == 'Q':
            break

        input_filename = input("What problem would you like to use it on? ")

        if input_filename.upper() == "QUIT" or input_filename.upper() == 'Q':
            break

        input_filename = check_filename(input_filename)
        files = os.listdir("data")
        if input_filename[5:] not in files:
            print("\n No such file \n")
            time.sleep(1)
            continue

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

            if answer == "YES" or answer == 'Y':
                filename = ask_for_solution()
                if filename[5:] not in files:
                    print("\nNo such file\n")
                    time.sleep(1)
                    continue

                old_solution = load_solution(filename)
                df = DF(grid, best_solution = len(old_solution) -1, solutions = [old_solution])
                solution = df.run()
                print(solution)

            else:
                DepthFirst = DF(grid)
                solution = DepthFirst.run()
                print(solution)

        elif algorithm == "RANDOM" or algorithm == 'R':
            print("Methods: \n \
random \n \
max_random \n \
random_not_prev")

            method = input("Choose your method: ").lower()
            Rand = Random(grid)
            solution, time_taken = Rand.run(method)
            print(solution)

        elif algorithm == "IMPROVINGRANDOM" or algorithm == "IR":
            tol = TOL(input_filename)
            solution = tol.run()
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

        else:
            print("\nNo such algorithm\n")
            time.sleep(1)
            continue

        save_file = input("Would you like to save the file? (yes/no)").upper()

        while save_file == "YES" or save_file == 'Y':
            save_filename = input("What name would you choose for your save file? ")
            save_filename = check_filename(save_filename)
            if save_filename[5:] in files:
                answer = input("File already exists, are you sure? ").upper()
                if answer == "YES" or answer == "Y":
                    solution_to_csv(solution, save_filename)
                    break
                else:
                    save_file = input("Want to pick a new name? (yes/no)").upper()

            else:
                solution_to_csv(solution, save_filename)
                break

        if save_file == "YES" or save_file == 'Y':
            answer = input("Do you want a visual of the solution? (yes/no)").upper()
            if answer == "YES" or answer == "Y":
                visual(save_filename, len(solution), input_filename)

if __name__ == "__main__":
    main()
