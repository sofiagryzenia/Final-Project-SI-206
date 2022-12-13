import os
import sqlite3
import csv
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import plotly.express as px


def setUpDatabase(db_name):
    path = os.path.dirname(os.path.abspath(__file__))
    conn = sqlite3.connect(path+'/'+db_name)
    cur = conn.cursor()
    return cur, conn





def billions(curr, csvfile):
   
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
    

  

    csvfile = "SongPopularity.csv"
    billions(cur,csvfile)

if __name__ == "__main__":
    main()