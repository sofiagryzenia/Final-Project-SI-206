#Wikipedia Top USA Songs Beautiful Soup

import json
import requests
import sqlite3
import os
import csv
from bs4 import BeautifulSoup

'''––––––––––––––––––––––––––––––––––––––––––––––––––––––––––– 
DB: Function to set up a database
 –––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––'''

def setUpDatabase(db_name):
    #create a database
    path = os.path.dirname(os.path.abspath(__file__))
    conn = sqlite3.connect(path+'/'+db_name)
    cur = conn.cursor()
    return cur, conn

def getSongs():
    URL = 'https://en.wikipedia.org/wiki/List_of_most-streamed_songs_on_Spotify'

    headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/107.0.0.0 Safari/537.36'}
    page = requests.get(URL, headers=headers)

    soup1 = BeautifulSoup(page.content, 'html.parser')
    soup = BeautifulSoup(soup1.prettify(),'html.parser')
    #prettify to turn Beautiful Soup parse tree into unicode string, w/ a separate line for each tag and each string
    #is this ok, found on internet


    #do we just want ranking and song? I added streams and artist bc unsure
    song_rank = []
    for i in range (0,100):
        rank = soup.find_all('th', attrs = {'style': 'text-align:center;'})[i].text
        rank = rank.replace('\n','')
        rank = rank.strip()
        song_rank.append(rank)

    song_list = []
    for i in range(0,500,5) :
        song = soup.find_all('td')[i].text
        song = song.replace('\n','')
        song = song.replace('"','')
        song = song.strip()
        song = ' '.join(song.split())
        song_list.append(song)


    streams_list = []
    for i in range(1,500,5) :
        streams = soup.find_all('td')[i].text
        streams = streams.replace('\n','')
        streams = streams.strip()
        streams_list.append(streams) 

    artist_list = []
    for i in range(2,500,5):
        artist = soup.find_all('td')[i].text
        artist = artist.replace('\n','')
        artist = artist.strip()
        artist = ' '.join(artist.split())
        artist_list.append(artist)

    data = {
        'Rank' : song_rank,
        'Song' : song_list,
        'Streams' : streams_list,
        'Artist' : artist_list,
    }

    return data

def setUpSongsTable(data, cur, conn):
    '''This function creates the SongsData Table with the songs pulled from the list of tuples and sorts the data into the respective columns.'''
    cur.execute("CREATE TABLE IF NOT EXISTS SongsData (Song_Name TEXT PRIMARY KEY, Artist_Name TEXT, Number_Of_Streams INTEGER")
    cur.execute("SELECT * FROM SongsData")
    num = len(cur.fetchall())
    count = 0
    for elem in data:
        if count == 25:
            break
        if cur.execute("SELECT Song_Name FROM SongsData WHERE Song_Name = ?", (elem[0],)).fetchone() == None:
            cur.execute('INSERT INTO SongsData (Song_Name, Artist_Name, Number_Of_Streams) VALUES (?, ?, ?)', (elem[0], elem[1], elem[2]))
            num = num + 1
            count = count + 1
    conn.commit()