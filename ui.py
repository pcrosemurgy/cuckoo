#!/usr/bin/env python
import pyglet
from pyglet.gl import *

#window = pyglet.window.Window(fullscreen=True)
window = pyglet.window.Window(480, 320)
window.set_mouse_visible(False)
pyglet.gl.glClearColor(1, 1, 1, 1)

background = pyglet.image.load('/Users/paul/Desktop/img/pattern.png')
on = pyglet.image.load('/Users/paul/Desktop/img/on.png')
off = pyglet.image.load('/Users/paul/Desktop/img/off.png')
dec = pyglet.image.load('/Users/paul/Desktop/img/decrement.png')
inc = pyglet.image.load('/Users/paul/Desktop/img/increment.png')
done = pyglet.image.load('/Users/paul/Desktop/img/done.png')

x = 480-75-5
y = 315

@window.event
def on_draw():
    glEnable(GL_BLEND)
    glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)
    window.clear()
    background.blit(0, 0)
    on.blit(x+5, y-75)
    inc.blit(x-6, 320/2-45+30)
    dec.blit(x-6, 320/2-45-30)
    done.blit(x+2, y-75-75-75-75)

pyglet.app.run()
