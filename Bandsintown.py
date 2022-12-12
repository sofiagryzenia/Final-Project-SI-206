import json
import sqlite3
import os
import requests




api_key = "222bf1b67a2801b6221b4cd60ca682a5"

artist_lst = ['Ed Sheeran', 'The Weeknd', 'Tones And I', 'Lewis Capaldi', 'Post Malone', 'Camila Cabello',
    'Drake', 'The Chainsmokers', 'Imagine Dragons', 'Shawn Mendes',
    'The Kid Laroi', 'Ed Sheeran', 'James Arthur', 'Billie Eilish', 'Glass Animals', 'Ed Sheeran',
    'Juice WRLD', 'Dua Lipa', 'The Weeknd', 'Drake', 'Billie Eilish', 'Harry Styles',
        'Ed Sheeran', 'Queen', 'The Chainsmokers', 'Lady Gaga', 'XXXTentacion', 'Justin Bieber',
        'Post Malone', 'John Legend', 'Hozier', 'Imagine Dragons', 'The Neighbourhood', 'Ariana Grande', 'Travis Scott',
        'XXXTentacion', 'Camila Cabello', 'Lil Uzi Vert', 'Twenty One Pilots', 'Dua Lipa', 'Marshmello',
        'Kendrick Lamar', 'OneRepublic', 'Travis Scott', 'Passenger', 'Avicii', 'Vance Joy', 'Justin Bieber',
            'The Weeknd', 'Major Lazer', 'DJ Snake', 'Saint Jhn',
            'Macklemore', 'Olivia Rodrigo', 'Post Malone', 'Calvin Harris',
            'Post Malone', 'Alan Walker', 'Shawn Mendes', 'Olivia Rodrigo', 'Sam Smith', 'Harry Styles',
            'The Chainsmokers', 'Halsey', 'Mike Posner', 'Mark Ronson featuring Bruno Mars',
                'Ed Sheeran', 'Maroon 5', 'Ariana Grande', 'Sam Smith', 'The Killers', 'Lil Nas X',
                'Imagine Dragons', 'Eminem', 'Luis Fonsi', '24kGoldn',
                'Dua Lipa', 'Lil Nas X', 'Bad Bunny', 'French Montana',
                'XXXTentacion', 'Roddy Ricch', 'BTS', 'Oasis', 'Arctic Monkeys', 'Bruno Mars', 'Sia',
                    'Shawn Mendes', 'Eminem', 'Shawn Mendes', 'Wiz Khalifa', 'Lauv',
                    'Maroon 5', 'Lukas Graham', 'Luis Fonsi', 'Jason Mraz', 'J. Cole',
                    'DaBaby', 'Nirvana', 'Maroon 5']


def setUpDatabase(db_name):
    path = os.path.dirname(os.path.abspath(__file__))
    conn = sqlite3.connect(path+'/'+db_name)
    cur = conn.cursor()
    return cur, conn




def get_events_info(artist_lst):
     


    for i in range(len(artist_lst)):
 
        if " " in artist_lst[i]:
            artist_lst[i] = artist_lst[i].replace(" ", "%20")

        url = f"https://rest.bandsintown.com/artists/{artist_lst[i]}/events?app_id={api_key}&date=2022-12-13,2023-12-9"
        r = requests.get(url)
        js = json.loads(r.text)

        
        upcoming_event_count = len(js)
        
        data = []
 
        artist_lst[i] = artist_lst[i].replace("%20", " ")

        location_lst = []
        #print(js)
        if js != []:
            for elem in js:

                location = elem["venue"]["location"]
                location_lst.append(location)
                venue = elem["venue"]["name"]
                date_and_time = elem["starts_at"]
                ticket_url = elem["offers"]
                for offer in ticket_url:
                    url = offer["url"]

                data.append((artist_lst[i],upcoming_event_count,venue,location,date_and_time,ticket_url))
  
        if data:
            #print(data[0])
            return data[0]
    


    
def create_artists_table(cur,conn,data,artist_lst):




    cur.execute("CREATE TABLE IF NOT EXISTS artist_info (id INTEGER PRIMARY KEY, name TEXT, upcoming_events INTEGER, venue TEXT, location TEXT, date_and_time TEXT, ticket_url TEXT)")
  
    conn.commit()
    
    count = 1
    check = 0

    for i in range(len(data)):

        artist_id = count
        upcoming_events = data[1]
        print(upcoming_events)
        name = data[0]
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
        for i in range(len(artist_lst)):

            cur.execute('INSERT OR IGNORE INTO artist_info (id, name, upcoming_events, venue, location, date_and_time, ticket_url) VALUES (?,?,?,?,?,?,?)', (int(count), str(artist_lst[i]), int(upcoming_events), str(venue), str(location), str(date_and_time), str(ticket_url)))

        count += 1
    conn.commit()

def main():
    
    artist_lst = ['Ed Sheeran', 'The Weeknd', 'Tones And I', 'Lewis Capaldi', 'Post Malone', 'Camila Cabello',
    'Drake', 'The Chainsmokers', 'Imagine Dragons', 'Shawn Mendes',
    'The Kid Laroi', 'Ed Sheeran', 'James Arthur', 'Billie Eilish', 'Glass Animals', 'Ed Sheeran',
    'Juice WRLD', 'Dua Lipa', 'The Weeknd', 'Drake', 'Billie Eilish', 'Harry Styles',
        'Ed Sheeran', 'Queen', 'The Chainsmokers', 'Lady Gaga', 'XXXTentacion', 'Justin Bieber',
        'Post Malone', 'John Legend', 'Hozier', 'Imagine Dragons', 'The Neighbourhood', 'Ariana Grande', 'Travis Scott',
        'XXXTentacion', 'Camila Cabello', 'Lil Uzi Vert', 'Twenty One Pilots', 'Dua Lipa', 'Marshmello',
        'Kendrick Lamar', 'OneRepublic', 'Travis Scott', 'Passenger', 'Avicii', 'Vance Joy', 'Justin Bieber',
            'The Weeknd', 'Major Lazer', 'DJ Snake', 'Saint Jhn',
            'Macklemore', 'Olivia Rodrigo', 'Post Malone', 'Calvin Harris',
            'Post Malone', 'Alan Walker', 'Shawn Mendes', 'Olivia Rodrigo', 'Sam Smith', 'Harry Styles',
            'The Chainsmokers', 'Halsey', 'Mike Posner', 'Mark Ronson featuring Bruno Mars',
                'Ed Sheeran', 'Maroon 5', 'Ariana Grande', 'Sam Smith', 'The Killers', 'Lil Nas X',
                'Imagine Dragons', 'Eminem', 'Luis Fonsi', '24kGoldn',
                'Dua Lipa', 'Lil Nas X', 'Bad Bunny', 'French Montana',
                'XXXTentacion', 'Roddy Ricch', 'BTS', 'Oasis', 'Arctic Monkeys', 'Bruno Mars', 'Sia',
                    'Shawn Mendes', 'Eminem', 'Shawn Mendes', 'Wiz Khalifa', 'Lauv',
                    'Maroon 5', 'Lukas Graham', 'Luis Fonsi', 'Jason Mraz', 'J. Cole',
                    'DaBaby', 'Nirvana', 'Maroon 5'] # and Coldplay,  and Bradley Cooper featuring Kendrick Lamar  featuring Young Thug featuring DaBaby, jack harlow, cardi b, roddy richh, and Bastille

    
    cur, conn = setUpDatabase('finalprojDB.db')

    data = get_events_info(artist_lst)

    create_artists_table(cur,conn,data,artist_lst)
    cur.close()

 

    



if __name__ == "__main__":
    main()

