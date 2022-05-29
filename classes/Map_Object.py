from random import randint
from classes.Map import Map

class Map_Object():
  def __init__(self, name: str, sprite: str, item_type: str, map: Map, has_collision: bool = True) -> None:
    self.name = name
    self.sprite = sprite
    self.type = item_type
    self.has_collision = has_collision
    self.map = map
    self.x = 0
    self.y = 0

  def spawn(self) -> None:
    empty_coords = self.map.get_empty_coords()
    if not empty_coords:
      return
    self.x, self.y = empty_coords[randint(0, len(empty_coords) - 1)]
    self.map.spawn(self)