import random

class Monsters:

    def __init__(self, symbol = 'x'):
        self._symbol = symbol
        self._x = None
        self._y = None
        self._dx = None
        self._dy = None
        self.step_on = "."
        self.previous_step_on = "."

    def initPos(self, _map,  height, width, player):
        '''
        Position initiale du monstre qui doit être dans la grille hors des murs
        '''
        found = False
        while found is False:
            y_init = random.randint(0, height-1)
            x_init = random.randint(0, int(width-1))
            if _map[y_init][x_init] == "." :
                found = True
                break
        self._x = x_init
        self._y = y_init
        _map[self._y][self._x] = 'x'
    
    def move_monsters(self, _map):
        move_allowed = False
        while not(move_allowed):
            #choix des dx et dy
            dx = random()
            dy = random()
            if dx < 0.5 :
                self._dx = -1
            elif dx > 0.5 :
                self._dx = 1
            else :
                self._dx = 0
            if dy < 0.5 :
                self._dy = -1
            elif dy > 0.5 :
                self._dy = 1
            else :
                self._dy = 0
            print(dx, dy)

            new_y = self._y + self._dy
            new_x = self._x + self._dx

            #test si on peut bien déplacer le monstre dans cette direction
            if map[new_y][new_x] == "." or map[new_y][new_x] == "@" :
                move_allowed =True
                map[new_y][new_x] = self._symbol
                map[self._y][self._x] = "."
                data = [{"i": f"{self._y}", "j":f"{self._x}", "content":"."}, {"i": f"{new_y}", "j":f"{new_x}", "content":self._symbol}]
                self._x = new_x
                self._y = new_y
            

        return data
       
