from sprites import *
from classes.Event import event

def identify(entity) -> None:
  return entity.__class__.__name__ + f'({entity.x}, {entity.y})'

class Map():
  def __init__(self, rows, cols) -> None:
    self.rows = rows
    self.cols = cols
    self.entities = []

  def render(self) -> None:
    player = self.get_entity('Player')
    area = [[empty_cell for _ in range(self.cols)] for _ in range(self.rows)]

    has_coins = self.get_entity('Coin')
    has_door = self.get_entity('Door')
    if not has_coins and not has_door:
      event.trigger('new_map_door_spawn')

    for entity in self.entities:
      if entity.x == player.x and entity.y == player.y and entity.__class__.__name__ != 'Player':
        area[entity.y][entity.x] = player.sprite
      else:
        if entity.__class__.__name__ == 'Player':
          print(identify(entity))
        area[entity.y][entity.x] = entity.sprite

    cell_length = len(area[0][0])
    print(' ' + '-' * self.cols * cell_length)
    for row in area:
      print('|' + ''.join(row) + '|')
    print(' ' + '-' * self.cols * cell_length)

  def get_entity(self, class_name: str) -> object:
    for entity in self.entities:
      if entity.__class__.__name__ == class_name:
        return entity
    return None

  def get_empty_coords(self) -> list[tuple]:
    coords = []
    for y in range(self.rows):
      for x in range(self.cols):
        if self.entity_at(x, y) is None:
          coords.append((x, y))
    return coords

  def spawn(self, entity) -> None:
    self.entities.append(entity)

  def destroy(self, entity) -> None:
    self.entities.remove(entity)

  def entity_at(self, x, y) -> object:
    for entity in self.entities:
      if entity.x == x and entity.y == y:
        return entity
    return None
