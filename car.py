class Car():
    def __init__(self, name, orientation, col, row, length) -> None:
        self._name = name
        self._orientation = orientation
        self._col = col
        self._row = row
        self._length = length

    # gives the coordinates of the car as a list of (x, y)
    def coordinates(self):
        coordinate = [self._row, self._col]

        return coordinate
    
    # returns true if the red car is over the finish line
    def win(self):
        # red car is denoted by X
        if self._name == "X":
            # currently do it like this, but the last column needs to be added from the grid initialization
            # either by a super from the grid, or by giving the lenght of the grid as initialization variable
            self._win_coordinates = 6 # grid._columns
            if self._col == self._win_coordinates:
                return True
            else:
                return False
        else:
            return False

# # possibly a subclass for a red car is quicker as we only loop over 1 car rather than all cars  
# # depends on our grid model for checking the win condition
# class RedCar(Car):
#     def __init__(self, name, orientation, col, row, length) -> None:
#         super().__init__(name, orientation, col, row, length)
