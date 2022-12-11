import json
import requests
import sqlite3
import os
import csv
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
import spotipy.util as util

def spotify():
    sp = spotipy.Spotify()
    cid = "5b023ed3b67b4648a542d812ee5974f4"
    secret = "5b3c316393c74cef8ab027e096757142"
    os.environ['SPOTIPY_CLIENT_ID']= cid
    os.environ['SPOTIPY_CLIENT_SECRET']= secret
    os.environ['SPOTIPY_REDIRECT_URI']='http://localhost:8888/callback'
    username =""
    client_credentials_manager = SpotifyClientCredentials(client_id=cid, client_secret=secret)
    sp = spotipy.Spotify(client_credentials_manager = client_credentials_manager)
    client_credentials_manager = SpotifyClientCredentials(client_id=cid, client_secret=secret) 
    sp = spotipy.Spotify(client_credentials_manager=client_credentials_manager)
    scope = 'user-top-read'
    token = util.prompt_for_user_token(cid, scope) 
    sp = spotipy.Spotify(auth=token)
    results = sp.current_user_top_tracks(limit=50,offset=0,time_range='medium_term')
    for album in range(50):
        list = []
        list.append(results)
        with open('top50_data.json', 'w', encoding='utf-8') as f:
            json.dump(list, f, ensure_ascii=False, indent=4)






def open_database(db_name):
    path = os.path.dirname(os.path.abspath(__file__))
    conn = sqlite3.connect(path+'/'+db_name)
    cur = conn.cursor()
    return cur, conn
    





def main():
    
    
    dir_path = os.path.dirname(os.path.realpath(__file__))
    
    cur, conn = open_database('spotify.db')
    spotify()

    
    


if __name__ == "__main__":
    main()