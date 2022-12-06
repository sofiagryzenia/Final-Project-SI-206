import json
import requests
import sqlite3
import os
import csv


client_id = "5b023ed3b67b4648a542d812ee5974f4"
client_secret = "5b3c316393c74cef8ab027e096757142"
url = 'https//accounts.spotify.com/api/token'


def open_database(db_name):
    path = os.path.dirname(os.path.abspath(__file__))
    conn = sqlite3.connect(path+'/'+db_name)
    cur = conn.cursor()
    return cur, conn

def read_json(cache_filename):
    
    try:
        with open(cache_filename, 'r', encoding="utf-8") as file: 
            return json.loads(file.read())
    
    except:
        empty_dict= {}
        return empty_dict
    

def write_json(cache_filename, dict):
    
    with open (cache_filename, "w") as f:
        f.write(json.dumps(dict))
        

def get_request_url(list):
    
    # example url = f"https://api.nytimes.com/svc/books/v3/lists/2016-07-10/{list}?api-key={API_KEY}"
    return url

def get_data_using_cache(list, cache_filename):
    
    
    json_dict = read_json(cache_filename)
    url = get_request_url(list)
    if url in json_dict:
        print("Using cache for " + list)
        return json_dict[url]
    else:
        try:
            print("Fetching data for " + list)
            r = requests.get(url)
            js = json.loads(r.text)
            if js["status"] == "OK":
                json_dict[url] = js["results"]
                write_json(cache_filename,json_dict)
                return json_dict
            else:
                print("No list found for list name provided")
                return None
        except:
            print("Exception")
            return None






def access_token():
    
    AUTH_URL = 'https://accounts.spotify.com/api/token'
    
    BASE_URL = 'https://api.spotify.com/v1/'


    # POST
    auth_response = requests.post(AUTH_URL, {
        'grant_type': 'client_credentials',
        'client_id': client_id,
        'client_secret': client_secret,
    })

    # convert the response to JSON
    auth_response_data = auth_response.json()

    # save the access token
    access_token = auth_response_data['access_token']

    headers = {
    'Authorization': 'Bearer {token}'.format(token=access_token)
}
    artist_id = '36QJpDe2go2KgaRleHCDTp'

    # pull all artists albums
    r = requests.get(BASE_URL + 'artists/' + artist_id + '/albums', 
                    headers=headers, 
                    params={'include_groups': 'album', 'limit': 50})
    d = r.json()    
    print(d)


def get_data(header):
    pass
    
   





def main():
    
    cache_filename = dir_path + '/' + "cache_spotify.json"

    dir_path = os.path.dirname(os.path.realpath(__file__))
    
    cur, conn = open_database('finalprojDB.db')
    
    # make_types_table(json_data, cur, conn)

if __name__ == "__main__":
    main()