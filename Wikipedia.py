from bs4 import BeautifulSoup
import requests

URL = 'https://en.wikipedia.org/wiki/List_of_most-streamed_songs_on_Spotify'

headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/107.0.0.0 Safari/537.36'}
page = requests.get(URL, headers=headers)

soup1 = BeautifulSoup(page.content, 'html.parser')
soup2 = BeautifulSoup(soup1.prettify(),'html.parser')

print(soup2)

