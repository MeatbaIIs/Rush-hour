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
            for i, state in enumerate(solution):
                self._visited[tuple(state)] =  i

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

    def check_for_better_solution(self, new_list, state):
        """
        Looks if the current configuration has been used for a solution and
        replaces part of the steps if this is is a faster way to reach the solution
        """
        for i, solution in enumerate(self._solutions):

            for j, config in enumerate(solution):

                # if the current configuration has been reached faster than in the solution replace the steps
                if new_list == config:
                    solution[:j + 1] = state + [new_list]

                    # if this is better than the current best solution, update the length of the best solution
                    if len(solution) < self._best_solution:
                        self._best_solution = len(solution) - 1
                        print(f'found solution of {len(solution) - 2} steps')
                        self.remove_long_visited(self._best_solution)
                        print(total_movements_sequence_to_steps(self._grid, solution))


    def pick_best_solution(self):
        """pick the beste solution out of al solutions found"""
        best_solution_len = float('inf')
        best_solution_steps = []

        for solution in self._solutions:
            if len(solution) < best_solution_len:
                best_solution_steps = total_movements_sequence_to_steps(self._grid, solution)

        return best_solution_steps

    def get_next_state(self, new_list, state):
        """add a new configuration to the stack"""
        self._new_state = True
        self._visited[tuple(new_list)] = len(state) - 1
        state.append(new_list)
        return state

    def check_for_new_state(self, state):
        """check whether a new configuration can be reached, otherwise take a step back"""
        if not self._new_state and len(state) > 0:
            state.pop()

        return state

    def check_for_solution(self, state):
        """checks whether a solution is reached"""
        if self._grid.win():
            print('found a solution of ' + str(len(state) - 1) + ' steps.')
            self._solutions.append(copy(state))
            self._best_solution = len(state) - 1
            self.remove_long_visited(self._best_solution)
            print(total_movements_sequence_to_steps(self._grid, state))

    def run(self, method):
        """
        Runs the depth-first algorithm with as little memory use as possible
        """
        state = [[0 for i in range(len(self._grid.get_car_names()))]]
        if method != "furthest" and method != "optimal":
            raise MethodInputError

        while state:

            # get the last configuaration of the current state
            last_list = state[-1]
            set_total_movements(self._grid, last_list)
            self._new_state = False
            current_steps = len(state) - 1

            # check for every car what moves are available and try them
            for i, car in enumerate(self._grid.get_car_names()):

                moves = self._grid.possible_moves(car)

                # make sure to stop searching deeper when the length of the best solution is reached
                if len(state) < self._best_solution:
                    if method == "furthest":
                        if moves:
                            moves = set([max(moves), min(moves)])

                        else:
                            continue

                    for move in moves:

                        # make a copy of the last list to add a move
                        new_list = copy(state[-1])
                        new_list[i] += move

                        # if the configuration has been reached before and has now been reached faster, check for a better solution
                        if tuple(new_list) in self._visited and self._visited[tuple(new_list)] > current_steps:
                            self.check_for_better_solution(new_list, state)
                            state = self.get_next_state(new_list, state)
                            set_total_movements(self._grid, new_list)

                            # break so the same car does not move twice in a row
                            break

                        # if the configuration has never been reached, try it out
                        elif tuple(new_list) not in self._visited:
                            state = self.get_next_state(new_list, state)
                            set_total_movements(self._grid, new_list)
                            self.check_for_solution(state)

                            # break so the same car does not move twice in a row
                            break

            # check whether the algorithm reached a new state, otherwise take a step back
            state = self.check_for_new_state(state)

        return self.pick_best_solution()
