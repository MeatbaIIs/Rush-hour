"""
This algorithm tries random steps with random cars until a solution is found
There are two variations, one to only move forward or backward maximally
The other to go through the cars one by one instead of randomly
"""


import random
import copy
from code.classes.grid import Grid
from code.classes.car import Car
import time
from code.helpers import MethodInputError

class Random():
    def __init__(self, grid):
        self._grid = grid
        self._last_car = ""
        self._previous_steps = []

    def random_algorithm(self, depth = float('inf')):
        """Move a random car randomly and check for the win condition"""
        random_car = random.choice(list(self._grid._cars.keys()))
        self._previous_steps = []

        current_depth = 0
        st = time.time()
        while not self._grid.win() and current_depth < depth:

            # get the possible moves
            moves = self._grid.possible_moves(random_car)

            if moves and random_car != self._last_car:

                random_move = random.choice(moves)
                self._grid.move(random_car, random_move)

                # keep track of all the moves done
                self._previous_steps.append([random_car, random_move])
                current_depth += 1

            self._last_car = random_car

            # pick a new random car
            random_car = random.choice(list(self._grid._cars.keys()))

        et = time.time()
        time_taken = et - st
        return self._previous_steps, time_taken

    def random_algorithm_max_move(self, depth = float('inf')):
        """Move a random car either forward or backward maximally and check for the win condition"""
        random_car = random.choice(list(self._grid._cars.keys()))
        self._previous_steps = []
        current_depth = 0
        st = time.time()
        while not self._grid.win() and current_depth < depth:
            moves = self._grid.possible_moves(random_car)

            # never move the same car twice in a row
            if moves and random_car != self._last_car:

                # pick the biggest moves either forward or backwards
                if min(moves) < 0:
                    min_move = min(moves)
                else:
                    min_move = max(moves)

                if max(moves) > 0:
                    max_move = max(moves)
                else:
                    max_move = min(moves)

                random_move = random.choice([min_move, max_move])
                self._grid.move(random_car, random_move)

                # keep track of the moves done
                self._previous_steps.append([random_car, random_move])

                # make sure the same car never moves twice
                self._last_car = random_car
                current_depth += 1

            # pick a new random car
            random_car = random.choice(list(self._grid._cars.keys()))

        et = time.time()
        time_taken = et - st
        return self._previous_steps, time_taken

    def random_algorithm_all_cars(self, depth = float('inf')):
        """Move all cars one by one randomly and check for the win condition"""
        st = time.time()
        current_depth = 0
        self._previous_steps = []

        while not self._grid.win() and current_depth < depth:

            # get the cars one by one
            for car in self._grid._cars:

                # get the possible moves and pick a random one
                moves = self._grid.possible_moves(car)

                # never move the same car twice in a row
                if moves:
                    random_move = random.choice(moves)
                    self._grid.move(car, random_move)

                    # keep track of all the moves done
                    self._previous_steps.append([car, random_move])
                    current_depth +=1
        et = time.time()
        time_taken = et - st
        return self._previous_steps, time_taken

    def run(self, method, depth = float("inf")):
        """Runs an algorithm based on the chosen method"""
        if method == "max_random":
            previous_steps, time_taken = self.random_algorithm_max_move(depth)
            return previous_steps, time_taken
        elif method == "random_not_prev":
            previous_steps, time_taken = self.random_algorithm_all_cars(depth)
            return previous_steps, time_taken
        elif method == "random":
            previous_steps, time_taken = self.random_algorithm(depth)
            return previous_steps, time_taken
        else:
            raise MethodInputError
