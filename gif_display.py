import glob
import pyglet

# TODO use bg image from settings

class GifDisplay():
    def __init__(self):
        self.gif = None
        self.files = set(glob.glob('data/img/day/*.gif'))
        pyglet.clock.schedule_interval(self.switchGif, 10)
        self._done = False

    def switchGif(self, dt):
        if self.gif:
            self.gif.delete()
        try:
            a = pyglet.image.load_animation(self.files.pop())
        except KeyError:
            self._done = true 
            return
        self.gif = pyglet.sprite.Sprite(a, x=240-a.get_max_width()/2, y=160-a.get_max_height()/2)

    def draw(self):
        if self._done:
            pyglet.clock.unschedule(self.switchGif)
            return True
        self.gifs.draw()
