from .map_generator import Generator
from .player import Player
from .monsters import Monsters


class Game:
    def __init__(self, width=96, height=32):
        self._generator = Generator(width=width, height=height)
        self._generator.gen_level()
        self._generator.gen_tiles_level()
        self._map = self._generator.tiles_level

        self._player = Player()
        self._player.initPos( self._map )
        self.height = self._generator.height
        self.width = self._generator.width
        #monstres
        self._Monsters = self._generator.gen_monster(self)

    def getMap(self):
        return self._map

    def move(self, dx, dy):
        return self._player.move(dx, dy, self._map)

    def update_monster(self):
        monster = self._Monster
        data = monster.move_monsters(self._map)
        return data