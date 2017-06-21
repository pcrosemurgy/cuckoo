#!/usr/bin/env python
import pyglet

#window = pyglet.window.Window(450, 450)
window = pyglet.window.Window(fullscreen=True)

a = pyglet.image.load_animation('data/img/day/C0yuLiK.gif')
s = pyglet.sprite.Sprite(a)

@window.event
def on_draw():
#window.clear()
    s.draw()

pyglet.app.run()
