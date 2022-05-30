from random import choice, randint
from classes.Map import Map
from classes.Event import event
from sprites import *

def rand_coord(map: Map) -> tuple:
  return (randint(0, map.cols - 1), randint(0, map.rows - 1))

class Player():
  def __init__(self, map: Map) -> None:
    self.map = map
    self.x = 0
    self.y = 0
    self.coins = 0
    self.sprite = player_cell
    self.high_score = int(open('high_score.txt', 'r').read())

  def spawn(self) -> None:
    self.x, self.y = rand_coord(self.map)
    if self.map.get_cell(self.x, self.y) != empty_cell:
      return self.spawn()
    self.map.spawn(self)

  def coords(self) -> tuple:
    return self.y, self.x

  def move(self, x: int, y: int) -> None:
    if self.map.get_cell(self.x + x, self.y + y) == wall_cell:
      return
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