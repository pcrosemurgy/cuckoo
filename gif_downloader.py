import os
import re
import glob
import urllib
from imgurpython import ImgurClient

def downloadGifs():
    cId = '672625cda895fbb'
    cSecret = '713c722f9ad5d145682067e405ece58b67a66b93'
    client = ImgurClient(cId, cSecret)  
    albumId = client.get_account_albums('thepaulbird')[0].id

    for f in glob.glob('data/img/week/*.gif'):
        os.remove(f)

    for e in [e.link for e in client.get_album_images(albumId)]:
        print(e)
        path = 'data/img/week'+e[e.rfind('/'):]
        urllib.urlretrieve(e, filename=path)

downloadGifs()
