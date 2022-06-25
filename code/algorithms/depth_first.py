from code.classes.grid import Grid
from copy import deepcopy, copy



# misschien overerven van breadth first
class DepthFirst():
    def __init__(self, grid, best_solution=float('inf'), solutions=[]):
        self._initial_grid = deepcopy(grid)
        self._grid = deepcopy(grid)
        self._empty_grid = []
        self._stack = []
        for _ in range(grid.get_size()):
            # deepcopy(grid.get_grid())
            self._empty_grid.append(grid.get_size() * ['*'])

        self._grid = grid
        self._cars = grid.get_car_names()
        self._initial_x = {}
        self._initial_y = {}
        self._orientation = {}
        self._lengths = {}
        self._visited = {}
        self._empty_state = {}
        self._last_car = ""

        # Make dictionaries with info about all cars on the given grid
        for name in self._cars:
            self._empty_state[name] = 0
            self._initial_x[name] = grid.get_car_x(name)
            self._initial_y[name] = grid.get_car_y(name)
            self._orientation[name] = grid.get_car_orientation(name)
            self._lengths[name] = grid.get_car_length(name)

        #self._queue.put([[0 for i in range(len(self._cars))]])
        self._stack.append([[0 for i in range(len(self._cars))]])
        self._visited[tuple([0 for i in range(len(self._cars))])] = 0

        for solution in solutions:
            for i, state in enumerate(solution):
                self._visited[tuple(state)] =  i

        self._solutions = solutions
        self._best_solution = best_solution

    def possible_next_lists(self, current_list):
        """ Gives the possible lists after one move on the grid that can be made with the given list """

        # Write the list to a grid and set this as current grid.

        grid = self.list_to_grid(current_list)
        self._grid.set_grid(grid)
        next_lists = []

        # For each car see what moves are possible
        for i, car in enumerate(self._cars):

            moves = self._grid.possible_moves(car)

            if moves and max(moves) > 0:
                distance = max(moves)
                next_list = copy(current_list)
                next_list[i] += distance
                next_lists.append(next_list)

            if moves and min(moves) < 0:
                distance = min(moves)
                next_list = copy(current_list)
                next_list[i] += distance
                next_lists.append(next_list)

        return next_lists

    def route_to_state(self, route):
        state = copy(self._empty_state)
        for move in route:
            car = move[0]
            distance = move[1]
            state[car] = distance

        return state

    def list_to_grid(self, current_list):
        """ Given a list with the total moved distance from the start position for each car, draws a list of lists that represents the grid """
        grid = deepcopy(self._empty_grid)

        # Add cars
        for i, car in enumerate(self._cars):
            x = self._initial_x[car]
            y = self._initial_y[car]
            length = self._lengths[car]

            if self._orientation[car] == 'H':
                x += current_list[i]
                for j in range(length):
                    grid[y][x + j] = car
            else:
                y += current_list[i]
                for j in range(length):
                    grid[y + j][x] = car

            # Update coordinates in each Car object
            self._grid.set_car_x(car, x)
            self._grid.set_car_y(car, y)

        return grid

    def is_solution(self, state):
        """ Checks whether the given state is a solution """
        if state[-1][-1] + self._initial_x['X'] == self._grid.get_size() - 2:
            return True

        return False

    def remove_long_visited(self, length):
        for key in self._visited:
            if self._visited[key] > length:
                self._visited[key].pop()

    def check_for_better_solution(self, new_list):
        # als hij deze wel sneller doet kan het zijn dat die state al in een vorige oplossing is gevonden, als dit zo is is dit een snelleren oplossing
        for i, solution in enumerate(self._solutions):

            for j, config in enumerate(solution):

                # als de huidige staat sneller bereikt is dan in de huidige oplossing wordt dat stuk van de oplossing vervangen
                if new_list == config:
                    solution[:j] = state + [new_list]

                    # als dit beter is dan be beste oplossing wardt dat opgeslagen
                    if len(solution) < self._best_solution:
                        self._best_solution = len(solution) - 1
                        print(f'found solution of {len(solution) - 2} steps')
                        self.remove_long_visited(self._best_solution)

    def pick_best_solution(self):
        for solution in self._solutions:
            if len(solution) - 1 == self._best_solution:
                return self._grid.solution_list_to_steps(solution)

    def get_next_state(self, new_list, state):
        self._new_state = True
        self._visited[tuple(new_list)] = len(state) - 1
        child = deepcopy(state)
        child.append(new_list)
        self._stack.append(child)

    def check_for_new_state(self, state):
        if not self._new_state and len(state) > 1:
            state.pop()
            self._stack.append(state)

    def check_for_solution(self, state):
        if self._grid.win():
            print('found a solution of ' + str(len(state) - 2) + ' steps.')
            self._solutions.append(state)
            self._best_solution = len(state) - 1
            self.remove_long_visited(self._best_solution)

    def check_for_max_move(self, move, moves):
        if move == max(moves) and move > 0:
            return True

        elif move == min(moves) and move < 0:
            return True

        return False

    def run(self):
        """
        """

        current_list = deepcopy(self._empty_state)

        while self._stack:

            state = self._stack.pop()

            # pak de laatste configuratie van de huidige staat
            last_list = state[-1]
            self._grid.set_configuration_from_list(last_list)

            self.check_for_solution(state)


            self._new_state = False

            # zorg dat er niet verder wordt gezocht dan de lengte van de beste oplossing
            if len(state) < self._best_solution - 1:

                # maak een set van alle bezochte staten
                current_steps = len(state)

                # check voor elke auto of er zetten mogelijk zijn en pak er een die naar een nieuwe state leidt
                for i, car in enumerate(self._cars):

                    moves = self._grid.possible_moves(car)

                    for move in moves:

                        # make a copy of the last list to add a move
                        new_list = copy(last_list)

                        # get the maximum move
                        if self.check_for_max_move(move, moves):
                            new_list[i] += move

                        else:
                            continue


                        if tuple(new_list) in self._visited and self._visited[tuple(new_list)] < current_steps:
                            continue

                        # als deze configuratie  al een keer bereikt is en hij deze keer niet sneller is dan de vorige keer slaan we hem over
                        if tuple(new_list) in self._visited and self._visited[tuple(new_list)] > current_steps:
                            self.check_for_better_solution(new_list)

                        self.get_next_state(new_list, state)
                        break

            # check of het algoritme nog wel een nieuwe staat kan bereiken, anders wordt er een stap terug gedaan
            state = self.check_for_new_state(state)

        return self.pick_best_solution()
