#!/usr/bin/env python
import pyglet
import touch_handler
import window_manager 

# TODO
# remove cloud_batch scheduler for 'clock' mode...
# uses more power

#window = pyglet.window.Window(fullscreen=True)
window = pyglet.window.Window(480, 320)
window.set_mouse_visible(False)
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
