#!/usr/bin/env python
import sys
import pyglet
import random
import datetime
from time_display import *

#window = pyglet.window.Window(fullscreen=True)
window = pyglet.window.Window(480, 320)
window.set_mouse_visible(False)
pyglet.gl.glClearColor(1, 1, 1, 1)
pyglet.font.add_file('data/cat.ttf')
catFont = pyglet.font.load('Cat Font')

timeDisp = TimeDisplay(window.width, window.height)

cloud = pyglet.sprite.Sprite(pyglet.image.load('data/bird1.png'), x=150, y=150)

@window.event
def on_draw():
    now = datetime.datetime.now().strftime("%A:%I:%M").split(":")
    day, hour, minute = now
    hour = str(int(hour))

    timeDisp.update(day, hour, minute)

    window.clear()
    timeDisp.draw()
    cloud.draw()

pyglet.clock.schedule_interval(timeDisp.colonSwitch, 0.5)
pyglet.app.run()
