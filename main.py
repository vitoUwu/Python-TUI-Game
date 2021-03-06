import os
import keyboard
from classes.Map import Map
from classes.Player import Player
from classes.Event import event
from map_objects.Door import Door
from map_objects.Coin import Coin

try:
  open('high_score.txt', 'x').close()
  open('high_score.txt', 'w').write('0')
except FileExistsError:
  pass

rows, cols = (100, 100)
os.system('cls||clear')
print('Creating Map...')
map = Map(rows, cols, 15)
print(f'Size: {rows}x{cols}\nSeed: {map.seed}\nRender Distance: {map.render_distance}')
player = Player(map)

def spawn_coins():
  for _ in range(1000):
    coin = Coin(map)
    coin.spawn()
  update()

def update():
  render = map.render()
  os.system('cls||clear')
  print(f'Size: {rows}x{cols}\nSeed: {map.seed}\nRender Distance: {map.render_distance} -> {map.render_distance * 2}x{map.render_distance * 2}')
  print(render)
  print(f'Coins: {player.coins}')
  print(f'High Score: {player.high_score}')
  print('Use the arrow keys to move. Press ESC to quit.')

def on_press(key: keyboard.KeyboardEvent):
  py, px = player.coords()
  if(key.name == 'up' and py > 0):
    player.move(0, -1)
  if(key.name == 'down' and py < rows - 1):
    player.move(0, 1)
  if(key.name == 'left' and px > 0):
    player.move(-1, 0)
  if(key.name == 'right' and px < cols - 1):
    player.move(1, 0)

def spawn_door():
  door = Door(map)
  door.spawn()

player.spawn()
spawn_coins()
update()

keyboard.on_press(on_press)
event.bind('update', update)
event.bind('new_map_door_open', spawn_coins)
event.bind('new_map_door_spawn', spawn_door)

try:
  while keyboard.wait('esc'): 
    pass
except KeyboardInterrupt:
  pass