import os
import subprocess
import pyglet
from gif_lib import *

# TODO use bg image from settings

class GifDisplay():
    def __init__(self):
        self.gif = None
        self.played = []
	self.newGif()

    def newGif(self, dt=0):
        self.randomGif()
        pyglet.clock.schedule_once(self.newGif, 15)

    def randomGif(self):
        while 1:
            f = subprocess.check_output("shuf -n1 -e data/img/day/*.gif", shell=True).rstrip()
            if f not in self.played:
                break
        self.played.append(f)
        myX, myY = resizeGif(f)
        a = pyglet.image.load_animation(f)
        self.gif = pyglet.sprite.Sprite(a, x=myX, y=myY)

    def draw(self):
        self.gif.draw()
        if len(self.played) == 3:
            pyglet.clock.unschedule(self.newGif)
            return True
