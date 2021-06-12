import random

class Monsters:

    def __init__(self, symbol = 'x'):
        self._symbol = symbol
        self._x = None
        self._y = None
        self._dx = None
        self._dy = None
        self.step_on = chr(0x1F532)	
        self.previous_step_on = chr(0x1F532)	

    def initPos(self, _map,  height, width, player):
        '''
        Position initiale du monstre qui doit être dans la grille hors des murs
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
        _map[self._y][self._x] = chr(0x1F532)
    
    def move_monsters(self, _map):
        move_allowed = False
        while not(move_allowed):
            #choix des dx et dy
            mouvement_choice = random.randint(1,4)

            if mouvement_choice==1 :
                self._dx = -1
                self._dy=0
            if mouvement_choice==2 :
                self._dx = 1
                self._dy=0
            if mouvement_choice==3:
                self._dx = 0
                self._dy=-1
            if mouvement_choice==4: 
                self._dx=0
                self._dy =1

            new_y = self._y + self._dy
            new_x = self._x + self._dx

            #test si on peut bien déplacer le monstre dans cette direction
            if _map[new_y][new_x] == chr(0x1F532):
                move_allowed =True
                _map[new_y][new_x] = chr(0x1F47B)
                _map[self._y][self._x] = chr(0x1F532)	
                data = [{"i": f"{self._y}", "j":f"{self._x}", "content":chr(0x1F532)	}, {"i": f"{new_y}", "j":f"{new_x}", "content":chr(0x1F47B)}]
                self._x = new_x
                self._y = new_y

        return data
       
    def get_pos(self):
        return (self._x,self._y)