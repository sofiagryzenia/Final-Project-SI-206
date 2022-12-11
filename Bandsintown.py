import json
import sqlite3
import os
import requests
from bs4 import BeautifulSoup



api_key = "222bf1b67a2801b6221b4cd60ca682a5"


def setUpDatabase(db_name):
    path = os.path.dirname(os.path.abspath(__file__))
    conn = sqlite3.connect(path+'/'+db_name)
    cur = conn.cursor()
    return cur, conn
 
def create_artists_table(cur,conn):


    artist_lst = ['Ed Sheeran', 'The Weeknd', 'Tones And I', 'Lewis Capaldi', 'Post Malone featuring 21 Savage', 'Post Malone and Swae Lee',
    'Drake featuring Wizkid and Kyla', 'The Chainsmokers featuring Halsey', 'Imagine Dragons', 'Shawn Mendes and Camila Cabello',
    'The Kid Laroi and Justin Bieber', 'Ed Sheeran', 'James Arthur', 'Billie Eilish', 'Glass Animals', 'Ed Sheeran',
    'Juice WRLD', 'Dua Lipa', 'The Weeknd featuring Daft Punk', 'Drake', 'Billie Eilish and Khalid', 'Harry Styles',
        'Ed Sheeran', 'Queen', 'The Chainsmokers and Coldplay', 'Lady Gaga and Bradley Cooper', 'XXXTentacion', 'Justin Bieber',
        'Post Malone', 'John Legend', 'Hozier', 'Imagine Dragons', 'The Neighbourhood', 'Ariana Grande', 'Travis Scott featuring Kendrick Lamar',
        'XXXTentacion', 'Camila Cabello featuring Young Thug', 'Lil Uzi Vert', 'Twenty One Pilots', 'Dua Lipa', 'Marshmello and Bastille',
        'Kendrick Lamar', 'OneRepublic', 'Travis Scott featuring Drake', 'Passenger', 'Avicii', 'Vance Joy', 'Justin Bieber',
            'The Weeknd', 'Major Lazer and DJ Snake featuring MØ', 'DJ Snake featuring Justin Bieber', 'Saint Jhn with Imanbek',
            'Macklemore & Ryan Lewis featuring Ray Dalton', 'Olivia Rodrigo', 'Post Malone', 'Calvin Harris and Dua Lipa',
            'Post Malone featuring Quavo', 'Alan Walker', 'Shawn Mendes', 'Olivia Rodrigo', 'Sam Smith', 'Harry Styles',
            'The Chainsmokers featuring Daya', 'Halsey', 'Mike Posner and Seeb', 'Mark Ronson featuring Bruno Mars',
                'Ed Sheeran and Justin Bieber', 'Maroon 5', 'Ariana Grande', 'Sam Smith', 'The Killers', 'Lil Nas X featuring Jack Harlow',
                'Imagine Dragons', 'Eminem', 'Luis Fonsi and Daddy Yankee featuring Justin Bieber', '24kGoldn and Iann Dior',
                'Dua Lipa featuring DaBaby', 'Lil Nas X', 'Bad Bunny and Jhay Cortez', 'French Montana featuring Swae Lee',
                'XXXTentacion', 'Roddy Ricch', 'BTS', 'Oasis', 'Arctic Monkeys', 'Bruno Mars', 'Sia featuring Sean Paul',
                    'Shawn Mendes', 'Eminem featuring Nate Dogg', 'Shawn Mendes', 'Wiz Khalifa featuring Charlie Puth', 'Lauv',
                    'Maroon 5 featuring Cardi B [B]', 'Lukas Graham', 'Luis Fonsi featuring Daddy Yankee', 'Jason Mraz', 'J. Cole',
                    'DaBaby featuring Roddy Ricch', 'Nirvana', 'Maroon 5']

    cur.execute("DROP TABLE IF EXISTS artist_info")
    cur.execute("CREATE TABLE artist_info (id INTEGER PRIMARY KEY, title TEXT)")
    for i in range(len(artist_lst)):
        cur.execute("INSERT INTO artist_info (id,title) VALUES (?,?)",(i,artist_lst[i]))
    conn.commit()



def get_events_info(artist_lst):
     
     for name in artist_lst:
        if " " in name:
            name = name.replace(" ", "%20")

        url = f"https://rest.bandsintown.com/artists/{name}/events?app_id={api_key}&date=2022-12-13,2023-12-9"
        r = requests.get(url)
        js = json.loads(r.text)
        upcoming_event_count = len(js)
        data = []
        
        index = 0
        name = name.replace("%20", " ")

        if js != []:
        
            #try:
            for elem in js:

                location = elem["venue"]["location"]
                venue = elem["venue"]["name"]
                date_and_time = elem["starts_at"]
                #upcoming_event_count = elem["artist"]["upcoming_event_count"]
                #name = elem["name"]
                ticket_url = elem["offers"][0]["url"]

                data.append((name,upcoming_event_count,venue,location,date_and_time,ticket_url))
                

            #except:
                #print("exception")
        #print(data)
        return data

def add_info_to_table(cur,conn,data):
    
    count = 1
    check = 0
    for i in data:
        artist_id = count
        upcoming_events = i[1]
        name = i[0]
        if upcoming_events > 0:
            venue = data[2]
            location = data[3]
            date_and_time = data[4]
            ticket_url = data[5]
        else:
            venue = "N/A"
            location = "N/A"
            date_and_time = "N/A"
            ticket_url = "N/A"
        
    for elem in data:
        if check == 25:
            break
        cur.execute('INSERT INTO artist_info (artist_id, name, upcoming_events, venue, location, date_and_time, ticket_url) VALUES (?,?,?,?,?,?,?)', (artist_id, name, upcoming_events, venue, location, date_and_time, ticket_url))

        count += 1
    conn.commit()

def main():
    
    artist_lst = ['Ed Sheeran', 'The Weeknd', 'Tones And I', 'Lewis Capaldi', 'Post Malone featuring 21 Savage', 'Post Malone and Swae Lee',
    'Drake featuring Wizkid and Kyla', 'The Chainsmokers featuring Halsey', 'Imagine Dragons', 'Shawn Mendes and Camila Cabello',
    'The Kid Laroi and Justin Bieber', 'Ed Sheeran', 'James Arthur', 'Billie Eilish', 'Glass Animals', 'Ed Sheeran',
    'Juice WRLD', 'Dua Lipa', 'The Weeknd featuring Daft Punk', 'Drake', 'Billie Eilish and Khalid', 'Harry Styles',
        'Ed Sheeran', 'Queen', 'The Chainsmokers and Coldplay', 'Lady Gaga and Bradley Cooper', 'XXXTentacion', 'Justin Bieber',
        'Post Malone', 'John Legend', 'Hozier', 'Imagine Dragons', 'The Neighbourhood', 'Ariana Grande', 'Travis Scott featuring Kendrick Lamar',
        'XXXTentacion', 'Camila Cabello featuring Young Thug', 'Lil Uzi Vert', 'Twenty One Pilots', 'Dua Lipa', 'Marshmello and Bastille',
        'Kendrick Lamar', 'OneRepublic', 'Travis Scott featuring Drake', 'Passenger', 'Avicii', 'Vance Joy', 'Justin Bieber',
            'The Weeknd', 'Major Lazer and DJ Snake featuring MØ', 'DJ Snake featuring Justin Bieber', 'Saint Jhn with Imanbek',
            'Macklemore & Ryan Lewis featuring Ray Dalton', 'Olivia Rodrigo', 'Post Malone', 'Calvin Harris and Dua Lipa',
            'Post Malone featuring Quavo', 'Alan Walker', 'Shawn Mendes', 'Olivia Rodrigo', 'Sam Smith', 'Harry Styles',
            'The Chainsmokers featuring Daya', 'Halsey', 'Mike Posner and Seeb', 'Mark Ronson featuring Bruno Mars',
                'Ed Sheeran and Justin Bieber', 'Maroon 5', 'Ariana Grande', 'Sam Smith', 'The Killers', 'Lil Nas X featuring Jack Harlow',
                'Imagine Dragons', 'Eminem', 'Luis Fonsi and Daddy Yankee featuring Justin Bieber', '24kGoldn and Iann Dior',
                'Dua Lipa featuring DaBaby', 'Lil Nas X', 'Bad Bunny and Jhay Cortez', 'French Montana featuring Swae Lee',
                'XXXTentacion', 'Roddy Ricch', 'BTS', 'Oasis', 'Arctic Monkeys', 'Bruno Mars', 'Sia featuring Sean Paul',
                    'Shawn Mendes', 'Eminem featuring Nate Dogg', 'Shawn Mendes', 'Wiz Khalifa featuring Charlie Puth', 'Lauv',
                    'Maroon 5 featuring Cardi B [B]', 'Lukas Graham', 'Luis Fonsi featuring Daddy Yankee', 'Jason Mraz', 'J. Cole',
                    'DaBaby featuring Roddy Ricch', 'Nirvana', 'Maroon 5']

    
    cur, conn = setUpDatabase('finalprojDB.db')



    data = get_events_info(artist_lst)

    add_info_to_table(cur,conn,data)
 

    



if __name__ == "__main__":
    main()

