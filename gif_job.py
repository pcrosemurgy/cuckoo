import os
import re
import glob
import urllib
from PIL import Image
from imgurpython import ImgurClient

cId = '672625cda895fbb'
cSecret = '713c722f9ad5d145682067e405ece58b67a66b93'
client = ImgurClient(cId, cSecret)  
print(client.get_auth_url('pin'))
c = client.authorize(raw_input('enter pin: '), 'pin')
client.set_user_auth(c['access_token'], c['refresh_token'])

def downloadGifs():
    for f in glob.glob('data/img/tmp/*.gif'):
        os.remove(f)
    gal = client.subreddit_gallery('catgifs', sort='best', window='week')
    count = 0

    for e in [e.link for e in gal if e.link[-3:] == 'gif']:
        if re.search(r"\w{8}\.gif$", e):
            e = e[:-5]+e[-4:]
        path = 'data/img/tmp'+e[e.rfind('/'):]
        urllib.urlretrieve(e, filename=path)

        w, h = Image.open(path).size
        if w > 480:
            w = 480
        if h > 320:
            h = 320
        os.system("gifsicle --batch --resize {}x{} {} 1>/dev/null 2>/dev/null".format(w, h, path))
        os.system("gifsicle -U `seq -f \"#%g\" 0 2 99` -O2 {} 1>/dev/null 2>/dev/null".format(path))
        if(os.path.getsize(path) > 4*1024**2):
            os.remove(path)
        else:
            print('downloaded '+e)
            count += 1 
            if count == 9:
                break

def uploadGifs():
    ids = []
    for f in glob.glob('data/img/tmp/*.gif'):
        print('uploading '+f)
        ids.append(client.upload_from_path(f, anon=False)['id'])
    print('uploaded ids: ')
    print(ids)
    albumId = client.get_account_albums('thepaulbird')[0].id
    client.album_add_images(albumId, ids)

downloadGifs()
#uploadGifs()
