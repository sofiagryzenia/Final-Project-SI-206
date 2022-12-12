import json
import sqlite3
import os
import requests
from bs4 import BeautifulSoup
import requests

api_key = "222bf1b67a2801b6221b4cd60ca682a5"


def get_artist_lst():
    
    url = 'https://kworb.net/itunes/'

    artist_lst = []

    r = requests.get(url)
    soup = BeautifulSoup(r.content, "html.parser")
    a = soup.find_all('a')
    for tag in a:
        tag = tag.text
        artist_lst.append(tag)

    artist_lst = artist_lst[14:114]
    return artist_lst




def setUpDatabase(db_name):
    path = os.path.dirname(os.path.abspath(__file__))
    conn = sqlite3.connect(path+'/'+db_name)
    cur = conn.cursor()
    return cur, conn




def get_events_info(artist_lst):
    
    global data
    data = []
    for i in range(len(artist_lst)):
        
 
        if " " in artist_lst[i]:
            artist_lst[i] = artist_lst[i].replace(" ", "%20")

        url = f"https://rest.bandsintown.com/artists/{artist_lst[i]}/events?app_id={api_key}&date=2022-12-13,2023-12-9"
        r = requests.get(url)
        js = json.loads(r.text)

        
        upcoming_event_count = len(js)
        
        
 
        artist_lst[i] = artist_lst[i].replace("%20", " ")

        location_lst = []
        venue_lst = []
        date_and_time_lst = []
        ticket_url_lst = []
        #print(js)
        if js != []:
            for elem in js:
              

                location = elem["venue"]["location"]
                location_lst.append(location)
                venue = elem["venue"]["name"]
                venue_lst.append(venue)
                date_and_time = elem["starts_at"]
                date_and_time_lst.append(date_and_time)
                ticket_url = elem["offers"]
                
                for offer in ticket_url:
                    url = offer["url"]
                    ticket_url_lst.append(url)

            data.append((artist_lst[i],upcoming_event_count,venue_lst,location_lst,date_and_time_lst,ticket_url_lst))

        if i == 99:
            return data
    


    
def create_artists_table(cur,conn,data,artist_lst):

   
    #print(data)

    cur.execute('DROP TABLE IF EXISTS artist_info')
    cur.execute("CREATE TABLE IF NOT EXISTS artist_info (id INTEGER PRIMARY KEY, name TEXT, upcoming_events INTEGER, venue TEXT, location TEXT, date_and_time TEXT, ticket_url TEXT)")
  
    conn.commit()
    
    count = 1
   
    
    
    for i in range(len(data)):

        artist_id = count
        upcoming_events = data[i][1]
        name = data[i][0]

        if upcoming_events > 0:
            venue = data[i][2]
            location = data[i][3]
            date_and_time = data[i][4]
            ticket_url = data[i][5]
        else:
            venue = "N/A"
            location = "N/A"
            date_and_time = "N/A"
            ticket_url = "N/A"
  
    #for elem in data:
        if i == 25:
            break
        #for i in range(len(artist_lst)):

        cur.execute('INSERT OR IGNORE INTO artist_info (id, name, upcoming_events, venue, location, date_and_time, ticket_url) VALUES (?,?,?,?,?,?,?)', (int(count), str(artist_lst[i]), int(upcoming_events), str(venue), str(location), str(date_and_time), str(ticket_url)))

        count += 1
    conn.commit()


def main():
    
    artist_lst = get_artist_lst()

    
    cur, conn = setUpDatabase('finalprojDB.db')

    data = get_events_info(artist_lst)

    create_artists_table(cur,conn,data,artist_lst)
    cur.close()

 

    



if __name__ == "__main__":
    main()

