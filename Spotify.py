import json
import requests
import sqlite3
import os
import csv
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
import spotipy.util as util
from spotipy.oauth2 import SpotifyOAuth
import matplotlib.pyplot as plt

def spotify():
    cid = "3641e3928ecd4cf48421e3cf84cd31dc"
    secret = "b16fb2fa6c7143daa22a8fc1c8c918f2"

    
    os.environ['SPOTIPY_CLIENT_ID']= cid
    os.environ['SPOTIPY_CLIENT_SECRET']= secret
    os.environ['SPOTIPY_REDIRECT_URI']='http://localhost:8888/callback'

    scope = "user-top-read"
    client_credentials_manager = SpotifyClientCredentials(client_id=cid, client_secret=secret)
    sp = spotipy.Spotify(auth_manager= SpotifyOAuth(scope = scope, redirect_uri= 'http://localhost:8888/callback'
, client_id= cid, client_secret= secret ))

    

    playlists = sp.user_playlists('spotify')

    results = sp.current_user_top_tracks(limit = 100, offset = 0, time_range = 'medium_term' )
    items = results["items"]
    #print(len(items))
    popularity = []
    names = []
    artists = []

    for item in items:
        popularity.append(item["popularity"])
        names.append(item["name"])
        artists.append(item['artists'][0]['name'])


    

        for key in item:
            print (key, item[key])


       # print (item, results[item])
            print("==================================================================")


    print (popularity)
    print (names)
    print (artists)
    return popularity,names,artists

  

    #fig, ax = plt.subplots()

    #fruits = ['apple', 'blueberry', 'cherry', 'orange']
    #counts = [40, 100, 30, 55]
   #bar_labels = ['red', 'blue', '_red', 'orange']
    #ar_colors = ['tab:red', 'tab:blue', 'tab:red', 'tab:orange']

    #ax.bar(names, popularity)
    #ax.bar(names, popularity, label=bar_labels, color=bar_colors)

    #ax.set_ylabel('popularity')
    #ax.set_title('song name')
    #ax.legend(title='Fruit color')

    #plt.show() 

    #y_axis = names
    #x_axis = popularity

    #plt.barh(y_axis, x_axis)
    #plt.title('title name')
    #plt.ylabel('y axis name')
    #plt.xlabel('x axis name')
    #plt.show()

    

    
    
    
    







def open_database(db_name):
    path = os.path.dirname(os.path.abspath(__file__))
    conn = sqlite3.connect(path+'/'+db_name)
    cur = conn.cursor()
    return cur, conn


def setUpSongsTable(cur, conn,l1,l2,l3):
    cur.execute("CREATE TABLE IF NOT EXISTS SpotifySongData (Popularity, Song_Name, artist)")
    cur.execute("SELECT * FROM SpotifySongData")
    for i in range(0,25):
        cur.execute('INSERT INTO SpotifySongData (Popularity, Song_name, artist) VALUES (?, ?, ?)', (l1[i], l2[i], l3[i]))
    conn.commit()







def main():
    
    
    dir_path = os.path.dirname(os.path.realpath(__file__))
    
    cur, conn = open_database('spotify.db')
    l1,l2,l3 = spotify()
    setUpSongsTable(cur,conn,l1,l2,l3)

    
    


if __name__ == "__main__":
    main()

    #https://spotipy.readthedocs.io/en/2.9.0/
    #https://rdrr.io/cran/spotifyr/man/get_my_top_artists_or_tracks.html
    #https://developer.spotify.com/documentation/general/guides/authorization/scopes/
