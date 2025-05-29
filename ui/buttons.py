import pyglet
from pyglet import shapes


class Button:
   def __init__(self,x,y,width,height,color,text,func,batch):
      self.rect = shapes.Rectangle(x, y, width, height, color=color, batch=batch)
      self.label = pyglet.text.Label(text, x=x + width // 2, y=y + height // 2, anchor_x='center', batch=batch)
      self.func = func
      self.x, self.y, self.w, self.h = x, y, width, height

   def contains(self, x, y):
      return self.x <= x <= self.x + self.w and self.y <= y <= self.y + self.h