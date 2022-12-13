import os
import sqlite3
import csv
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import plotly.express as px
import geopandas as gpd


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

 
def streams_visualzation(cur,csvfile):
    
    data = pd.read_csv("TotalTopStreams.csv")
    
    df = pd.DataFrame(data)

    X = list(df.iloc[:, 0])

    Y = list(df.iloc[:, 1])

    plt.bar(X, Y, color='midnightblue')
    plt.title("Total Streams for Top 25 Artists")
    plt.xlabel("Artist Name")
    plt.ylabel("Number of Streams in Billions")
   
    plt.xticks(rotation=50,fontsize=4)
    
    
    plt.show()

    







def main():
   
    cur, conn = setUpDatabase('finalprojDB.db')
    

    '''Calling all visualization functions.'''
    
    csvfile = "ArtistNextEvent.csv"
    events_visualization(cur,csvfile)

    csvfile = "TotalTopStreams.csv"
    streams_visualzation(cur,csvfile)
    cur.close()


if __name__ == "__main__":
    main()