import pandas as pd
import re
songs = pd.read_table('/Volumes/Data/Dropbox/Python3/git/spotify/songs.txt').values.tolist()
#print(songs[0][0][-22:])

songid=[]

for song in songs:
    songid.append('spotify:track:'+song[0][-22:])

#print(songid[0:5])

import spotipy
import spotipy.util as util

token = util.prompt_for_user_token('117616277','user-read-recently-played','c9b1603ff54c4384b7ff635b0784496e','bc56ff583be844b8b35d3571b7b1ca80','dajofischer://callback/')
spotify = spotipy.Spotify(auth=token)


whichurl = 'spotify:artist:4qhaHyCtCaFugTqT9LzuKp'

artistresults = spotify.artist(whichurl)

artistimageurl = artistresults['images'][0]['url']
print(artistimageurl)

# Freundin Conni: spotify:artist:0HerMOOFZXxIF3Yg9BVl0W
# Conni spotify:artist:0jRC2uXx4hEpqNrBDJdY7l
# Bibi Tina: spotify:artist:2x8vG4f0HYXzMEo3xNsoiI
# petterson findus: spotify:artist:3YZqnPKdtP5qP4LSvrgx9i
# sam: spotify:artist:4qhaHyCtCaFugTqT9LzuKp

#results = spotify.artist_albums('spotify:artist:0HerMOOFZXxIF3Yg9BVl0W',limit=50)
results = spotify.artist_albums(whichurl,limit=48,offset=0)
#results = spotify.artist_albums('spotify:artist:0jRC2uXx4hEpqNrBDJdY7l',limit=50,offset=50)

albumname  = []
albumpicture  = []
albumid  = []
artistpicture  = []
#print((results['items'][0]['external_urls']['spotify']))

for item in results['items']:
    albumname.append(item['name'])
    albumpicture.append(item['images'][0]['url'])
    albumid.append(item['external_urls']['spotify'])
    #artistpicture.append(item[''])
#print(results['items'])
from PIL import Image
import requests
from io import BytesIO
import numpy as  np
import os.path
import qrcode

# imgcode = qrcode.make('https://www.youtube.com/watch?v=U9EjruMBmhY')
# imgcode.show()

import matplotlib
matplotlib.use("TkAgg")
from matplotlib import pyplot as plt

response = requests.get(artistimageurl)
imgartist = Image.open(BytesIO(response.content))

imgartist = np.array(imgartist)

printfront = []
printback = []

for i in range(len(albumname)):


    imgcode = qrcode.make(albumid[i])
    #img.save('test.jpg')

    response = requests.get(albumpicture[i])
    img = Image.open(BytesIO(response.content))
    img = np.array(img)



    imgcodesmall = imgcode.resize([300,300])
    imgcoverqc = np.array(imgcodesmall)
    imgcoverqc = np.uint8(imgcoverqc)*255
    imgcoverartist = np.array(imgartist)

    shapes = [imgcoverqc.shape, imgcoverartist.shape]


    mask = int((shapes[1][0]/2))
    mask = [mask, mask+shapes[0][0]]

    imgcoverartist[mask[0]:mask[1],mask[0]:mask[1],0] = imgcoverqc
    imgcoverartist[mask[0]:mask[1],mask[0]:mask[1],1] = imgcoverqc
    imgcoverartist[mask[0]:mask[1],mask[0]:mask[1],2] = imgcoverqc

    printfront.append(imgcoverartist)
    printback.append(img)
    print([imgcoverartist.shape, img.shape])

emptypic = np.ones([shapes[1][0],shapes[1][0],3],dtype = np.uint8)*255

if len(printfront)%6 != 0:
    for _ in range(6-len(printfront)%6):
        printfront.append(emptypic)
        printback.append(emptypic)



arrayaccess = np.reshape(np.arange(0,len(printfront)),(int(len(printfront)/6),6))

print(arrayaccess)

for rowaccess in arrayaccess:

    im = Image.fromarray(np.concatenate([np.concatenate([printback[rowaccess[0]],printback[rowaccess[1]],printback[rowaccess[2]]],axis = 0),np.concatenate([printback[rowaccess[3]],printback[rowaccess[4]],printback[rowaccess[5]]],axis = 0)],axis=1))
    if os.path.isfile('test.pdf'):
        im.save('test.pdf',append=True)
    else:
        im.save('test.pdf')

    im = Image.fromarray(np.concatenate([np.concatenate([printfront[rowaccess[3]],printfront[rowaccess[4]],printfront[rowaccess[5]]],axis = 0),np.concatenate([printfront[rowaccess[0]],printfront[rowaccess[1]],printfront[rowaccess[2]]],axis = 0)],axis=1))
    im.save('test.pdf',append=True)
