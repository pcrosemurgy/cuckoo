#!/usr/bin/env python
import os
import urllib
import subprocess
from PIL import Image
from imgurpython import ImgurClient
import pyglet

def isGifAnimated(inGif):
    try:
        frame = Image.open(inGif)
        frame.seek(1)
        frame.seek(2)
        return True
    except:
        return False

if len(sys.argv) > 1:
    cId = '672625cda895fbb'
    cSecret = '713c722f9ad5d145682067e405ece58b67a66b93'
    client = ImgurClient(cId, cSecret)  

    gal = client.subreddit_gallery('catgifs', sort='best', window='day')
    for e in [e.link for e in gal if e.link[-3:] == 'gif']:
        byteSize = int(urllib.urlopen(e).info().getheaders("Content-Length")[0])
        if byteSize > 1024**2*3 or byteSize == 0:
            continue
        os.system("wget -P data/img/day {} 2>/dev/null".format(e))
        i = e.rfind('/')
        path = 'data/img/day'+e[i:]
        animated = isGifAnimated(path)
        if animated:
            print(e)
        else:
            try:
                os.remove(path)
            except OSError:
                pass

window = pyglet.window.Window(450, 450)
#window = pyglet.window.Window(fullscreen=True)

a = pyglet.image.load_animation('data/img/day/C0yuLiK.gif')
s = pyglet.sprite.Sprite(a)

@window.event
def on_draw():
    s.draw()

pyglet.app.run()
