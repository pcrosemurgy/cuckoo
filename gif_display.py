import subprocess
import pyglet

# TODO use bg image from settings

class GifDisplay():
    def __init__(self):
        self.gifs = []
        self.count = 0
        self.files = subprocess.check_output("shuf -n4 -e data/img/day/*.gif", shell=True).split()
        for f in self.files:
            print(f)
            a = pyglet.image.load_animation(f)
            self.gifs.append(pyglet.sprite.Sprite(a, x=240-a.get_max_width()/2, y=160-a.get_max_height()/2))
        def f(dt):
            self.count += 1
        pyglet.clock.schedule_once(f, 10)

    def draw(self):
        if self.count == len(self.gifs)
            pyglet.clock.unschedule(self.newGif)
            return True
        self.gifs[self.count].draw()
