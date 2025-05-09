from pyglet.graphics import Group
import pyglet
import math
from pyglet import shapes


window = pyglet.window.Window(1600, 900, vsync=True)
# создаем окно
game_width = 1100
game_height = 900
sidebar_width1 = 200
sidebar_width2 = 300
# размеры основного и бокового поля

bat = pyglet.graphics.Batch()
# объект пакетной отрисовки

background_group = Group(0)
middle_group = Group(1)
foreground_group = Group(2)
# создание групп объектов по слоям наложения

game_area = shapes.Rectangle(0, 0, game_width, game_height, color=(40, 40, 40), batch=bat, group= background_group)
sidebar1 = shapes.Rectangle(game_width, 0, sidebar_width1, game_height, color=(60, 60, 60), batch=bat, group= background_group)
sidebar2 = shapes.Rectangle(game_width + sidebar_width1, 0, sidebar_width2, game_height, color=(80, 80, 80), batch=bat, group= background_group)
# создание в окне основных полей


class Car:
   def __init__(self, x, y,ind = (0,0,0)):
      self.des_x = None # координата x точки назначения
      self.des_y = None # координата y точки назначения
      self.image = pyglet.image.load('sourse/car.png') # загрузка изображения
      self.image.anchor_x = self.image.width // 2 # добавление якоря
      self.image.anchor_y = self.image.height // 2 # добавление якоря
      self.objc = pyglet.sprite.Sprite(self.image, x=x, y=y, batch=bat, group=foreground_group) # создание объекта типа Sprite
      self.path = (self.des_x, self.des_y) # точка назначения
      self.id = ind
      self.pathless = 0
      self.speed = 300
      self.speed_x = 0 # скорость по x
      self.speed_y = 0 # скорость по y
      self.objc.scale = 0.1 # масштаб объекта
      self.objc.rotation = 0 # угол проворота

   def movecar(self, dt): # движение машины по двум заданным точкам, с поворотом в сторону конечной точки
      if not (math.isclose(self.objc.x, self.des_x, abs_tol=0.1) and math.isclose(self.objc.y, self.des_y, abs_tol=0.1)): # проверка есть ли близко искомая точка с небольшой погрешностью
         if self.pathless >= (self.speed_x ** 2 + self.speed_y ** 2)**0.5:
            self.pathless -= (self.speed_x ** 2 + self.speed_y ** 2)**0.5
            self.objc.x += self.speed_x
            self.objc.y += self.speed_y
         else:
            self.objc.x = self.des_x
            self.objc.y = self.des_y

      else:
         self.objc.x = self.des_x
         self.objc.y = self.des_y
         self.speed_x = 0
         self.speed_y = 0
         self.speed = 0
         return

      if self.speed_x == 0 and self.speed_y ==0:
         dx = self.des_x - self.objc.x
         dy = self.des_y - self.objc.y
         self.pathless = (dx ** 2 + dy ** 2)**0.5
         if dx > 0 :
            self.speed_x = self.speed * dt
            if dy > 0:
               self.speed_y = (self.speed * dt) * abs((dy / dx))
            else:
               self.speed_y = -((self.speed * dt) * abs((dy / dx)))
         elif dx < 0:
            self.speed_x = -(self.speed * dt)
            if dy > 0:
               self.speed_y = (self.speed * dt) * abs((dy / dx))
            else:
               self.speed_y = -((self.speed * dt) * abs((dy / dx)))
         else:
            self.speed_x = 0
            if dy > 0:
               self.speed_y = (self.speed * dt)
            else:
               self.speed_y = -(self.speed * dt)




         self.objc.rotation = math.degrees(math.atan2(dx,dy))




   def init(self): # инициализация движения(движение по введенным координатам)
      for inp in inputs:
         if inp.ident == self.id[0]:
            self.des_x = int(inp.text)
         if inp.ident == self.id[1]:
            self.des_y = int(inp.text)
         if inp.ident == self.id[2]:
            self.speed = int(inp.text)
      pyglet.clock.schedule_interval(self.movecar, 1 / FPS)
# класс для объектов(машин)

class Button:
   def __init__(self,x,y,width,height,color,text,func,batch):
      self.rect = shapes.Rectangle(x, y, width, height, color=color, batch=batch)
      self.label = pyglet.text.Label(text, x=x + width // 2, y=y + height // 2, anchor_x='center', batch=bat)
      self.func = func
      self.x, self.y, self.w, self.h = x, y, width, height

   def contains(self, x, y):
      return self.x <= x <= self.x + self.w and self.y <= y <= self.y + self.h
# класс для кнопок

class DesInput:
   def __init__(self, x, y, width, height, batch, ident):
      self.ident = ident
      self.rect = pyglet.shapes.Rectangle(x, y, width, height, color=(220, 220, 220), batch=batch)
      self.label = pyglet.text.Label("", x=x + 5, y=y + height // 2, anchor_y='center', batch=batch,font_size=height//2)
      self.cursor = pyglet.shapes.Rectangle(x + 5, y + 5, 2, height - 10, color=(0, 0, 0), batch=batch)
      self.cursor.visible = False
      self.active = False
      self.text = ''
      self.len = None

   def check_hit(self, x, y): # обработка попадания на текстовое поле
         return self.rect.x <= x <= self.rect.x + self.rect.width and self.rect.y <= y <= self.rect.y + self.rect.height

   def on_text(self, text): # ввод текста за исключением перевода строки и табуляции
      if self.active:
         if text not in ('\n', '\r', '\t'):
            self.text += text
            self.label.text = self.text
            self._update_cursor_pos()

   def on_key_press(self, symbol, modifiers): # обработка нажатия клавиши
      if self.active and symbol == pyglet.window.key.BACKSPACE:
         self.text = self.text[:-1]
         self.label.text = self.text
         self._update_cursor_pos()

   def _update_cursor_pos(self): # обновление позиции курсора
      self.cursor.x = self.label.x + self.label.content_width + 2

   def set_active(self, active): # активность поля
      self.active = active
      self.cursor.visible = active
      self.rect.color = (180, 180, 255) if active else (220, 220, 220)
# класс для полей ввода


class Point:
   def __init__(self,x,y,batch,name):
      self.model = pyglet.shapes.Circle(x,y,30,None, color=(77, 62, 215),batch=batch, group=middle_group)
      self.x = x
      self.y = y
      self.name = name

points_list = []

def create_point():
   global points_list
   point_x = 0
   point_y = 0
   point_name = ""

   for inp in inputs:
      if inp.ident == "point_x":
         point_x = int(inp.text)
      elif inp.ident == "point_y":
         point_y = int(inp.text)
      elif inp.ident == "point_name":
         point_name = inp.text

   points_list.append(Point(point_x,point_y,bat,point_name))

def delete_point():
   point_name = ""
   for inp in inputs:
      if inp.ident == "point_name_delete":
         point_name = inp.text
   for point in points_list:
      if point.name == point_name:
         point.model.delete()
         points_list.remove(point)


point_test = Point(100, 100, bat, "point_test")

inputs = [
DesInput(1100, 650, 90, 40, bat, '1x'),
DesInput(1210, 650, 90, 40, bat, '1y'),
DesInput(1150, 600, 90, 40, bat, 'speed1'),

DesInput(1100, 350, 90, 40, bat, '2x'),
DesInput(1210, 350, 90, 40, bat, '2y'),
DesInput(1150, 300, 90, 40, bat, 'speed2'),

DesInput(1350,550,90,40,bat,'point_x'),
DesInput(1460,550,90,40,bat,'point_y'),
DesInput(1400,500,90,40,bat,'point_name'),

DesInput(1400,350,90,40,bat,'point_name_delete')

]
# набор полей ввода

buttons = [
   Button(1100, 700, 200, 50, (70, 70, 220), "Машина 1", lambda: car1.init(), bat),
   Button(1100, 400, 200, 50, (220, 70, 70), "Машина 2", lambda: car2.init(), bat),
   Button(1350,600,200, 50, (100, 170, 70), "Создать пункт", lambda : create_point(), bat),
   Button(1350,400,200, 50, (100, 170, 70), "Удалить пункт", lambda: delete_point(), bat)
]
# набор кнопок


car1 = Car(1000,800, ('1x','1y','speed1'))
car2 = Car(100,900, ('2x','2y','speed2'))
# создание машин



@window.event
def on_text(text):
   for inp in inputs:
      inp.on_text(text)

@window.event
def on_key_press(symbol, modifiers):
   for inp in inputs:
      inp.on_key_press(symbol, modifiers)

@window.event
def on_draw():
   window.clear()
   bat.draw()
# отрисовка


@window.event
def on_mouse_press(x, y, button, modifiers):
   for but in buttons:
      if but.contains(x,y):
         but.func()
   for inp in inputs:
      inp.set_active(inp.check_hit(x, y)) # проверка сначала попадания в область поля ввода, затем передача T/F в активность поля

# обработка нажатия кнопки мыши


FPS = 60

pyglet.app.run()