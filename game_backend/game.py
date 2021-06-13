from .map_generator import Generator
from .player import Player
from .monsters import Monsters


class Game:
    def __init__(self, width=53, height=28,number_monsters=20,number_bananas=20,number_hearts=10):
        self._generator = Generator(width=width, height=height)
        self._generator.gen_level()
        self._generator.gen_tiles_level()
        self._map = self._generator.tiles_level

        self._player1 = Player(symbol=chr(0x1F435))
        self._player1.initPos( self._map )
        self._player2= Player(symbol=chr(0x1F438))
        self._player2.initPos( self._map )
        self.height = self._generator.height
        self.width = self._generator.width
        #monstres
        self._Monsters = self._generator.gen_monster(number_monsters,self)
        self._Items= self._generator.gen_item(number_bananas,number_hearts,self)

    def getMap(self):
        return self._map

    def move_1(self, dx, dy):
        return self._player1.move(dx, dy, self._map)

    def move_2(self, dx, dy):
        return self._player2.move(dx, dy, self._map)


    def update_monster(self):
        datas=[]
        monsters = self._Monsters
        for i in range(len(monsters)):
            monster=monsters[i]
            data=monster.move_monsters(self._map)
            datas.append(data)
        return datas

    def players_shock(self,player,dx,dy):
        if player== self._player1:
            data2=self._player2.move(dx,dy,self._map)
            data1=self._player1.move(-dx,-dy,self._map)
        else:
            data1=self._player1.move(dx,dy,self._map)
            data2=self._player2.move(-dx,-dy,self._map)

        return [data1[0], data2[0]]


    """ def get_player_health(self) :
        return self._player.get_health_points()
    
    def conflict(self):
        conflicts=[]
        for monster in self._Monsters:
            if  (monster._x,monster._y) ==(self._player._x,self._player._y):
                print("conflit!!!")
                conflicts.append(monster)
        return conflicts
    def get_monsters(self):
        return self._Monsters"""