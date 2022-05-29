from classes.Map import Map
from sprites import *
from classes.Map_Object import Map_Object
from classes.Event import event

class Door(Map_Object):
  def __init__(self, map: Map):
    super().__init__('new_map_door', door_cell, 'door', map, False)

  def open(self) -> None:
    self.map.destroy(self)
    event.trigger('new_map_door_open')