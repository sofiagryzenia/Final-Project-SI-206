import os
import sqlite3
import csv
import geopandas
from geopandas import GeoDataFrame
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import plotly.express as px
import geopandas as gpd

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


def events_visualization(cur,csvfile):

    
        ArtistNextEvent = pd.read_csv("ArtistNextEvent.csv")

        ArtistNextEvent.head()
               

        
        
        world = gpd.read_file(gpd.datasets.get_path('naturalearth_lowres'))
        world.plot(figsize=(18,10))
        plt.scatter(ArtistNextEvent.Longitude, ArtistNextEvent.Latitude, s=15, color="red", alpha=0.7)
        plt.xlabel("Longitude")
        plt.ylabel("Latitude")
        plt.title("Concert Locations from the Current Top 25 Artists")
        plt.show()

 








def main():
   
    cur, conn = setUpDatabase('finalprojDB.db')
    

    '''Calling all visualization functions.'''
    
    csvfile = "ArtistNextEvent.csv"
    events_visualization(cur,csvfile)


    cur.close()


if __name__ == "__main__":
    main()