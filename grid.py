from car import Car
#from loader import loader


class Grid():
    def __init__(self, size=7):
        self._grid = []
        for i in range(size):
            self._grid.append(size * ['*'])
        self._cars = {}
        self._size = size

    def add_car(self, name, orientation, x, y, length):
        car = Car(name, orientation, x, y, length, self._size)
        self._cars[name] = car
        for i in range(length):
            if orientation == 'H':
                self._grid[y][x + i] = name
            elif orientation == 'V':
                self._grid[y + i][x] = name

    def move(self, name, distance):
        car = self._cars[name]
        coor = car.coordinates()
        orientation = car._orientation
        length = car._length

        x = coor[0]
        y = coor[1]

        for i in range(length):
            if orientation == 'H':
                self._grid[y][x + i] = '*'
                self._grid[y][x + i + distance] = name

            if orientation == 'V':
                self._grid[y + i][x] = '*'
                self._grid[y + i + distance][x] = name


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

        x = coor[0]
        y = coor[1]

        if orientation == 'H':
            distance = 0
            for i in range(x + length, self._size):
                if self._grid[y][i] == '*':
                    distance += 1
                    moves.add(distance)
                else:
                    break

            distance = 0
            for i in range(x - 1, -1, -1):
                if self._grid[y][i] == '*':
                    distance -= 1
                    moves.add(distance)
                else:
                    break

        elif orientation == 'V':
            distance = 0
            for i in range(y + length, self._size):
                if self._grid[i][x] == '*':
                    distance += 1
                    moves.add(distance)
                else:
                    break

            distance = 0
            for i in range(y - 1, -1, -1):
                if self._grid[i][x] == '*':
                    distance -= 1
                    moves.add(distance)
                else:
                    break

        return moves

    # gives the cars that can move to a certain sport given their orientation and that
    # they are the first car towards the point. The point must be * ofcourse
    def movable_neighbours(self, x, y):
        coordinate = self._grid[y][x]
        movable_neighbours = []
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
                    movable_neighbours.append([car._name, (x, y + i)])
                # doesnt add any cars if there is a horizontal car blocking the way
                break
            

        for i in range(1, self._size):
            if y - i < 0:
                break
            elif self._grid[y - i][x] != "*":
                neighbour = self._grid[y - i][x]
                if self._cars[neighbour]._orientation == "V":
                    car = self._cars[neighbour]
                    movable_neighbours.append([car._name, (x, y - i)])
                break
            

        for j in range(1, self._size):
            if x + j >= self._size - 1:
                break
            elif self._grid[y][x + j] != "*":
                neighbour = self._grid[y][x + j]
                if self._cars[neighbour]._orientation == "H":
                    car = self._cars[neighbour]
                    movable_neighbours.append([car._name, (x + j, y)])
                break
            
        
        for j in range(1, self._size):
            if x - j < 0:
                break
            elif self._grid[y][x - j] != "*":
                neighbour = self._grid[y][x - j]
                if self._cars[neighbour]._orientation == "H":
                    car = self._cars[neighbour]
                    movable_neighbours.append([car._name, (x - j, y)])
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

        print(list_of_empties)
        return list_of_empties

    def give_all_possible_moves(self):
        empties = self.give_empties()
        total_coords = []

        for element in empties:
            coords = self.movable_neighbours(element[0], element[1])
            if len(coords) != 0:
                total_coords.append(coords)
        
        print(total_coords)


    def print_grid(self):
        for y in self._grid:
            print(''.join(y))


if __name__ == '__main__':
    grid = Grid()
    grid.add_car('X', 'H', 2, 3, 2)
    grid.print_grid()
    #grid.move('X', 3)
    # grid.print_grid()
    # print(grid.possible_moves('X'))
