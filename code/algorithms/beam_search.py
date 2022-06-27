from .breadth_first import BreadthFirst
from ..helpers import next_total_movements


class BeamSearch(BreadthFirst):
    def __init__(self, grid):
        """
        A Beam Search algorithm that runs like breadth first, only instead of saving the total_movements of all possible next steps, it only saves that of (one of) the furthest.
        """
        super().__init__(grid)

    def get_next_total_movements(self, total_movements):
        """
        Overwrite the Breadth First get_next_total_movements from all possible to only the one with (one of) the furthest step(s).
        """
        return next_total_movements(self._grid, total_movements, furthest=True)
