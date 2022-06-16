import copy
import random
from code.classes.grid import Grid


class Depth_first():
    def __init__(self, grid):
        self._current_grid = grid
        self._previous_grids = [copy.deepcopy(grid)]
        self._previous_steps = []
        self._new_state = False


    def step(self, i):
        """Gets a new state for the grid"""

        # check the moves for every car
        i = 0
        for original_grid in self._previous_grids:
            self._previous_grids.remove(original_grid)
            i += 1

            for car in grid._cars.keys():

                # get the moves of a car and check whether any moves are possible
                moves = grid.possible_moves(car)

                if not moves:
                    continue

                for move in moves:
                    self.check_move(grid, car, move, i)

                # initialize check variable
                #check = False

                # first try the furthest moving moves
                # if max(moves) > 0:
                #     check, i = self.check_move(car, max(moves), i)
                #     moves.remove(max(moves))
                # if moves and min(moves) < 0 and not check:
                #     check, i = self.check_move(car, min(moves), i)
                #     moves.remove(min(moves))



                # check whether the game has been won, and print al steps
                if grid.win():
                    print(i)
                    break

                # grid.print_grid()

            # if no car could move for a new state, go back to previous states
            # if not self._new_state:
            #     pass

                # last_step = self._previous_steps.pop(-1)
                # self._current_grid.move(last_step[0], -1 * last_step[1])
                # i -= 1

    def check_move(self, grid, car, move, i):
        """checks whether a move is feasible"""
        grid.move(car, move)

        # if the new state is has already been, move back
        if grid not in self._previous_grids:
            # we hebbben duncan's wondercode nog nodig hier
            self._previous_grids.append(copy.deepcopy(self._current_grid._grid))
            # self._previous_moves[i].append([car, move])
            self._new_state = True

    def run(self):
        """run the algorithm"""
        i = 0
        while not self._current_grid.win():
            i = self.step(i)
        print(f"won in {i} steps")

        return self._previous_steps
