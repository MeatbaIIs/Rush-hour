import random
import copy
from code.classes.grid import Grid
from code.classes.car import Car
import time


class Random():
    def __init__(self, grid):
        self._grid = grid
        self._last_car = ""
        self._previous_steps = []

    def random_algorithm(self):
        """Move a random car randomly and check for the win condition"""
        random_car = random.choice(list(self._grid._cars.keys()))

        st = time.time()
        while not self._grid.win():

            # get the possible moves
            moves = self._grid.possible_moves(random_car)

            if moves and random_car != self._last_car:

                random_move = random.choice(moves)
                self._grid.move(random_car, random_move)

                # keep track of all the moves done
                self._previous_steps.append([random_car, random_move])

            self._last_car = random_car

            # pick a new random car
            random_car = random.choice(list(self._grid._cars.keys()))

        et = time.time()
        time_taken = et - st
        return self._previous_steps, time_taken

    def random_algorithm_max_move(self):
        """Move a random car either forward or backward maximally and check for the win condition"""
        random_car = random.choice(list(self._grid._cars.keys()))

        st = time.time()
        while not self._grid.win():
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

            # pick a new random car
            random_car = random.choice(list(self._grid._cars.keys()))

        et = time.time()
        time_taken = et - st
        return self._previous_steps, time_taken

    def random_algorithm_all_cars(self):
        """Move all cars one by one randomly and check for the win condition"""
        st = time.time()

        while not self._grid.win():

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

        et = time.time()
        time_taken = et - st
        return self._previous_steps, time_taken

    def run(self, method):
        """Runs an algorithm based on the chosen method"""
        if method == "max_random":
            previous_steps, time_taken = self.random_algorithm_max_move()
            return previous_steps, time_taken
        elif method == "random_not_prev":
            previous_steps, time_taken = self.random_algorithm_all_cars()
            return previous_steps, time_taken
        elif method == "random":
            previous_steps, time_taken = self.random_algorithm()
            return previous_steps, time_taken
        else:
            raise MethodInputError

class MethodInputError(Exception):
    """Raised when a method input is wrong for Random.run()"""
    """possible inputs are 'max_random' and 'random_not_prev' """
    pass
