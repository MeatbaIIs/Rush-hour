from code.classes.grid import Grid
from copy import deepcopy, copy
from code.helpers import steps_to_total_movements_sequence, set_total_movements, total_movements_sequence_to_steps, MethodInputError



class DepthFirst():
    def __init__(self, grid, best_solution=float('inf'), solution=[]):
        self._grid = grid
        amount_of_cars = len(self._grid.get_car_names())
        self._visited = {tuple([0 for i in range(amount_of_cars)]):0}

        # if there is a solution add it to current solution
        if solution:
            solution = steps_to_total_movements_sequence(grid, solution)
            self._solutions = [solution]

            # add all visited configuration to visited
            for i, total_movements_sequence in enumerate(solution):
                self._visited[tuple(total_movements_sequence)] =  i

        else:
            self._solutions = []

        # keep track of the length of the best solution
        self._best_solution = best_solution

    def remove_long_visited(self, length):
        """removes the configurations in visited that are longer than the current best solution"""
        to_remove = []

        for key in self._visited:
            if self._visited[key] > length:
                to_remove.append(key)

        for key in to_remove:
            del self._visited[key]

    def check_for_better_solution(self, new_total_movements, total_movements_sequence):
        """
        Looks if the current configuration has been used for a solution and
        replaces part of the steps if this is is a faster way to reach the solution
        """
        for i, solution in enumerate(self._solutions):

            for j, config in enumerate(solution):

                # if the current configuration has been reached faster than in the solution replace the steps
                if new_total_movements == config:
                    solution[:j + 1] = total_movements_sequence + [new_total_movements]

                    # if this is better than the current best solution, update the length of the best solution
                    if len(solution) - 1 < self._best_solution:
                        self._best_solution = len(solution) - 1
                        print(f'found a solution of {len(solution) - 1} steps')
                        self.remove_long_visited(self._best_solution)
                        # print(total_movements_sequence_to_steps(self._grid, solution))


    def pick_best_solution(self):
        """pick the beste solution out of al solutions found"""
        best_solution_len = float('inf')
        best_solution_steps = []

        for solution in self._solutions:
            if len(solution) < best_solution_len:
                best_solution_steps = total_movements_sequence_to_steps(self._grid, solution)

        return best_solution_steps

    def get_next_total_movements_sequence(self, new_total_movements, total_movements_sequence):
        """add a new configuration to the stack"""
        self._new_state = True
        self._visited[tuple(new_total_movements)] = len(total_movements_sequence) - 1
        total_movements_sequence.append(new_total_movements)
        return total_movements_sequence

    def check_for_new_total_movements_sequence(self, total_movements_sequence):
        """check whether a new configuration can be reached, otherwise take a step back"""
        if not self._new_state and len(total_movements_sequence) > 0:
            total_movements_sequence.pop()

        return total_movements_sequence

    def check_for_solution(self, total_movements_sequence):
        """checks whether a solution is reached"""
        if self._grid.win():
            print('found a solution of ' + str(len(total_movements_sequence) - 1) + ' steps.')
            self._solutions.append(copy(total_movements_sequence))
            self._best_solution = len(total_movements_sequence) - 1
            self.remove_long_visited(self._best_solution)
            # print(total_movements_sequence_to_steps(self._grid, total_movements_sequence))

    def run(self, method):
        """
        Runs the depth-first algorithm with as little memory use as possible
        """
        total_movements_sequence = [[0 for i in range(len(self._grid.get_car_names()))]]
        if method != "furthest" and method != "optimal":
            raise MethodInputError

        while total_movements_sequence:

            # get the last configuaration of the current total_movements_sequence
            last_total_movements = total_movements_sequence[-1]
            set_total_movements(self._grid, last_total_movements)
            self._new_state = False

            # check for every car what moves are available and try them
            for i, car in enumerate(self._grid.get_car_names()):

                moves = self._grid.possible_moves(car)
                current_steps = len(total_movements_sequence) - 1

                # make sure to stop searching deeper when the length of the best solution is reached
                if current_steps + 1 < self._best_solution:
                    if method == "furthest":
                        if moves:
                            new_moves = set()
                            if min(moves) < 0:
                                new_moves.add(min(moves))

                            if max(moves) > 0:
                                new_moves.add(max(moves))

                            moves = new_moves

                        else:
                            continue

                    for move in moves:

                        # make a copy of the last total_movements to add a move
                        new_total_movements = copy(total_movements_sequence[-1])
                        new_total_movements[i] += move

                        # if the configuration has been reached before and has now been reached faster, check for a better solution
                        if tuple(new_total_movements) in self._visited and self._visited[tuple(new_total_movements)] > current_steps:
                            self.check_for_better_solution(new_total_movements, total_movements_sequence)
                            total_movements_sequence = self.get_next_total_movements_sequence(new_total_movements, total_movements_sequence)
                            set_total_movements(self._grid, new_total_movements)

                            # break so the same car does not move twice in a row
                            break

                        # if the configuration has never been reached, try it out
                        elif tuple(new_total_movements) not in self._visited:
                            total_movements_sequence = self.get_next_total_movements_sequence(new_total_movements, total_movements_sequence)
                            set_total_movements(self._grid, new_total_movements)
                            self.check_for_solution(total_movements_sequence)

                            # break so the same car does not move twice in a row
                            break

            # check whether the algorithm reached a new total_movements_sequence, otherwise take a step back
            total_movements_sequence = self.check_for_new_total_movements_sequence(total_movements_sequence)

        return self.pick_best_solution()
