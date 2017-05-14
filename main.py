#!/usr/bin/env python
import sys
import pyglet
import random
import datetime
from cloud_batch import *
from time_display import *

#window = pyglet.window.Window(fullscreen=True)
window = pyglet.window.Window(480, 320)
window.set_mouse_visible(False)
pyglet.gl.glClearColor(1, 1, 1, 1)
pyglet.font.add_file('data/cat.ttf')
catFont = pyglet.font.load('Cat Font')

timeDisp = TimeDisplay(window.width, window.height)
clouds = CloudBatch(4)

@window.event
def on_draw():
    now = datetime.datetime.now().strftime("%A:%I:%M").split(":")
    day, hour, minute = now
    hour = str(int(hour))

    timeDisp.update(day, hour, minute)

    window.clear()
    clouds.draw()
    timeDisp.draw()

pyglet.clock.schedule_interval(clouds.updateSprites, 1/60.0)
pyglet.clock.schedule_interval(timeDisp.colonSwitch, 0.5)
pyglet.app.run()
