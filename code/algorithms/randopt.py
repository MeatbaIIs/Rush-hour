"""
Algorithm that solves a given Rush hour puzzle by taking random steps. The best solution is written to a csv file while running.
"""

from cmath import inf
import copy
import queue
import random
import numpy as np
from ..helpers import loader
import keyboard
import csv
import time


class RandOpt():
    def __init__(self, input_file_name):
        print("Running Random Optimized algorithm")
        self._start_grid = loader(input_file_name)
        self._solution = []
        self._grid = copy.deepcopy(self._start_grid)
        self._running = True
        # keyboard.add_hotkey("enter", self.stop_running)
        self._solution_filename = input_file_name.rstrip(
            ".csv") + "_randopt_solution.csv"

    def begin_new_solution(self):
        self._solution = []
        self._grid = copy.deepcopy(self._start_grid)

    def stop_running(self):
        self._running = False

    def random_step(self):
        """ Checks whether the given state is a solution """
        distance = 0
        moves = []

        while not moves:
            car = random.choice(list(self._grid._cars.keys()))
            moves = self._grid.possible_moves(car)

        distance = random.choice(moves)
        self._grid.move(car, distance)

        return [car, distance]

    def run(self):
        """ Runs a looping random algorithm """

        best_solution = []
        best_solution_len = inf
        start_time = time.perf_counter()

        while self._running:
            self._solution = []
            counter = 0
            self.begin_new_solution()

            while not self._grid.win() and counter < best_solution_len:
                self._solution.append(self.random_step())
                counter += 1

            if best_solution_len > len(self._solution):
                best_solution = copy.deepcopy(self._solution)
                best_solution_len = len(best_solution)
                end_time = time.perf_counter()
                duration = round((end_time-start_time)/60, 2)
                print(
                    f'found a solution of {len(self._solution)} steps after around {duration} minutes')

                with open(self._solution_filename, 'w') as csvfile:
                    csvwriter = csv.writer(csvfile, delimiter=',')
                    csvwriter.writerow(['car', 'move'])

                    for step in best_solution:
                        csvwriter.writerow(step)

                # start time for next round
                start_time = time.perf_counter()

        return best_solution
