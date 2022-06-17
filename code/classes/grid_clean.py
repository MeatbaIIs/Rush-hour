from .car import Car
import random


class Grid():
    def __init__(self, size=7):
        self._grid = []
        for i in range(size):
            self._grid.append(size * ['*'])
        # dictionary of all the cars
        self._cars = {}

        # keep track of the movement per car to compare grids
        self._total_movements = {}


        self._size = size
        self._last_car = ""

    def add_car(self, name, orientation, x, y, length, car_num):
        """Add a car to the grid"""
        car = Car(name, orientation, x, y, length, self._size)  # car_num)
        self._cars[name] = car

        # change empty spaces to the right letter
        for i in range(length):
            if orientation == 'H':
                self._grid[y][x + i] = name
            elif orientation == 'V':
                self._grid[y + i][x] = name

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

                # if there is enough space add the distacne
                if space:
                    distance += 1
                    moves.append(distance)

                # if there is not enough space there is no need to look further
                else:
                    break

            # set distance back to zero to look behind the car
            distance = 0

            # go through spaces behind the car. No need to check for size, since coordinates are back of the car
            for i in range(x - 1, -1, -1):

                # check if spaces behind the car are empty
                if self._grid[y][i] == '*' or self._grid[y][i] == name:
                    distance -= 1
                    moves.append(distance)

                # if a space is not free there is no need to look further
                else:
                    break

        # same structure as horizontal orientation
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
        return moves

    def print_grid(self):
        for y in self._grid:
            print(''.join(y))
        print()

    def get_grid(self):
        return self._grid

    def set_grid(self, new_state):
        self._grid = new_state
        return

    def get_car_names(self):
        return list(self._cars.keys())

    def get_car_x(self, car_name):
        return self._cars[car_name].get_x()

    def get_car_y(self, car_name):
        return self._cars[car_name].get_y()

    def set_car_x(self, car_name, x):
        return self._cars[car_name].set_x(x)

    def set_car_y(self, car_name, y):
        return self._cars[car_name].set_y(y)

    def get_car_orientation(self, car_name):
        return self._cars[car_name].get_orientation()

    def get_car_length(self, car_name):
        return self._cars[car_name].get_length()

    def get_size(self):
        return self._size

    def win(self):
        """Check if the red car can reach the end"""
        x, y = self._cars['X'].coordinates()

        # check whether every space before the red car is empty
        if self._grid[y][x + 2:self._size] == (self._size - x - 2) * ["*"]:
            return True
        return False
