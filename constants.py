import pyglet
from pyglet.graphics import Group

background_group = Group(0)
middle_group = Group(1)
foreground_group = Group(2)

main_batch = pyglet.graphics.Batch()

FPS = 60