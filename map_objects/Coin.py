from classes.Map import Map
from classes.Player import Player
from sprites import *
from classes.Map_Object import Map_Object

class Coin(Map_Object):
  def __init__(self, map: Map):
    super().__init__('Coin', coin_cell, 'collectable', map, False)
    self.value = 1
    self.sprite = coin_cell
  
  def collect(self, player: Player) -> None:
    player.coins += self.value
    if player.coins > player.high_score:
      player.high_score = player.coins
      open('high_score.txt', 'w').write(str(player.coins))
    self.map.destroy(self, True)