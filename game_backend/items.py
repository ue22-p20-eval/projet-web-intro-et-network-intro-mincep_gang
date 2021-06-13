import random

class Items:

    def __init__(self, symbol = '$'):
        self._symbol = symbol
        self._x = None
        self._y = None

    def initPos(self, _map,  height, width):
        '''
        Position initiale de l'item qui doit être dans la grille hors des murs
        '''
        found = False
        while found is False:
            y_init = random.randint(0, height-1)
            x_init = random.randint(0, int(width-1))
            if _map[y_init][x_init] == chr(0x1F532)	 :
                found = True
                break
        self._x = x_init
        self._y = y_init
        _map[self._y][self._x] = self._symbol