import pyglet

from pyglet import shapes
from ui import *
from models import *
import constants as const

window = pyglet.window.Window(1600, 900, vsync=True)
# создаем окно
game_width = 1100
game_height = 900
sidebar_width1 = 200
sidebar_width2 = 300
# размеры основного и бокового поля

bat = pyglet.graphics.Batch()
# объект пакетной отрисовки


# создание групп объектов по слоям наложения

game_area = shapes.Rectangle(0, 0, game_width, game_height, color=(40, 40, 40), batch=const.main_batch, group=  const.background_group)
sidebar1 = shapes.Rectangle(game_width, 0, sidebar_width1, game_height, color=(60, 60, 60), batch=const.main_batch, group= const.background_group)
sidebar2 = shapes.Rectangle(game_width + sidebar_width1, 0, sidebar_width2, game_height, color=(80, 80, 80), batch=const.main_batch, group= const.background_group)
# создание в окне основных полей

point_test = Point(100, 100, "point_test")

all_inputs = [
DesInput(1100, 650, 90, 40, '1x'),
DesInput(1210, 650, 90, 40, '1y'),
DesInput(1150, 600, 90, 40, 'speed1'),

DesInput(1100, 350, 90, 40, '2x'),
DesInput(1210, 350, 90, 40, '2y'),
DesInput(1150, 300, 90, 40, 'speed2'),

DesInput(1350,550,90,40,'point_x'),
DesInput(1460,550,90,40,'point_y'),
DesInput(1400,500,90,40,'point_name'),

DesInput(1400,350,90,40,'point_name_delete')

]
# набор полей ввода

buttons = [
   Button(1100, 700, 200, 50, (70, 70, 220), "Машина 1", lambda: car1.init(all_inputs), const.main_batch),
   Button(1100, 400, 200, 50, (220, 70, 70), "Машина 2", lambda: car2.init(all_inputs), const.main_batch),
   Button(1350,600,200, 50, (100, 170, 70), "Создать пункт", lambda : Point.create_point(all_inputs,const.main_batch), const.main_batch),
   Button(1350,400,200, 50, (100, 170, 70), "Удалить пункт", lambda: Point.delete_point(all_inputs), const.main_batch)
]
# набор кнопок

car1 = Car(1000,800, ('1x','1y','speed1'))
car2 = Car(100,700, ('2x','2y','speed2'))
# создание машин



@window.event
def on_text(text):
   for inp in all_inputs:
      inp.on_text(text)

@window.event
def on_key_press(symbol, modifiers):
   for inp in all_inputs:
      inp.on_key_press(symbol, modifiers)

@window.event
def on_draw():
   window.clear()
   const.main_batch.draw()
# отрисовка

@window.event
def on_mouse_press(x, y, button, modifiers):
   for but in buttons:
      if but.contains(x,y):
         but.func()
   for inp in all_inputs:
      inp.set_active(inp.check_hit(x, y)) # проверка сначала попадания в область поля ввода, затем передача T/F в активность поля

# обработка нажатия кнопки мыши


pyglet.app.run()