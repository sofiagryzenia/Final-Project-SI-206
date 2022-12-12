import os
import sqlite3

import geopandas
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

import warnings

warnings.filterwarnings('ignore')


geopandas.datasets.available

from  geopy.geocoders import Nominatim
geolocator = Nominatim(user_agent="Sofia")


def setUpDatabase(db_name):
    path = os.path.dirname(os.path.abspath(__file__))
    conn = sqlite3.connect(path+'/'+db_name)
    cur = conn.cursor()
    return cur, conn


def events_visualization(cur):

    location_lst = []
    loc_lst = []
    resultList = []

    data = cur.execute("SELECT * FROM artist_info").fetchall()
    
    format_dict = {}
    final_dict = {}

    for item in data:
        name = item[1]
        locations = item[4]
        loc = locations.split(',')[0]
        loc = loc.replace("['",'')
        loc_lst.append(loc)
    for l in loc_lst:

        geolocator = Nominatim(user_agent="Sofia")
        location = geolocator.geocode(l)
        #print(location.address)
        #print((location.latitude, location.longitude))

    
    cities = format_dict.values()
    world = geopandas.read_file(geopandas.datasets.get_path("naturalearth_cities"))
    world.geometry.name
    world.shape
    world.head()
    with plt.style.context(("seaborn", "ggplot")):
        world.plot(figsize=(18,10),
                color="white",
                edgecolor = "grey")

        x = location.latitude
        y = location.longitude
        plt.scatter(plt.scatter(x, y, s=15, color="red", alpha=0.3))
        plt.xlabel("Longitude")
        plt.ylabel("Latitude")
        plt.title("Concert Locations from the Top 100 Artists Currently")
        
    
        geo_data = cities.groupby("City").mean()
        cnts = cities.groupby("City").count()[["City"]].rename(columns={"City":"Count"})
        cnts = geo_data.join(cnts).sort_values(by=["Count"], ascending=False)
        cnts = cnts[cnts["Count"]>10]
        cnts.head()
        plt.show()







def main():
   
    cur, conn = setUpDatabase('finalprojDB.db')
    

    '''Calling all visualization functions.'''
    
    events_visualization(cur)


    cur.close()


if __name__ == "__main__":
    main()