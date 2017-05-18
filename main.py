#!/usr/bin/env python
import pyglet
from cloud_batch import *
from time_display import *
from touch_handler import *

#window = pyglet.window.Window(fullscreen=True)
window = pyglet.window.Window(480, 320)
window.set_mouse_visible(False)
pyglet.gl.glClearColor(102.0/255, 204.0/255, 1, 1)
pyglet.font.add_file('data/cat.ttf')
catFont = pyglet.font.load('Cat Font')

timeDisp = TimeDisplay(window.width, window.height)
clouds = CloudBatch()

touch = TouchHandler()

# TODO
# make "ModeManager" class
# designates what draws to do based on mode
# holds system time, have updated every 5 seconds
# modes: normal, bird, settings, alarm -> chromium kiosk

# TODO
# make timer class
# update every 10 seconds

@window.event
def on_mouse_press(x, y, button, modifiers):
    touch.press(x, y)

@window.event
def on_mouse_release(x, y, button, modifiers):
    e = touch.release(x, y)
# TODO
# pass these on to the ModeManager
# which will pass on to the current DisplayManager
# registerPress(x, y) if not drag

# TODO
# to determine which object was pressed:
# curr = x^2+y^1 gives you unique polynomial
# for each rectangle hit box: - bottom-left corner x^2+y^1
#                             - bottom-right corner
# if curr within hit box's two polynomial values then hit
# uses binning
    if e == 'drag':
        pass
    elif e == 'short':
        pass
    elif e == 'long':
        pass

@window.event
def on_draw():
    window.clear()
    clouds.draw()
    timeDisp.draw()

pyglet.clock.schedule_interval(clouds.updateSprites, 1/60.0)
pyglet.clock.schedule_interval(timeDisp.colonSwitch, 0.5)
pyglet.clock.schedule_interval(timeDisp.update, 5)
pyglet.app.run()
