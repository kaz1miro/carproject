import pyglet
import constants as const


class Point:
   points_list = []  # Общий список всех точек (атрибут класса)

   def __init__(self, x, y, name):
      self.model = pyglet.shapes.Circle(x, y, 30, None, color=(77, 62, 215), batch=const.main_batch, group= const.middle_group)
      self.x = x
      self.y = y
      self.name = name
      Point.points_list.append(self)  # Автоматически добавляем новую точку в список

   @classmethod
   def create_point(cls, innputs, batch):
      """Метод класса для создания новой точки"""
      point_x = 0
      point_y = 0
      point_name = ""

      for inp in innputs:
         if inp.ident == "point_x":
            point_x = int(inp.text)
         elif inp.ident == "point_y":
            point_y = int(inp.text)
         elif inp.ident == "point_name":
            point_name = inp.text

      return cls(point_x, point_y, point_name)  # Создаем и возвращаем новый экземпляр

   @classmethod
   def delete_point(cls, innputs):
      """Метод класса для удаления точки по имени"""
      point_name = ""
      for inp in innputs:
         if inp.ident == "point_name_delete":
            point_name = inp.text

      for point in cls.points_list[:]:  # Делаем копию списка для безопасного удаления
         if point.name == point_name:
            point.model.delete()
            cls.points_list.remove(point)
            break

   @classmethod
   def get_point_by_name(cls, name):
      """Дополнительный метод для поиска точки по имени"""
      for point in cls.points_list:
         if point.name == name:
            return point
      return None