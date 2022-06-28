"""
This class keeps track of all the variables concerning a specific car on the grid
"""

class Car():
    def __init__(self, name, orientation, x, y, length, grid_size):
        self._name = name
        self._orientation = orientation
        self._x = x
        self._initial_x = x
        self._y = y
        self._initial_y = y
        self._length = length

    def set_coordinates(self, new_x, new_y):
        self._x = new_x
        self._y = new_y

    def get_x(self):
        return self._x

    def get_initial_x(self):
        return self._initial_x

    def get_y(self):
        return self._y

    def get_initial_y(self):
        return self._initial_y

    def set_x(self, x):
        self._x = x

    def set_y(self, y):
        self._y = y

    def get_orientation(self):
        return self._orientation

    def get_length(self):
        return self._length
