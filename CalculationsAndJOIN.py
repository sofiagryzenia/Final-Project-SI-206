#Calculations and JOIN
import sqlite3
import os
import csv
from  geopy.geocoders import Nominatim
geolocator = Nominatim(user_agent="Sofia")


'''––––––––––––––––––––––––––––––––––––––––––––––––––––––––––– DB: Function to set up a database –––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––'''
def setUpDatabase(db_name):
    '''This function will create a database named after the string input into the function.'''

    path = os.path.dirname(os.path.abspath(__file__))
    conn = sqlite3.connect(path+'/'+db_name)
    cur = conn.cursor()
    return cur, conn


'''–––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––– CALCULATIONS ––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––'''
#here are where calcs are need to rename/do
def calcONE(cur, conn, filepath):


    cur.execute('SELECT artist_info.id, artist_info.name, artist_info.upcoming_events, artist_info.location FROM artist_info')
    data = cur.fetchall()
    conn.commit()


    popularity_lst = []
    for tup in data: 
        popularity_lst.append(tup[0])

    artist_lst = []
    for tup in data: 
        artist_lst.append(tup[1])
    
    upcoming_events_count_lst = []
    for tup in data: 
        upcoming_events_count_lst.append(tup[2])
    
    
    loc_lst = []
    city_lst = []
    state_and_county_lst = []
    for tup in data: 
        loc_lst.append(tup[3])
  
            
    for location in loc_lst:
        city = location.split(',')[0]
        final_city = city.replace("['",'')
        city_lst.append(final_city)
        
        state_or_country = location.split(',')[1]
        state_or_country_final = state_or_country.replace("']",'')
        final_state_country = state_or_country_final.replace("'","")
        state_and_county_lst.append(final_state_country)

    
    lat_lst = []
    lon_lst = []
    for city in city_lst:
        geolocator = Nominatim(user_agent="Sofia")
        location = geolocator.geocode(city)
        y = location.longitude
        x =  location.latitude
        lat_lst.append(y)
        lon_lst.append(x)
            
    with open(filepath, 'w', newline = '', encoding= 'utf-8') as f: 
        f = csv.writer(f, delimiter = ',')
        f.writerow(['Artist Ranking', 'Aritst Name', 'Upcoming Event Count','Next Event City','Next Event State or Country', 'Latitude', 'Longitude'])

        
        for index in range(len(popularity_lst)):
            write = (popularity_lst[index], artist_lst[index], upcoming_events_count_lst[index],city_lst[index],state_and_county_lst[index],lon_lst[index],lat_lst[index])
            f.writerow(write)
    

def calcTWO(cur, conn, filepath):

    # Fetch the data from the database
    data = cur.execute('SELECT Song_Streams, Song_Name, Artist_Name FROM WikiSongsData').fetchall()
    conn.commit()
    # Create an empty dictionary to store the artist stream data
    artist_streams = {}

    # Loop through the data and add the corresponding number of streams for each song to the appropriate artist's entry in the dictionary
    for row in data:
        streams, song, artist = row
        if artist not in artist_streams:
            artist_streams[artist] = 0
        artist_streams[artist] += streams

    # Open the CSV file for writing
    with open(filepath, 'w', newline='') as csvfile:
        writer = csv.writer(csvfile)

        # Write the header row
        writer.writerow(['Artist', 'Number of Streams (in billions)'])

        # Loop through the dictionary and write each artist's data to the CSV file
        for artist, streams in artist_streams.items():
            # Convert the number of streams from millions to billions
            num_streams_in_billions = streams / 1000000000
            writer.writerow([artist, num_streams_in_billions])

def calcTHREE(cur, conn, filepath):
    
    data = cur.execute('SELECT WikiSongsData.Song_Streams, WikiSongsData.Song_Name, WikiSongsData.Artist_Name FROM WikiSongsData').fetchall()

    conn.commit()

    #print(data)
    streams_lst = []
    for tup in data: 
        streams_lst.append(tup[0])


    songs_lst = []
    for tup in data: 
        songs_lst.append(tup[1])
    
    artists_lst = []
    for tup in data: 
        artists_lst.append(tup[2])
    
    artist_streams_dict = {}

    for i in range(len(artists_lst)):

        if artists_lst[i] not in artist_streams_dict:
            artist_streams_dict[artists_lst[i]] = streams_lst[i]
        else:
            artist_streams_dict[artists_lst[i]] += streams_lst[i]

    sorted_streams = sorted(artist_streams_dict.items(), key=lambda x:x[1],reverse=True)
    #print(len(sorted_streams))
    #sorted_final = {}
    #for value in sorted_streams:
        #new_val = round(value[1],2)

    with open(filepath, 'w', newline = '', encoding= 'utf-8') as f: 
        f = csv.writer(f, delimiter = ',')
        f.writerow(['Artist Name','Streams'])

        
        for index in range(len(sorted_streams)):
            write = (sorted_streams[index])
            f.writerow(write)
    

def joinData(cur, conn):
    cur.execute("SELECT Quality_of_Life, Average_Annual_Salary, Population FROM CitiesData JOIN RestaurantCities ON trim(CitiesData.City_Name) = trim(RestaurantCities.Cities)")
    joined = cur.fetchall()
    for x in joined: 
        print(x)
    conn.commit()


def main():
   
    cur, conn = setUpDatabase('finalprojDB.db')
    

    calcONE(cur, conn, "ArtistNextEvent.csv")

    calcTWO(cur, conn, "SongPopularity.csv")

    calcTHREE(cur, conn, "TotalTopStreams.csv")

    '''Calling the JOIN statement function.'''
    joinData(cur, conn)

    cur.close()


if __name__ == "__main__":
    main()