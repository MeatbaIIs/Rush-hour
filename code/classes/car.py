class Car():
    def __init__(self, name, orientation, x, y, length, grid_size):
        self._name = name
        self._orientation = orientation
        self._x = x
        self._y = y
        self._length = length
        # give the columns of the grid for the win condition
        self._grid_size = grid_size

    def coordinates(self):
        """ gives the coordinates of the car as a list of (x, y) """
        coordinate = [self._x, self._y]

        return coordinate

    def set_coordinates(self, new_x, new_y):
        self._x = new_x
        self._y = new_y

    def get_x(self):
        return self._x

    def get_y(self):
        return self._y

    def set_x(self, x):
        self._x = x

    def set_y(self, y):
        self._y = y

    def get_orientation(self):
        return self._orientation

    def get_length(self):
        return self._length
