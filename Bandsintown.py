import json
import unittest
import os
import requests


api_key = "222bf1b67a2801b6221b4cd60ca682a5"


def get_events_info(artist_name):
    
    url = f"https://rest.bandsintown.com/artists/{artist_name}/events/?app_id={api_key}"

    return url

def main():
    get_events_info("Taylor Swift")



if __name__ == "__main__":
    main()
