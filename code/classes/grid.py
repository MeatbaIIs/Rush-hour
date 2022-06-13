from car import Car
import random


class Grid():
    def __init__(self, size=7):
        self._grid = []
        for i in range(size):
            self._grid.append(size * ['*'])
        self._cars = {}
        self._size = size

    def add_car(self, name, orientation, x, y, length, car_num):
        """Add a car to the grid"""
        car = Car(name, orientation, x, y, length, self._size, car_num)
        self._cars[name] = car

        # change empty spaces to the right letter
        for i in range(length):
            if orientation == 'H':
                self._grid[y][x + i] = name
            elif orientation == 'V':
                self._grid[y + i][x] = name

    def random_algorythm(self):
        """Move a random car randomly and check for the win condition"""
        random_car = random.choice(list(self._cars.keys()))

        steps = 0
        # t = time.time()
        while not self.win():
            # get the possible moves and pick a random one
            moves = self.possible_moves(random_car)

            if moves:
                steps += 1
                random_move = random.choice(moves)
                self.move(random_car, random_move)

            # pick a new random car
            random_car = random.choice(list(self._cars.keys()))
        # print(f"Yay, solved in {steps} steps and {time.time() - t} seconds")

        return steps

    def random_step(self):
        """Move a random car randomly and check for the win condition"""
        # auto's uit het
        cars = self._cars
        moves = []

        while not moves:
            random_car = random.choice(list(cars.keys()))
            moves = self.possible_moves(random_car)

        random_move = random.choice(moves)
        self.move(random_car, random_move)
        return random_car + ',' + str(random_move)

    def move(self, name, distance):
        """Move a car a set distance, does not check if its a possible move"""

        # get variables
        car = self._cars[name]
        coor = car.coordinates()
        orientation = car._orientation
        length = car._length

        x = coor[0]
        y = coor[1]

        # check orientation
        if orientation == 'H':
            new_x = x + distance
            # empty the previous space of the car
            self._grid[y][x:x+length] = length * ["*"]

            # fill the new space of the car
            self._grid[y][new_x:new_x + length] = length * [name]

            # change coordinates of car
            car.set_coordinates(new_x, y)

        # same as horizontal orientation
        elif orientation == 'V':
            new_y = y + distance
            for i in range(length):
                self._grid[y+i][x] = "*"
            for i in range(length):
                self._grid[new_y + i][x] = name
            car.set_coordinates(x, new_y)

        # print(name + ',', distance)

    def possible_cars(self, x, y):
        """ Generates a set of cars that could move to given coordinates. """
        if not self._grid[y][x] == '*':
            return {}
        possible_cars = {}
        for car in self._cars.values():
            grid_values = []
            if car._orientation == 'H' and car._y == y:
                distance = x-car._x
                if x < car._x:
                    grid_values = self._grid[y][x:car._x+1]
                elif x > car._x:
                    grid_values = self._grid[y][car._x:x+1]
            elif car._orientation == 'V' and car._x == x:
                distance = y-car._y
                if y < car._y:
                    grid_values = self._grid[y: car._y+1][x]
                elif y > car._y:
                    grid_values = self._grid[car._y: y+1][x]

            if grid_values and all(value in ['*', car._name] for value in grid_values):
                possible_cars[car] = distance
                print(car._name)

        print(possible_cars)
        return possible_cars

    def possible_moves(self, name):
        """Gives the possible moves of a given car"""

        # get variables
        moves = []
        car = self._cars[name]
        orientation = car._orientation
        length = car._length
        coor = car.coordinates()

        x = coor[0]
        y = coor[1]

        # check orientation and then checks the empty spaces in front and behind the car
        if orientation == 'H':
            distance = 0
            # go through spaces in front of car
            for i in range(x + 1, self._size - length + 1):
                space = True

                # check if the space is big enough for the car
                for j in range(length):
                    if not (self._grid[y][i + j] == '*' or self._grid[y][i + j] == name):
                        space = False
                        break

                if space:
                    distance += 1
                    moves.append(distance)
                else:
                    break

            distance = 0

            # go through spaces behind the car. No need to check for size, since coordinates are back of the car
            for i in range(x - 1, -1, -1):
                if self._grid[y][i] == '*' or self._grid[y][i] == name:
                    distance -= 1
                    moves.append(distance)
                else:
                    break

        # same as horizontal orientation
        elif orientation == 'V':
            distance = 0
            for i in range(y + 1, self._size - length + 1):
                space = True
                for j in range(length):
                    if not (self._grid[i + j][x] == '*' or self._grid[i + j][x] == name):
                        space = False
                        break
                if space:
                    distance += 1
                    moves.append(distance)
                else:
                    break

            distance = 0
            for i in range(y - 1, -1, -1):
                if self._grid[i][x] == '*' or self._grid[i][x] == name:
                    distance -= 1
                    moves.append(distance)
                else:
                    break
        #print(name, moves)
        return moves

    def movable_neighbours(self, x, y):
        """
        gives the cars that can move to a certain sport given their orientation and that
        they are the first car towards the point. The point must be * ofcourse
        """
        coordinate = self._grid[y][x]
        movable_neighbours = {}
        # loop over next neighbours up till the size of the board
        if coordinate != "*":
            return {}

        for i in range(1, self._size):
            # cant go over grid size or break loop
            if y + i > self._size - 1:
                break
            # checks that the next grid element is a car name
            elif self._grid[y + i][x] != "*":
                neighbour = self._grid[y + i][x]
                if self._cars[neighbour]._orientation == "V":
                    car = self._cars[neighbour]
                    movable_neighbours[car] = car._name, -i
                # doesnt add any cars if there is a horizontal car blocking the way
                break

        for i in range(1, self._size):
            if y - i < 0:
                break
            elif self._grid[y - i][x] != "*":
                neighbour = self._grid[y - i][x]
                if self._cars[neighbour]._orientation == "V":
                    car = self._cars[neighbour]
                    # distance is negative
                    movable_neighbours[car] = car._name, i
                break

        for j in range(1, self._size):
            if x + j > self._size - 1:
                break
            elif self._grid[y][x + j] != "*":
                neighbour = self._grid[y][x + j]
                if self._cars[neighbour]._orientation == "H":
                    car = self._cars[neighbour]
                    movable_neighbours[car] = car._name, -j
                break

        for j in range(1, self._size):
            if x - j < 0:
                break
            elif self._grid[y][x - j] != "*":
                neighbour = self._grid[y][x - j]
                if self._cars[neighbour]._orientation == "H":
                    car = self._cars[neighbour]
                    # distance is negative
                    movable_neighbours[car] = car._name, j
                break

        return movable_neighbours

    def give_empties(self):
        """ gives a list of the coordinates of all empty locations on the board """
        list_of_empties = []

        for y in range(self._size):
            for x in range(self._size):
                element = self._grid[y][x]
                if element == "*":
                    list_of_empties.append((x, y))

        return list_of_empties

    def give_all_possible_moves(self):
        """ give all possible moves after inputting all empty locations """
        empties = self.give_empties()
        total_coords = {}

        for element in empties:
            coords = self.movable_neighbours(element[0], element[1])
            total_coords.update(coords)

        return total_coords

    def other_random_algorithm(self):
        iterator = 0
        while self.win() == False:
            list_of_empties = self.give_empties()
            empty = random.choice(list_of_empties)
            possible_moves = self.movable_neighbours(empty[0], empty[1])

            if len(possible_moves) != 0:
                moving_car = random.choice(list(possible_moves.keys()))
                car_name, car_distance = possible_moves[moving_car]

                self.move(car_name, car_distance)
                iterator += 1

        # self.print_grid()
        # print(f"we have won after {iterator} moves")
        return iterator

    def print_grid(self):
        for y in self._grid:
            print(''.join(y))
        print()

    def win(self):
        """Check if the red car can reach the end"""
        x, y = self._cars['X'].coordinates()

        # check whether every space before the red car is empty
        if self._grid[y][x + 2:self._size] == (self._size - x - 2) * ["*"]:
            return True
        return False


# if __name__ == '__main__':
    # grid = Grid()
    # grid.add_car('X', 'H', 2, 3, 2)
    # grid.print_grid()
    # #grid.move('X', 3)
    # # grid.print_grid()
    # # print(grid.possible_moves('X'))
    # grid.random_algorythm()
