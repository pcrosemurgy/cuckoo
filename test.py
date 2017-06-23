import os
import subprocess
import pyglet

# TODO use bg image from settings

class GifDisplay():
    def __init__(self):
        self.gif = None
        self.played = []
	self.newGif()

    def newGif(self, dt=0):
        self.randomGif()
        pyglet.clock.schedule_once(self.newGif, 5)

    def randomGif(self):
        while 1:
            f = subprocess.check_output("gshuf -n1 -e data/img/day/*.gif", shell=True).rstrip()
            if f not in self.played:
                break
        print(f)
        self.played.append(f)
        a = pyglet.image.load_animation(f)
        self.gif = pyglet.sprite.Sprite(a, x=240-a.get_max_width()/2, y=160-a.get_max_height()/2)

    def draw(self):
        self.gif.draw()
#if len(self.played) == 3:
#pyglet.clock.unschedule(self.newGif)
#return True

window = pyglet.window.Window(480, 320)
g = GifDisplay()

@window.event
def on_draw():
    window.clear()
    g.draw()

pyglet.app.run()
