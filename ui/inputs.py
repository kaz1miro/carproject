import pyglet
import constants as const

class DesInput:
   def __init__(self, x, y, width, height, ident):
      self.ident = ident
      self.rect = pyglet.shapes.Rectangle(x, y, width, height, color=(220, 220, 220), batch=const.main_batch, group=const.middle_group)
      self.label = pyglet.text.Label("", x=x + 5, y=y + height // 2, anchor_y='center', batch=const.main_batch,font_size=height//2)
      self.cursor = pyglet.shapes.Rectangle(x + 5, y + 5, 2, height - 10, color=(0, 0, 0), batch=const.main_batch, group=const.foreground_group)
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