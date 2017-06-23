#!/usr/bin/env python
import os
import sys
from gif_lib import *
import pyglet

if len(sys.argv) > 1:
    downloadGifs()

window = pyglet.window.Window(480, 320)
#window = pyglet.window.Window(fullscreen=True)

gif = '2AMqHUJ.gif'
x1, y1 = resizeGif('data/img/day/'+gif, (480, 320))
a = pyglet.image.load_animation('data/img/day/'+gif)
s = pyglet.sprite.Sprite(a, x=x1, y=y1)

@window.event
def on_draw():
    window.clear()
    s.draw()

pyglet.app.run()
