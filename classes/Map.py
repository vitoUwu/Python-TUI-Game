import random
import opensimplex
from sprites import *
from classes.Event import event

def identify(entity) -> None:
  return entity.__class__.__name__ + f'({entity.x}, {entity.y})'

class Map():
  def __init__(self, rows: int = 100, cols: int = 100, render_distance: int = 5) -> None:
    self.rows = rows
    self.cols = cols
    self.entities = []
    self.ground_entities = []
    self.render_distance = render_distance
    self.seed = random.randint(0, 1000000)
    self.ground = [[None for _ in range(cols)] for _ in range(rows)]
    self.rendered_ground = 0
    self.player = None

  def render(self) -> str:
    render = []
    if self.player is None:
      self.player = self.get_entity('Player')

    has_coins = self.get_entity('Coin')
    has_door = self.get_entity('Door')
    if not has_coins and not has_door:
      event.trigger('new_map_door_spawn')

    cell_count = self.render_distance * 2 + 1
    renderizable_area = [[empty_cell for _ in range(cell_count)] for _ in range(cell_count)]
    for x in range(max(0, self.player.x - self.render_distance), min(self.cols, self.player.x + self.render_distance)):
      for y in range(max(0, self.player.y - self.render_distance), min(self.rows, self.player.y + self.render_distance)):
        render_x = x - self.player.x + self.render_distance
        render_y = y - self.player.y + self.render_distance
        if x == 0 or y == 0 or x == self.cols - 1 or y == self.rows - 1:
          renderizable_area[render_y][render_x] = wall_cell
        else:
          if self.ground[y][x] is not None:
            renderizable_area[render_y][render_x] = self.ground[y][x]
          else:
            entity = self.entity_at(x, y)
            if entity is not None:
              renderizable_area[render_y][render_x] = entity.sprite
            else:
              self.ground[y][x] = grounds[int(opensimplex.noise2(x, y) * 10) % len(grounds)]
              self.rendered_ground += 1
              renderizable_area[render_y][render_x] = self.ground[y][x]

    renderizable_area[self.render_distance][self.render_distance] = player_cell

    for entity in self.entities:
      if entity.__class__.__name__ == 'Player':
        render.append(identify(entity))
      if entity.__class__.__name__ == 'Door':
        render.append(identify(entity))

    render.append(f'Grounds created: {self.rendered_ground}/{self.rows * self.cols}')
    render.append(f'Entities: {len(self.entities) + len(self.ground_entities)}')

    renderized_area = ''
    for row in renderizable_area:
      renderized_area += ''.join(row) + '\n'
    
    render.append(renderized_area)
    render = '\n'.join(render)
    return render

  def get_entity(self, class_name: str) -> object:
    for entity in self.entities:
      if entity.__class__.__name__ == class_name:
        return entity
    for entity in self.ground_entities:
      if entity.__class__.__name__ == class_name:
        return entity
    return None

  def get_cell(self, x, y) -> str:
    if x == 0 or y == 0 or x == self.cols - 1 or y == self.rows - 1:
      return wall_cell
    entity = self.entity_at(x, y)
    if entity is not None:
      return entity.sprite
    return empty_cell

  def spawn(self, entity, fixed: bool = False) -> None:
    if fixed:
      self.ground_entities.append(entity)
      self.ground[entity.y][entity.x] = entity.sprite
    else:
      self.entities.append(entity)

  def destroy(self, entity, fixed: bool = False) -> None:
    if fixed:
      self.ground_entities.remove(entity)
      self.ground[entity.y][entity.x] = None
    else:
      self.entities.remove(entity)

  def entity_at(self, x, y) -> object:
    for entity in self.entities:
      if entity.x == x and entity.y == y:
        return entity
    for entity in self.ground_entities:
      if entity.x == x and entity.y == y:
        return entity
    return None
