"""
Anneloes'en Duncans wondercode
"""
import copy
from matplotlib.pyplot import cla
from ..classes.grid import Grid
from helpers import loader

class DepthFirst:
    def __init__(self, data_file) -> None:
        grid = loader(data_file)

        self._grid = grid
        # make a copy of the total displacement of every car in the grid
        # the list is [0,0,0,0,0,0, etc...] at the start and is alphabetical ie A=0, B = 1 and X is the last car
        self._movement_nodes = [grid._total_moves[:]]
        self._current_node = grid._total_moves[:]

        # last number of the total movements is the number of steps
        self._N_steps = self._current_node[-1]

        # keep remembering the previous node
        self._previous_node = self._current_node

        # remember the exact moves that have been done for the current node
        # dit is bijvoorbeeld [A 1, X -2, B 3, G 1, H -1, etc...]
        self._done_movements = []


    # """
    # pseudocode for the steps
    # """"
    # def step(self):
    #     moves = self.grid.possible_moves()

    #     # berekent voor alle mogelijke moves wat de total moves zouden zijn als we naar die node zouden bewegen
    #     for move in moves:
    #         # de move functie moet aangepast worden zodat we vanuit bijvoorbeeld auto B die beweegt in +3
    #         # dat de lijst total moves gekopieerd wordt en de 2 plek +3 wordt
    #         current_node + move

    #         # sla op wat de moves zijn in alle moves zodat we niet dezelfde configuratie hebben
    #         movement_nodes.append(node)
        
    #     # bekijk eerst of er moves mogelijks zijn
    #     if len(moves) != 0:
    #         # update de vorige node naar huidige voordat we bewegen
    #         self.previous_node = self.current_node
    #         # beweeg de huidige node naar de volgende
    #         self._current_node =  self.grid.move(random.choice van moves)
        
    #         moves.remove(move)
        
    #         # we kijken of de nieuwe huidige node niet al bestaat in ons algoritmes geheugen
    #         if self._current_node in self.movement_nodes:
    #             # we voegen de huidige node niet toe aan de lijst omdat we een stap terug moeten

    #             # we gaan voor de huidige node 1 stap terug die we halen uit de gedane movement lijst
    #             self.current_node.move(laatste element in de gedane stappen)
    #             # we zetten de previous node 2 stappen terug uit de exacte  movement lijst
    #             self.previous_node.move(laatste en enalaatste element in de gedane stappen)
                
    #         # anders slaan we de node wel op
    #         else:
    #             self._movement_nodes.append(self._current_node)
    #     # als alle moves al eerder voorkwamen of er geen moves mogelijk zijn gaan we ook naar de vorige node
    #     else:
    #         # we gaan voor de huidige node 1 stap terug die we halen uit de gedane movement lijst
    #         self.current_node.move(laatste element in de gedane stappen)
    #         # we zetten de previous node 2 stappen terug uit de exacte  movement lijst
    #         self.previous_node.move(laatste en enalaatste element in de gedane stappen)

              
    
    def run(self):
        # loopt tot de grid opgelost is
        while not win:
            self.step()
    

algorithm = DepthFirst("data/Rushhour6x6_1.csv")
algorithm.step()