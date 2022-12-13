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
   
    plt.xticks(rotation=50,fontsize=4,weight='bold')
    
    
    plt.show()

def num_concerts_visualzation(cur,csvfile):
    
    data = pd.read_csv("ArtistNextEvent.csv")

    data.head()
    
    df = pd.DataFrame(data)
    X = list(df.iloc[:, 1])
    Y = list(df.iloc[:, 2])



    plt.bar(X, Y, color='purple')
    plt.title("Num of Concerts For Top 18 Artists From 2022-12-13,2023-12-9",weight='bold')
    plt.xlabel("Artist Name")
    plt.ylabel("Num of Concerts in the next year")
   
    plt.xticks(rotation=50,fontsize=7,weight='bold')
    
    
    plt.show()


def billions(cur, csvfile):
   
    data = pd.read_csv("SongPopularity.csv")

    
    artists = []
    num_streams = []

    
    for i in range(data.shape[0]):
        artist = data.iloc[i, 0]
        streams = data.iloc[i, 1]
        artists.append(artist)
        num_streams.append(int(streams))

    
    plt.bar(artists, num_streams, color='blue')
    plt.xlabel('Artist')
    plt.ylabel('Number of Streams (in billions)')

    
    plt.show()











    







def main():
   
    cur, conn = setUpDatabase('finalprojDB.db')
    

    '''Calling all visualization functions.'''
    
    csvfile = "ArtistNextEvent.csv"
    events_visualization(cur,csvfile)

    csvfile = "TotalTopStreams.csv"
    streams_visualzation(cur,csvfile)
    cur.close()
    
    csvfile = "ArtistNextEvent.csv"
    num_concerts_visualzation(cur,csvfile)

    csvfile = "SongPopularity.csv"
    billions(cur,csvfile)

if __name__ == "__main__":
    main()