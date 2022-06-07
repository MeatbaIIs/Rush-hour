from car import Car
#from loader import loader


class Grid():
    def __init__(self, size=7):
        self._grid = []
        for i in range(size):
            self._grid.append(size * ['*'])
        self._cars = {}
        self._size = size

    def add_car(self, name, orientation, col, row, length):
        car = Car(name, orientation, col, row, length, self._size)
        self._cars[name] = car
        for i in range(length):
            if orientation == 'H':
                self._grid[row][col + i] = name
            elif orientation == 'V':
                self._grid[row + i][col] = name

    def move(self, name, distance):
        car = self._cars[name]
        coor = car.coordinates()
        orientation = car._orientation
        length = car._length

        col = coor[0]
        row = coor[1]

        for i in range(length):
            if orientation == 'H':
                self._grid[row][col + i] = '*'
                self._grid[row][col + i + distance] = name

            if orientation == 'V':
                self._grid[row + i][col] = '*'
                self._grid[row + i + distance][col] = name


        if name == 'X':
            car.win()

    def possible_cars(self, x, y):
        """ Generates a set of cars that could move to given coordinates. """
        possible_cars = set()
        for car in self._cars:
            if car.can_move_to(x, y):
                possible_cars.add(car)

        return possible_cars

    def possible_moves(self, name):
        moves = set()
        car = self._cars[name]
        orientation = car._orientation
        length = car._length
        coor = car.coordinates()

        col = coor[0]
        row = coor[1]

        if orientation == 'H':
            distance = 0
            for i in range(col + length, self._size):
                if self._grid[i][col] == '*':
                    distance += 1
                    moves.add(distance)
                else:
                    break

            distance = 0
            for i in range(col, -1, -1):
                if self._grid[i][col] == '*':
                    distance -= 1
                    moves.add(distance)
                else:
                    break

        elif orientation == 'V':
            distance = 0
            for i in range(row + length, self._size):
                print(i)
                if self._grid[row][i] == '*':
                    distance += 1
                    moves.add(distance)
                else:
                    break

            distance = 0

            for i in range(row, -1, -1):
                if self._grid[row][i] == '*':
                    distance -= 1
                    moves.add(distance)
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
        for row in self._grid:
            print(''.join(row))


if __name__ == '__main__':
    grid = Grid()
    grid.add_car('X', 'V', 0, 3, 2)
    grid.print_grid()
    #grid.move('X', 3)
    # grid.print_grid()
    print(grid.possible_moves('X'))
