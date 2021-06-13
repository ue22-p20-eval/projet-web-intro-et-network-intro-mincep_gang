import random

class Player:
    def __init__(self, symbol="@"):
        self._symbol = symbol
        self._x = None
        self._y = None
        self.health_points=20
        self.bananas=0

    def initPos(self, _map):
        n_row = len(_map)
        #n_col = len(_map[0])

        y_init = n_row//2
        found = False
        while found is False:
            y_init += 1
            for i,c in enumerate(_map[y_init]):
                if c == chr(0x1F532)	:
                    x_init = i
                    found = True
                    break

        self._x = x_init
        self._y = y_init

        _map[self._y][self._x] = self._symbol

    def move(self, dx, dy, map):
        new_x = self._x + dx
        new_y = self._y + dy
        data = []
        ret=False
        hp_loss=0
        hp_gain=0
        banana_gain=0
        conflict=False

        if  map[new_y][new_x] == chr(0x1F435) or map[new_y][new_x] == chr(0x1F438):   #si le joueur rencontre J1 ou J2
                conflict=True
        elif map[new_y][new_x] != chr(0x1F4E6)  :        #tant que ce n'est pas un mur  
            ret =True
            if  map[new_y][new_x] == chr(0x1F47B):   #si le joueur est sur un monstre, il passe quand même mais perd de la vie
                hp_loss=1
                self.health_points=max(0, self.health_points - hp_loss)
            if map[new_y][new_x] == chr(0x1F34C):   #banane
                self.bananas+=1
                banana_gain=1
            if map[new_y][new_x] == chr(0x1F496):  #coeur
                hp_gain=1
                self.health_points=min(20, self.health_points + hp_gain)
            map[new_y][new_x] = self._symbol
            map[self._y][self._x] = chr(0x1F532)  #sol	
            data = [{"i": f"{self._y}", "j":f"{self._x}", "content":chr(0x1F532)	}, {"i": f"{new_y}", "j":f"{new_x}", "content":self._symbol}]
            self._x = new_x
            self._y = new_y
        
        return data, ret, hp_loss, hp_gain, banana_gain, conflict
