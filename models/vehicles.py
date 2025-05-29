import pyglet

import constants as const


class Car:
   def __init__(self, x, y,ind = (0,0,0)):
      self.des_x = None # координата x точки назначения
      self.des_y = None # координата y точки назначения
      self.image = pyglet.image.load('sourse/car.png') # загрузка изображения
      self.image.anchor_x = self.image.width // 2 # добавление якоря
      self.image.anchor_y = self.image.height // 2 # добавление якоря
      self.objc = pyglet.sprite.Sprite(self.image, x=x, y=y, batch=const.main_batch, group= const.foreground_group) # создание объекта типа Sprite
      self.path = (self.des_x, self.des_y) # точка назначения
      self.id = ind
      self.pathless = 0
      self.speed = 300
      self.speed_x = 0 # скорость по x
      self.speed_y = 0 # скорость по y
      self.objc.scale = 0.1 # масштаб объекта
      self.objc.rotation = 0 # угол проворота

   def movecar(self, dt): # движение машины по двум заданным точкам, с поворотом в сторону конечной точки
      import math
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




   def init(self, inputs): # инициализация движения(движение по введенным координатам)
      for inp in inputs:
         if inp.ident == self.id[0]:
            self.des_x = int(inp.text)
         if inp.ident == self.id[1]:
            self.des_y = int(inp.text)
         if inp.ident == self.id[2]:
            self.speed = int(inp.text)
      pyglet.clock.schedule_interval(self.movecar, 1 / const.FPS)