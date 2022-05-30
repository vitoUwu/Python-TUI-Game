from random import randint
from classes.Map import Map
from sprites import *

def rand_coord(map: Map) -> tuple:
  return (randint(0, map.cols - 1), randint(0, map.rows - 1))

class Map_Object():
  def __init__(self, name: str, sprite: str, item_type: str, map: Map, has_collision: bool = True) -> None:
    self.name = name
    self.sprite = sprite
    self.type = item_type
    self.has_collision = has_collision
    self.map = map
    self.x = 0
    self.y = 0
    self.spawn_call_count = 0

  def spawn(self) -> None:
    if self.spawn_call_count == 10:
      return
    self.x, self.y = rand_coord(self.map)
    if self.map.get_cell(self.x, self.y) != empty_cell:
      self.spawn_call_count += 1
      return self.spawn()
    self.map.spawn(self, True)

  def colide(self, entity: object) -> None:
    if entity is None:
      return
    if entity.type == 'collectable':
      entity.collect(self)
    if entity.type == 'door':
      entity.open()