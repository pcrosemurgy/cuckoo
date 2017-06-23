#!/usr/bin/env python
import sys
import pyglet
import touch_handler
import window_manager 
from gif_lib import downloadGifs

# TODO
# ADD LOGGING
downloadGifs()

pyglet.options['debug_gl'] = False

if len(sys.argv) > 1:
    window = pyglet.window.Window(fullscreen=True)
else:
    window = pyglet.window.Window(480, 320)
window.set_mouse_visible(False)
pyglet.font.add_file('data/cat.ttf')
pyglet.font.load('Cat Font')
pyglet.font.load('Helvetica')

touch = touch_handler.TouchHandler()
windowMan = window_manager.WindowManager()

@window.event
def on_mouse_press(x, y, button, modifiers):
    touch.press(x, y)

@window.event
def on_mouse_release(x, y, button, modifiers):
    event = touch.release(x, y)
    windowMan.registerPress(event, x, y)

@window.event
def on_draw():
    window.clear()
    windowMan.draw()

pyglet.app.run()
