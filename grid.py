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
        """Move a random car randomly and check for the win condition"""
        random_car = random.choice(list(self._cars.keys()))
        while not self.win():
            # get the possible moves and pick a random one
            moves = self.possible_moves(random_car)
            if moves:
                random_move = random.choice(moves)
                self.move(random_car, random_move)
                self.print_grid()
            # pick a new random car
            random_car = random.choice(list(self._cars.keys()))
        print("Yay,solved")


    def move(self, name, distance):
        """Move a car a set distance, does not check if its a possible move"""
        print(name)
        car = self._cars[name]
        coor = car.coordinates()
        orientation = car._orientation
        length = car._length


        x = coor[0]
        y = coor[1]

        if orientation == 'H':
            new_x = x + distance
            # empty the previous space of the car
            self._grid[y][x:x+length] = length * ["*"]
            # fill the new space of the car
            self._grid[y][new_x:new_x +length] = length * [name]
            # aanpassen naar een functie
            car.set_coordinates(new_x, y)

        elif orientation == 'V':
            new_y = y + distance
            for i in range(length):
                self._grid[y+i][x] = "*"
            for i in range(length):
                self._grid[new_y + i][x] = name
            # aanpassen naar een functie
            car.set_coordinates(x, new_y)
            #car._y = new_y

    def possible_cars(self, x, y):
        """ Generates a set of cars that could move to given coordinates. """
        possible_cars = set()
        for car in self._cars:
            if car.can_move_to(x, y):
                possible_cars.add(car)

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
            for i in range(x + 1, self._size - length + 1):
                space = True
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
            for i in range(x - 1, -1, -1):
                if self._grid[y][i] == '*' or self._grid[y][i] == name:
                    distance -= 1
                    moves.append(distance)
                else:
                    break

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
        print()

    def win(self):
        """Check if the red car can reach the end"""
        x, y = self._cars['X'].coordinates()
        # check whether every space before the red car is empty
        if self._grid[y][x + 2:self._size] == (self._size - x - 2) * ["*"]:
            return True
        return False

if __name__ == '__main__':
    grid = Grid()
    grid.add_car('X', 'H', 2, 3, 2)
    grid.print_grid()
    #grid.move('X', 3)
    # grid.print_grid()
    #print(grid.possible_moves('X'))
    grid.random_algorythm()
