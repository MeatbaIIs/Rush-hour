import copy
import random
from code.classes.grid import Grid

class Depth_first():
    def __init__(self, grid):
        self._current_grid = grid
        self._previous_grids = [copy.deepcopy(grid._grid)]
        self._previous_steps = []
        self._last_car = []
        self._count = 0

    def step(self, i):
        """Gets a new state for the grid"""

        # check whether a new state has been found
        new_state = False

        # check the moves for every car
        # for car in self._current_grid._cars.keys():

        # get the moves of a car and check whether any moves are possible
        # moves = []
        # counter = 0
        # while (not moves or car in self._last_car) and counter < 10:
        #     car = random.choice(list(self._current_grid._cars.keys()))
        #     moves = self._current_grid.possible_moves(car)
        #     counter += 1
        #
        # self._last_car.append(car)
        #
        # # initialize check variable
        # check = False
        #
        # # first try the furthest moving moves
        # if moves and max(moves) > 0:
        #     new_state, check, i = self.check_move(car, max(moves), new_state, i)
        #     moves.remove(max(moves))
        # if moves and min(moves) < 0 and not check:
        #     new_state, check, i = self.check_move(car, min(moves), new_state, i)
        #     moves.remove(min(moves))
        #
        # # if the furthest moves dont deliver a new state, try the other moves
        # if not check:
        #     for move in moves:
        #         new_state, check, i = self.check_move(car, move, new_state, i)
        #         if check:
        #             break


        # check the moves for every car
        for car in self._current_grid._cars.keys():

            # get the moves of a car and check whether any moves are possible
            moves = self._current_grid.possible_moves(car)
            if not moves:
                continue


            # initialize check variable
            check = False

            # first try the furthest moving moves
            if max(moves) > 0:
                new_state, check, i = self.check_move(car, max(moves), new_state, i)
                moves.remove(max(moves))
            if moves and min(moves) < 0 and not check:
                new_state, check, i = self.check_move(car, min(moves), new_state, i)
                moves.remove(min(moves))

            # if the furthest moves dont deliver a new state, try the other moves
            if not check:
                for move in moves:
                    new_state, check, i = self.check_move(car, move, new_state, i)
                    if check:
                        break

            # check whether the game has been won, and print al steps
            if self._current_grid.win():
                for step in self._previous_steps:
                    step[1] = str(step[1])
                    print(", ".join(step))
                    #break

        # if no car could move for a new state, go back to previous states
        # if not new_state and self._count < 3:
        #     self._count += 1
        if not new_state:
            last_step = self._previous_steps.pop(-1)
            self._current_grid.move(last_step[0], -1 * last_step[1])
            i -= 1
            self._count = 0
            self._last_car = []

        return i

    def check_move(self, car, move, new_state, i):
        """checks whether a move is feasible"""
        self._current_grid.move(car, move)

        # if the new state is has already been, move back
        if self._current_grid._grid in self._previous_grids:
            self._current_grid.move(car, -1 * move)
            return new_state, False, i

        # if a new state is a achieved, add it to the list
        else:
            i += 1
            self._previous_grids.append(copy.deepcopy(self._current_grid._grid))
            self._previous_steps.append([car, move])
            self._last_car = [car]
            print(car)
            self._current_grid.print_grid()
            new_state = True
            self._count = 0
            return new_state, True, i

    def run(self):
        """run the algorithm"""
        i = 0
        while not self._current_grid.win():
            i = self.step(i)
        print(f"won in {i} steps")
