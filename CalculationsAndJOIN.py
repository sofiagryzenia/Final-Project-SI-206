#Calculations and JOIN
import sqlite3
import os
import csv


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


def calcTWO(cur, conn, filepath):


defcalcTHREE(cur, conn, filepath):