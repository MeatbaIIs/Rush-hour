from car import Car
#from loader import loader

class Grid():
    def __init__(self, size):
        self._grid = []
        for i in range(size):
            self._grid.append(size * ['*'])
        self._cars = {}
        self._size = size
        # is true when red car is at finish from move
        self._win = False

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
            self._win = car.win()

    def check_empties(self):
        list_of_empties = []
        for y in range(self._size):
            for x in range(self._size):
                element = self._grid[y][x] 
                if element == "*":
                    # print(f"{x, y} are coordinates for * ")
                    list_of_empties.append(element)
        return list_of_empties

    

    def print_grid(self):
        for row in self._grid:
            print(''.join(row))


if __name__ == '__main__':
    grid = Grid()
    # grid.add_car('X', 'V', 3, 0, 2)
    # grid.print_grid()
