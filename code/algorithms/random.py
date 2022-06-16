import random
import copy
from code.classes.grid import Grid
from code.classes.car import Car

class Random():
    def __init__(self, grid):
        self._grid = grid
        self._last_car = ""
        self._previous_steps = []

    def random_algorithm(self):
        """Move a random car randomly and check for the win condition"""
        random_car = random.choice(list(self._grid._cars.keys()))

        steps = 0
        # t = time.time()
        while not self._grid.win():
            # get the possible moves and pick a random one
            moves = self._grid.possible_moves(random_car)
            #print(random_car,moves)

            if moves and random_car != self._last_car:
                steps += 1
                # if min(moves) < 0:
                #     min_move = min(moves)
                # else:
                #     min_move = max(moves)
                #
                # if max(moves) > 0:
                #     max_move = max(moves)
                # else:
                #     max_move = min(moves)

                random_move = random.choice(moves)
                self._grid.move(random_car, random_move)
                self._previous_steps.append([random_car, random_move])
            # pick a new random car
            self._last_car = random_car
            random_car = random.choice(list(self._grid._cars.keys()))
        # print(f"Yay, solved in {steps} steps and {time.time() - t} seconds")

        return self._previous_steps

    def random_algorithm_max_move(self):
        """Move a random car randomly and check for the win condition"""
        random_car = random.choice(list(self._grid._cars.keys()))

        steps = 0
        # t = time.time()
        while not self._grid.win():
            # get the possible moves and pick a random one
            moves = self._grid.possible_moves(random_car)

            if moves and random_car != self._last_car:
                steps += 1
                if min(moves) < 0:
                    min_move = min(moves)
                else:
                    min_move = max(moves)

                if max(moves) > 0:
                    max_move = max(moves)
                else:
                    max_move = min(moves)

                random_move = random.choice([min_move,max_move])
                self._grid.move(random_car, random_move)
                self._last_car = random_car


            # pick a new random car
            random_car = random.choice(list(self._grid._cars.keys()))
        # print(f"Yay, solved in {steps} steps and {time.time() - t} seconds")

        return steps

    def random_algorithm_all_cars(self):
        """Move a random car randomly and check for the win condition"""
        random_car = random.choice(list(self._grid._cars.keys()))

        steps = 0
        # t = time.time()
        while not self._grid.win():

            for random_car in self._grid._cars:

                # get the possible moves and pick a random one
                moves = self._grid.possible_moves(random_car)
                if moves and random_car != self._last_car:
                    steps += 1
                    # if min(moves) < 0:
                    #     min_move = min(moves)
                    # else:
                    #     min_move = max(moves)
                    #
                    # if max(moves) > 0:
                    #     max_move = max(moves)
                    # else:
                    #     max_move = min(moves)

                    random_move = random.choice(moves)
                    self._grid.move(random_car, random_move)
                    #self._last_car = random_car
                if self._grid.win():
                    break

            # pick a new random car
            #random_car = random.choice(list(self._grid._cars.keys()))
        # print(f"Yay, solved in {steps} steps and {time.time() - t} seconds")

        return steps

    def other_random_algorithm(self):
        iterator = 0
        while not self._grid.win():
            list_of_empties = self._grid.give_empties()
            empty = random.choice(list_of_empties)
            possible_moves = self._grid.movable_neighbours(empty[0], empty[1])

            if len(possible_moves) != 0:
                moving_car = random.choice(list(possible_moves.keys()))
                car_name, car_distance = possible_moves[moving_car]

                self._grid.move(car_name, car_distance)
                iterator += 1

        #self._grid.print_grid()
        return iterator
        #print(f"we have won after {iterator} moves")

    def random_step(self):
        """Move a random car randomly and check for the win condition"""
        # auto's uit het
        cars = self._grid._cars
        moves = []

        while not moves:
            random_car = random.choice(list(cars.keys()))
            moves = self._grid.possible_moves(random_car)

        random_move = random.choice(moves)
        self.move(random_car, random_move)
        return random_car + ',' + str(random_move)
