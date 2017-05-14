import pyglet
from random import *

# TODO
# test on RPi
# add a bunch of funky birds
class CloudBatch(pyglet.graphics.Batch):
    def __init__(self, numClouds):
        pyglet.graphics.Batch.__init__(self)

        self.birdSprites = []
        for i in range(1, 5):
            png = pyglet.image.load("data/bird{}.png".format(i))
            self.birdSprites.append(pyglet.sprite.Sprite(png, x=randint(0, 480), y=randint(20, 240)))

        self.sprites = [pyglet.sprite.Sprite(pyglet.image.load('data/bird1.png'),
            x=randint(0, 480), y=randint(20, 240), batch=self)]
        for i in range(0, numClouds):
            self.sprites.append(pyglet.sprite.Sprite(pyglet.image.load("data/cloud{}.png".format(i%3+1)),
                x=randint(0, 480), y=randint(20, 300), batch=self))

    def updateSprites(self, dt):
        for i, s in enumerate(self.sprites):
            if s.x > 480:
                if i == 0:
                    s.batch = None
                    self.sprites[0] = choice(self.birdSprites)
                    self.sprites[0].batch = self
                    s.x = randint(-250, -100)
                    s.y = randint(20, 240)
                else:
                    s.x = randint(-250, -100)
                    s.y = randint(20, 300)
            else:
                vs = 12.0 if i == 0 else 22.0
                s.x += vs*dt
