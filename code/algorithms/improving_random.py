"""
Algorithm that solves a puzzle by continually search for a better random solution
"""
import copy
import random
from ..helpers import MethodInputError
import time
from code.algorithms.random import Random


class ImprovingRandom(Random):
    def __init__(self, grid):
        super().__init__(grid)
        self._start_grid = grid
        self._solution = []
        self._grid = copy.deepcopy(self._start_grid)
        self._running = True

    def begin_new_solution(self):
        self._solution = []
        self._grid = copy.deepcopy(self._start_grid)

    def stop_running(self):
        self._running = False

    def random_step(self):
        """ Checks whether the given state is a solution """
        distance = 0
        moves = []

        # keep picking a new car until one has a legal move
        while not moves:
            car = random.choice(list(self._grid._cars.keys()))
            moves = self._grid.possible_moves(car)

        distance = random.choice(moves)
        self._grid.move(car, distance)

        return [car, distance]

    def run_improving(self, method, amount, random_method = "random"):
        """ Runs a looping random algorithm """
        print("Running Random Optimized algorithm")
        best_solution = []
        best_solution_len = float("inf")
        start_time = time.perf_counter()
        beginning = time.perf_counter()
        amount = int(amount)

        # check if a correct method is chosen
        if method != "time" and method != "iterations":
            raise MethodInputError

        stop_condition = 0

        while stop_condition < amount:
            # self._solution = []
            self.begin_new_solution()

            self._solution, _ = self.run(random_method, best_solution_len + 1)

            # if a better solution is found, save it and look for better
            if best_solution_len > len(self._solution):
                best_solution = copy.deepcopy(self._solution)
                best_solution_len = len(best_solution)
                end_time = time.perf_counter()
                duration = round((end_time-start_time)/60, 2)

                print(
                    f'found a solution of {len(self._solution)} steps after around {duration} minutes')

                start_time = time.perf_counter()

            # determining the stop condition depending on chosen method
            if method == "time":
                stop_condition =  time.perf_counter() - beginning

            elif method == "iterations":
                stop_condition += 1

        return best_solution
