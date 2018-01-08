import os
import glob
import json
import urllib

def download(replace=True, dt=None):
    if replace:
        for f in glob.glob('data/img/day/*.gif'):
            os.remove(f)
    query = 'cat'
    key = 'UpXOAsb4XAS8rY6s1cVw9Jm2HgnTUEzc'
    data = json.loads(urllib.urlopen("http://api.giphy.com/v1/gifs/search?q={}&sort=recent&api_key={}&limit=3".format(query, key)).read())

    for e in data['data']:
        path = 'data/img/day/'+e['id']+'.gif'
        obj = e['images']['downsized']
        urllib.urlretrieve(obj['url'], filename=path)

        if int(obj['width']) > 480 or int(obj['height']) > 320:
            os.system("gifsicle --batch --resize {}x{} {} 1>/dev/null 2>/dev/null".format(480, 320, path))
