# Copyright (c) 2016 Payam Siyari
#!/usr/bin/env python
# -*- coding: utf-8 -*-

import urllib
import requests
from bs4 import BeautifulSoup
import eyed3
import sys
import json
import os

def setTags (fileName, spotifyURI):
    trackID = spotifyURI.split('spotify:track:')[-1]
    urlTrack = 'https://api.spotify.com/v1/tracks/' + trackID
    headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'}

    response = requests.get(urlTrack, headers=headers)

    jsonResponseTrack = response.content
    jTrack = json.loads(jsonResponseTrack)
    albumName = jTrack['album']['name']
    coverFileUrl = jTrack['album']['images'][0]['url']
    urllib.urlretrieve(coverFileUrl,"img.jpg")
    imagedata = open("img.jpg","rb").read()
    artists = ''
    for a in jTrack['artists']:
        artists += a['name'] + ", "
    artists = artists.rstrip(", ")
    title = jTrack['name']

    urlAlbum = jTrack['album']['href']
    response = requests.get(urlAlbum, headers=headers)
    jsonResponseAlbum = response.content
    jAlbum = json.loads(jsonResponseAlbum)
    albumReleaseDate = jAlbum['release_date'].split('-')[0]

    audiofile = eyed3.load(fileName)
    audiofile.tag.artist = artists
    audiofile.tag.album = albumName
    audiofile.tag.album_artist = artists
    audiofile.tag.title = title
    audiofile.tag.date = albumReleaseDate
    audiofile.tag.release_date = albumReleaseDate
    audiofile.tag.orig_release_date = albumReleaseDate
#     audiofile.tag.recording_date = albumReleaseDate
    audiofile.tag.encoding_date = albumReleaseDate
    audiofile.tag.tagging_date = albumReleaseDate
    audiofile.tag.images.set(3,imagedata,"image/jpeg")
    audiofile.tag.save()

    os.remove("img.jpg")

    print artists + ", " + title + ", " + albumName + ", " + albumReleaseDate

if __name__ == "__main__":
    setTags(sys.argv[-2], sys.argv[-1])