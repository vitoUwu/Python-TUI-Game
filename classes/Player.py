from random import choice
from classes.Map import Map
from classes.Event import event
from sprites import *

class Player():
  def __init__(self, map: Map) -> None:
    self.map = map
    self.x = 0
    self.y = 0
    self.coins = 0
    self.sprite = player_cell
    self.high_score = int(open('high_score.txt', 'r').read())

  def spawn(self) -> None:
    self.x, self.y = choice(self.map.get_empty_coords())
    self.map.spawn(self)

  def coords(self) -> tuple:
    return self.y, self.x

  def move(self, x: int, y: int) -> None:
    self.colide(self.map.entity_at(self.x + x, self.y + y))
    self.x += x
    self.y += y
    event.trigger('update')

  def colide(self, entity: object) -> None:
    if entity is None:
      return
    if entity.type == 'collectable':
      entity.collect(self)
    if entity.type == 'door':
      entity.open()