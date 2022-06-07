class Car():
    def __init__(self, name, orientation, col, row, length, grid_size) -> None:
        self._name = name
        self._orientation = orientation
        self._col = col
        self._row = row
        self._length = length
        # give the columns of the grid for the win condition
        self._grid_size = grid_size

    # gives the coordinates of the car as a list of (x, y)
    def coordinates(self):
        coordinate = [self._col, self._row]

        return coordinate

    # returns true if the red car is over the finish line
    def win(self):
        # red car is denoted by X
        if self._name == "X":
            if self._col == self._grid_size - 1:
                return True
            else:
                return False
        else:
            return False

    def can_move_to(self, x, y):
        """ Check whether the car can move to the given coordinates. """

        if self._orientation == 'H':

            if not self._row == y:
                return False

        # If the car is vertical
        if not self._col == x:
            return False

        pass
# # possibly a subclass for a red car is quicker as we only loop over 1 car rather than all cars
# # depends on our grid model for checking the win condition
# class RedCar(Car):
#     def __init__(self, name, orientation, col, row, length, grid_size) -> None:
#         super().__init__(name, orientation, col, row, length, grid_size)
