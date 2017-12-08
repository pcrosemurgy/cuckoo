import urllib, json

def download(replace=False):
    if replace:
        for f in glob.glob('data/img/day/*.gif'):
            os.remove(f)
    query = 'cat'
    key = 'UpXOAsb4XAS8rY6s1cVw9Jm2HgnTUEzc'
    data = json.loads(urllib.urlopen("http://api.giphy.com/v1/gifs/search?q={}&api_key={}&limit=3".format(query, key)).read())

    for e in data['data']:
        urllib.urlretrieve(e['images']['downsized']['url'], filename='data/img/day/'+e['id']+'.gif')
