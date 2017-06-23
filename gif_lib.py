import os
import sys
import urllib
from PIL import Image
from imgurpython import ImgurClient

def isGifAnimated(gif):
    try:
        frame = Image.open(gif)
        frame.seek(1)
        frame.seek(2)
        return True
    except:
        return False

def analyzeImage(path):
    im = Image.open(path)
    results = {'size': im.size, 'mode': 'full'}
    try:
        while True:
            if im.tile:
                tile = im.tile[0]
                update_region = tile[1]
                update_region_dimensions = update_region[2:]
                if update_region_dimensions != im.size:
                    results['mode'] = 'partial'
                    break
            im.seek(im.tell()+1)
    except EOFError:
        pass
    return results

def resizeGif(path):
    mode = analyzeImage(path)['mode']
    im = Image.open(path)
    if im.size[0] > 480:
        resizeTo[0] = 480
    if im.size[1] > 480:
        resizeTo[1] = 320
    p = im.getpalette()
    last_frame = im.convert('RGBA')
    allFrames = []
    i = 0
    try:
        while True:
            if not im.getpalette():
                im.putpalette(p)
            new_frame = Image.new('RGBA', im.size)
            if mode == 'partial':
                new_frame.paste(last_frame)
            new_frame.paste(im, (0, 0), im.convert('RGBA'))
            new_frame.thumbnail(resizeTo, Image.ANTIALIAS)
            allFrames.append(new_frame)
            i += 1
            last_frame = new_frame
            im.seek(im.tell()+1)
    except EOFError:
        pass
    allFrames[0].save(path, optimize=True, save_all=True, append_images=allFrames[1:], loop=1000)

def downloadGifs():
    os.system('rm -f data/img/day/*')
    cId = '672625cda895fbb'
    cSecret = '713c722f9ad5d145682067e405ece58b67a66b93'
    client = ImgurClient(cId, cSecret)  
    gal = client.subreddit_gallery('catgifs', sort='best', window='day')
    for e in [e.link for e in gal if e.link[-3:] == 'gif']:
        byteSize = int(urllib.urlopen(e).info().getheaders("Content-Length")[0])
        if byteSize > 1024**2*3 or byteSize == 0:
            continue
        os.system("wget -P data/img/day {} 2>/dev/null".format(e))
        path = 'data/img/day'+e[e.rfind('/'):]
        if not isGifAnimated(path):
            try:
                os.remove(path)
            except OSError:
                pass
        resizeGif(path)
