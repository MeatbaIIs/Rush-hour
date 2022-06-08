from car import Car
#from loader import loader
import random


class Grid():
    def __init__(self, size=7):
        self._grid = []
        for i in range(size):
            self._grid.append(size * ['*'])
        self._cars = {}
        self._size = size

    def add_car(self, name, orientation, x, y, length):
        """Add a car to the grid"""
        car = Car(name, orientation, x, y, length, self._size)
        self._cars[name] = car
        for i in range(length):
            if orientation == 'H':
                self._grid[y][x + i] = name
            elif orientation == 'V':
                self._grid[y + i][x] = name

    def random_algorythm(self):
        random_car = random.choice(list(self._cars.keys()))
        while not self.win():
            moves = self.possible_moves(random_car)
            random_move = random.choice(moves)
            print(random_move)
            self.move(random_car, random_move)
            self.print_grid()
            random_car = random.choice(list(self._cars.keys()))
        print("Yay,solved")

    def move(self, name, distance):
        """Move a car a set distance, does not check if its a possible move"""
        car = self._cars[name]
        coor = car.coordinates()
        orientation = car._orientation
        length = car._length

        x = coor[0]
        y = coor[1]

        if orientation == 'H':
            new_x = x + distance
            self._grid[y][x:x+length] = length * ["*"]
            self._grid[y][new_x:new_x + length] = length * [name]
            # aanpassen naar een functie
            car._x = new_x
        elif orientation == 'V':
            new_y = y + distance
            self._grid[y:y+length][x] = length * ["*"]
            self._grid[new_y: new_y + length][x] = length * [name]
            # aanpassen naar een functie
            car._y = new_y

    def possible_cars(self, x, y):
        """ Generates a set of cars that could move to given coordinates. """
        if not self._grid[y][x] == '*':
            return set()
        possible_cars = set()
        for car in self._cars.values():
            grid_values = []
            if car._orientation == 'H' and car._y == y and x < car._x:
                grid_values = self._grid[y][x:car._x+1]
            elif car._orientation == 'H' and car._y == y and x > car._x:
                grid_values = self._grid[y][car._x:x+1]
            elif car._orientation == 'V' and car._x == x and y < car._y:
                grid_values = self._grid[y: car._y+1][x]
            elif car._orientation == 'V' and car._x == x and y > car._y:
                grid_values = self._grid[car._y: y+1][x]

            if grid_values and all(value in ['*', car._name] for value in grid_values):
                possible_cars.add(car)
                print(car._name)

        print(possible_cars)
        return possible_cars

    def possible_moves(self, name):
        """Gives the possible moves of a given car"""
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
            for i in range(x + length, self._size):
                if self._grid[y][i] == '*':
                    distance += 1
                    moves.append(distance)
                else:
                    break

            distance = 0
            for i in range(x - 1, -1, -1):
                if self._grid[y][i] == '*':
                    distance -= 1
                    moves.append(distance)
                else:
                    break

        elif orientation == 'V':
            distance = 0
            for i in range(y + length, self._size):
                if self._grid[i][x] == '*':
                    distance += 1
                    moves.append(distance)
                else:
                    break

            distance = 0
            for i in range(y - 1, -1, -1):
                if self._grid[i][x] == '*':
                    distance -= 1
                    moves.append(distance)
                else:
                    break

        return moves

    # gives the cars that can move to a certain sport given their orientation and that
    # they are the first car towards the point. The point must be * ofcourse
    def movable_neighbours(self, x, y):
        coordinate = self._grid[y][x]
        movable_neighbours = {}
        # loop over next neighbours up till the size of the board
        if coordinate != "*":
            print("input is not a *")
            return

        for i in range(1, self._size):
            # cant go over grid size or break loop
            if y + i >= self._size - 1:
                break
            # checks that the next grid element is a car name
            elif self._grid[y + i][x] != "*":
                neighbour = self._grid[y + i][x]
                if self._cars[neighbour]._orientation == "V":
                    car = self._cars[neighbour]
                    movable_neighbours[car] = car._name, i
                # doesnt add any cars if there is a horizontal car blocking the way
                break
            

        for i in range(1, self._size):
            if y - i < 0:
                break
            elif self._grid[y - i][x] != "*":
                neighbour = self._grid[y - i][x]
                if self._cars[neighbour]._orientation == "V":
                    car = self._cars[neighbour]
                    movable_neighbours[car] = car._name, i
                break
            

        for j in range(1, self._size):
            if x + j >= self._size - 1:
                break
            elif self._grid[y][x + j] != "*":
                neighbour = self._grid[y][x + j]
                if self._cars[neighbour]._orientation == "H":
                    car = self._cars[neighbour]
                    movable_neighbours[car] = car._name, j
                break
            
        
        for j in range(1, self._size):
            if x - j < 0:
                break
            elif self._grid[y][x - j] != "*":
                neighbour = self._grid[y][x - j]
                if self._cars[neighbour]._orientation == "H":
                    car = self._cars[neighbour]
                    movable_neighbours[car] = car._name, j
                break

        return movable_neighbours

    # gives a list of the coordinates of all empty locations on the board
    def give_empties(self):
        list_of_empties = []

        for y in range(self._size):
            for x in range(self._size):
                element = self._grid[y][x]
                if element == "*":
                    list_of_empties.append((x, y))

        return list_of_empties

    # give all possible moves after inputting all empty locations
    def give_all_possible_moves(self):
        empties = self.give_empties()
        total_coords = {}

        for element in empties:
            coords = self.movable_neighbours(element[0], element[1])
            total_coords.update(coords)

        print(total_coords)
        return total_coords


    def print_grid(self):
        for y in self._grid:
            print(''.join(y))

    def win(self):
        x, y = self._cars['X'].coordinates()
        # win = True
        print((self._size - x - 2) * ["*"])
        if not self._grid[y][x + 2:self._size] == (self._size - x - 2) * ["*"]:
            return False
        return True
        # for i in range(x + 2, self._size):
        #     if not self._grid[y][i] == "*":
        #         win = False
        #         break
        # return win


if __name__ == '__main__':
    grid = Grid()
    grid.add_car('X', 'H', 2, 3, 2)
    grid.print_grid()
    #grid.move('X', 3)
    # grid.print_grid()
    # print(grid.possible_moves('X'))
    grid.random_algorythm()
