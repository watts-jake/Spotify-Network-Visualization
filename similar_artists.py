#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Notes for code imporvement:
fix or remove genre
"""

import spotipy
import pandas as pd
from spotipy.oauth2 import SpotifyClientCredentials
from pyvis.network import Network

# credentials to use spotify API
client_id = ''
client_secret = ''
client_credentials_manager = SpotifyClientCredentials(client_id, client_secret)
sp = spotipy.Spotify(client_credentials_manager=client_credentials_manager)

# takes artist name and gives artistID of first search result
def getArtistID(artistName):
    name = "{" + artistName + "}"
    result = sp.search(name, type = 'artist') #search query
    artistName = result['artists']['items'][0]['name']
    artistPopularity = result['artists']['items'][0]['popularity']
    artistImage = result['artists']['items'][0]['images'][0]['url']
    artistID = result['artists']['items'][0]['id']
    artistGenre = result['artists']['items'][0]['genres'][0]
    artistInfo = [artistName, artistID, artistPopularity, 
                  artistImage, artistGenre]
    return artistInfo

# gets 20 related artists based on artistsID
def getRelatedArtists(artistID, num):
    artist = sp.artist_related_artists(artistID)
    
    artistsRelated = []
    for i in range(num):
        artistRelated = [artist['artists'][i]['name'], 
                         artist['artists'][i]['popularity'],
                         artist['artists'][i]['id'],
                         artist['artists'][i]['images'][0]['url'],
                         artist['artists'][i]['genres'][0]
                         ]
        artistsRelated.append(artistRelated)
        
    df = pd.DataFrame(artistsRelated, 
                      columns = ['artist', 'popularity', 
                                 'artistID', 'url', 'genre'])
    df = df.sort_values(by= 'popularity', ascending = False).reset_index()
        
    return df

# adds node to graph based on artist
def graphRelatedArtist(name, num, df):
    g.add_node(name, 
               label=name, title='popularity: ' + str(artistInfo[2]) + 
               "\ngenre: " + str(artistInfo[4]),
               shape = 'image', image = artistInfo[3])
    for i in range(num):
        g.add_node(df.artist[i], label=df.artist[i], 
                   title='popularity: ' + str(df.popularity[i]) + 
                   "\ngenre: " + str(df.genre[i]),
                   shape = 'image', image = df.url[i])
        g.add_edge(name, df.artist[i])

name = input('enter name: ')
num = int(input('enter number of related artists to display (1-20): '))
artistInfo = getArtistID(name)
df = getRelatedArtists(artistInfo[1], 20)

# visualization method with html file
g = Network(height="750px", width="100%", bgcolor="#222222", 
            font_color="white")           
graphRelatedArtist(name, num, df)

expnasion = True
while expnasion is True:        
    expand = input('would you like to view more related artists (y/n)? ')
    if expand == 'n':
        print('graph complete')
        expnasion = False
    elif expand == 'y':
        print(df.artist[0:num])
        choice = int(input('choose number corresponding to desired artist: '))
        num = int(input('enter number of related artists to display (1-20): '))
        artistInfo = getArtistID(df.artist[choice])
        df = getRelatedArtists(artistInfo[1], 20)
        graphRelatedArtist(artistInfo[0], num, df)
    else:
        print('error enter y or n')

# populates the nodes and edges data structures
g.show("nx.html")
