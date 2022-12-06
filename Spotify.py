import json
import requests
import sqlite3
import os
import csv


client_id = "5b023ed3b67b4648a542d812ee5974f4"
client_secret = "5b3c316393c74cef8ab027e096757142"



def open_database(db_name):
    path = os.path.dirname(os.path.abspath(__file__))
    conn = sqlite3.connect(path+'/'+db_name)
    cur = conn.cursor()
    return cur, conn




def get_data(header):
    pass
    
   





def main():
    
    
    dir_path = os.path.dirname(os.path.realpath(__file__))
    
    cur, conn = open_database('spotify.db')
    


if __name__ == "__main__":
    main()