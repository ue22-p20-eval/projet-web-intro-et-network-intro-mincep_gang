import random

class Player:
    def __init__(self, symbol="@"):
        self._symbol = symbol
        self._x = None
        self._y = None
        self.health_points=100

    def initPos(self, _map):
        n_row = len(_map)
        #n_col = len(_map[0])

        y_init = n_row//2
        found = False
        while found is False:
            y_init += 1
            for i,c in enumerate(_map[y_init]):
                if c == ".":
                    x_init = i
                    found = True
                    break

        self._x = x_init
        self._y = y_init

        _map[self._y][self._x] = self._symbol

    def move(self, dx, dy, map):
        new_x = self._x + dx
        new_y = self._y + dy
        hp_loss=0

        if map[new_y][new_x] == "." or map[new_y][new_x] == "x" :
            if map[new_y][new_x] == "x":            #si le joueur est sur un monstre, il passe quand même mais perd de la vie
                hp_loss= random.randint(10,20)
                self.health_points = max(0,self.health_points - hp_loss)
            ret =True
            map[new_y][new_x] = self._symbol
            map[self._y][self._x] = "."
            data = [{"i": f"{self._y}", "j":f"{self._x}", "content":"."}, {"i": f"{new_y}", "j":f"{new_x}", "content":self._symbol}]
            self._x = new_x
            self._y = new_y
        else:
            ret = False
            data = []
        
        return data, ret, hp_loss

    def get_health_points(self) :
        return self.health_points