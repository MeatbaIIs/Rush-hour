import copy


class Improving_algorithm():
    def __init__(self, grid, solution):
        self._grid = grid
        self._solution = solution
        self._test_solution = []  # copy.deepcopy(self._solution)

    def correct_later_moves(self, car, distance, step):
        """ correct the next move of car 'car' after step 'step' for the given distance. """
        for i in range(step, len(self._test_solution)):
            if self._test_solution[i][0] == car:
                self._test_solution[i][1] -= distance
                break

    def check_solution(self):
        """ Returns True if test_solution is a valid solution. """
        gridcopy = copy.deepcopy(self._grid)

        for move in self._test_solution:
            car = move[0]
            distance = move[1]

            if distance in gridcopy.possible_moves(car):
                gridcopy.move(car, distance)

            else:
                return False

        if gridcopy.win():
            return True

        return False

    def step(self, i):
        """ Remove move at index i from solution, correct the next move of that car, and modify the solution if the new solution is valid. """
        self._test_solution = copy.deepcopy(self._solution)
        deleted_step = self._test_solution.pop(i)
        car = deleted_step[0]
        distance = deleted_step[1]

        self.correct_later_moves(car, distance, i)

        if self.check_solution():
            self._solution = copy.deepcopy(self._test_solution)
            return True

        return False

    def run(self):
        """ Check for every move if it can be removed from the solution and return the optimized solution """
        found_optimization = True

<<<<<<< HEAD
        while found__optimization:
=======
        while found_optimization:
>>>>>>> f6196a79503b7d8796c770fdaf119a222cdc798d
            found_optimization = False

            for i in range(len(self._solution)):
                if self.step(i):
                    found_optimization = True
                    break

        return self._solution
