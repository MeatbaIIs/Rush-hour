from .breadth_first import BreadthFirst


class BeamSearch(BreadthFirst):
    def __init__(self, grid):
        """
        A Beam Search algorithm that runs like breadth first, only instead of saving the total_movements of all possible next steps, it only saves that of (one of) the furthest.
        """
        super().__init__(grid)

    def get_next_lists(self, last_list):
        """
        Overwrite the Breadth First get_next_total_movements from all possible to only the one with (one of) the furthest step(s).
        """
        return self._grid.furthest_next_lists(last_list)
