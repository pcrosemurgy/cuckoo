#!/usr/bin/env python
from imgurpython import ImgurClient

client_id = '672625cda895fbb'
client_secret = '713c722f9ad5d145682067e405ece58b67a66b93'
client = ImgurClient(client_id, client_secret)  

# Example request 
items = client.gallery() 
for item in items:     
    print(item.link)
