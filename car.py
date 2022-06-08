class Car():
    def __init__(self, name, orientation, x, y, length, grid_size) -> None:
        self._name = name
        self._orientation = orientation
        self._x = x
        self._y = y
        self._length = length
        # give the columns of the grid for the win condition
        self._grid_size = grid_size

    # gives the coordinates of the car as a list of (x, y)
    def coordinates(self):
        coordinate = [self._x, self._y]

        return coordinate

    def set_coordinates(self, new_x, new_y):
        self._x = new_x
        self._y = new_y

    def can_move_to(self, x, y):
        """ Check whether the car can move to the given coordinates. """

        if self._orientation == 'H':

            if not self._y == y:
                return False

        # If the car is vertical
        if not self._x == x:
            return False

        pass
# # possibly a subclass for a red car is quicker as we only loop over 1 car rather than all cars
# # depends on our grid model for checking the win condition
# class RedCar(Car):
#     def __init__(self, name, orientation, col, y, length, grid_size) -> None:
#         super().__init__(name, orientation, col, y, length, grid_size)
