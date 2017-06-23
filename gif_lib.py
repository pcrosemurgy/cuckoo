import os
import sys
import urllib
from PIL import Image
from imgurpython import ImgurClient

def isGifAnimated(path):
    try:
        frame = Image.open(path)
        frame.seek(1)
        frame.seek(2)
        return True
    except:
        return False

def downloadGifs():
    os.system('rm -f data/img/day/*')
    cId = '672625cda895fbb'
    cSecret = '713c722f9ad5d145682067e405ece58b67a66b93'
    client = ImgurClient(cId, cSecret)  
    gal = client.subreddit_gallery('catgifs', sort='best', window='day')
    count = 0
    for e in [e.link for e in gal if e.link[-3:] == 'gif']:
        byteSize = int(urllib.urlopen(e).info().getheaders("Content-Length")[0])
        if byteSize > 1024**2*3 or byteSize == 0:
            continue
        os.system("wget -P data/img/day {} 2>/dev/null".format(e))
        path = 'data/img/day'+e[e.rfind('/'):]
        if isGifAnimated(path):
            w, h = Image.open(path).size
            if w > 480:
                w = 480
            if h > 320:
                h = 320
            os.system("gifsicle --batch --resize {}x{} {}".format(w, h, path))
            print(e)
            count += 1 
        else:
            try:
	        os.remove(path)
            except OSError:
	        pass
        if count == 10:
            break
