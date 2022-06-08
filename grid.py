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

    # geeft de buren van dingen op bepaald x,y coordinaat
    def neighbours(self, x, y):
        coordinate = self._grid[y][x]
        neighbours = []

        for i in [-1, 1]:
            neighbour = self._grid[y + i][x]
            neighbours.append([neighbour, (y + i, x)])
        for j in [-1, 1]:
            neighbour = self._grid[y][x + j]
            neighbours.append([neighbour, (y, x + j)])

        print(f"{coordinate} is op {x, y} met buren, {neighbours}")
        return neighbours

    def give_empties(self):
        list_of_empties = []

        for y in range(self._size):
            for x in range(self._size):
                element = self._grid[y][x]
                if element == "*":
                    list_of_empties.append((y, x))
        print(list_of_empties)
        return list_of_empties

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
