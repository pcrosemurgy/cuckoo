import glob
import pyglet

INTERVAL = 10

class GifDisplay():
    def __init__(self):
        self.gif = None
        self._done = False
        self.files = glob.glob('data/img/day/*.gif')
	self.newGif()
        pyglet.clock.schedule_interval(self.newGif, INTERVAL)

    def newGif(self, dt=0):
        if self.gif:
            self.gif.delete()
        try:
            a = pyglet.image.load_animation(self.files.pop())
        except IndexError:
            self._done = True 
            return
        self.gif = pyglet.sprite.Sprite(a, x=240-a.get_max_width()/2, y=160-a.get_max_height()/2)

    def draw(self):
        if self._done:
            pyglet.clock.unschedule(self.newGif)
            return True
        self.gif.draw()
