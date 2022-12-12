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
    '''This function will create a database named after the string input into the function.'''
    #create a database
    path = os.path.dirname(os.path.abspath(__file__))
    conn = sqlite3.connect(path+'/'+db_name)
    cur = conn.cursor()
    return cur, conn

'''––––––––––––––––– SONGS BEAUTIFUL SOUP: Pulling data from Wikipedia using Beautiful Soup and putting it into the SongsData table ––––––––––––––––––––'''

def getSongs():
    '''This function pulls data from Wikipedia using Beautiful Soup 
    and returns a list of tuples containing top 100 songs, their rank, number of streams, and artist.'''
    URL = 'https://en.wikipedia.org/wiki/List_of_most-streamed_songs_on_Spotify'

    headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/107.0.0.0 Safari/537.36'}
    page = requests.get(URL, headers=headers)

    soup = BeautifulSoup(page.content, 'html.parser')


    topSongs = []
    table = soup.find_all('tbody')[0]
    for row in table.find_all("tr")[1:-1]:
        rank = row.find('th').text
        streams = row.find_all('td')[1].text
        song = row.find_all('td')[0].text
        artist = row.find_all('td')[2].text
        topSongs.append((int(rank), float(streams), song, artist))

    return topSongs


def setUpSongsTable(data, cur, conn):

    '''Funtion to create the WikiSongsData table with the songs pulled from the list of tuples and sorts the data into columns.'''

    cur.execute("CREATE TABLE IF NOT EXISTS WikiSongsData (Song_Rank INTEGER, Song_Streams FLOAT, Song_Name TEXT, Artist_Name TEXT)")
    cur.execute("SELECT * FROM WikiSongsData")
    num = len(cur.fetchall())
    count = 0
    for elem in data:
        if count == 25:
            break
        if cur.execute("SELECT Song_Name FROM WikiSongsData WHERE Song_Name = ?", (elem[1],)).fetchone() == None:#Not properly checking if item in DB
            cur.execute('INSERT INTO WikiSongsData (Song_Rank, Song_Streams, Song_Name, Artist_Name) VALUES (?, ?, ?, ?)', (elem[0], elem[1], elem[2], elem[3]))
            num = num + 1
            count = count + 1
    conn.commit()

'''–––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––– MAIN –––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––'''
def main():
    '''The main function calls the function to set up the database, sets up the WikiSongsData table, SpotifySongData table, and artist_info table. 
    It calls all the visualization functions, calculation functions, and the JOIN statement.'''
    cur, conn = setUpDatabase('finalprojDB.db')
    


    '''Calling the getSongs function and setUpSongsTable using Beautiful Soup on Wikipedia.'''
    data = getSongs()
    setUpSongsTable(data, cur, conn)


    cur.close()


if __name__ == "__main__":
    main()
