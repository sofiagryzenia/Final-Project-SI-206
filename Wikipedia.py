from bs4 import BeautifulSoup
import requests

URL = 'https://en.wikipedia.org/wiki/List_of_most-streamed_songs_on_Spotify'

headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/107.0.0.0 Safari/537.36'}
page = requests.get(URL, headers=headers)

firstsoup = BeautifulSoup(page.content, 'html.parser')
soup = BeautifulSoup(firstsoup.prettify(),'html.parser')


song_ranking = []
for i in range (0,100):
    rank = soup.find_all('th', attrs = {'style': 'text-align:center;'})[i].text
    rank = rank.replace('\n','')
    rank = rank.strip()
    song_ranking.append(rank)

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
    'Rank' : song_ranking,
    'Song' : song_list,
    'Streams' : streams_list,
    'Artist' : artist_list,
}

print(data)




