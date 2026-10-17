import os 
import requests 
from db_connection import save
from db_connection import view_db

def fetch_and_save(playlist_id):

    url = "https://www.googleapis.com/youtube/v3/playlistItems?part=snippet&playlistId="

    url += (playlist_id + "&" + f"key={key}&")

    url += "maxResults=50"

    #print(url)
    
    try:
        response = requests.get(url, timeout=5)

        if response.status_code == 200:

            data = response.json()

            playlist_items = data["items"]

            vids = {}

            for item in playlist_items:

                snippet = item["snippet"]

                video_id = snippet["resourceId"]["videoId"]

                title = snippet["title"]

                vids[video_id] = title 

            save(playlist_id, vids)


        else: 

            print(f"An error occurred during request: {response.status_code}")

    except requests.exceptions.RequestException as e:

        print(f"Something went wrong: {e}") 




PROJECT_ROOT = os.path.dirname(os.path.abspath(__file__))

key_path = os.path.join(PROJECT_ROOT, "key.txt") 

with open(key_path, "r") as file:

    key = file.read().strip() 

#print(key) 


choice = input("1) Fetch a playlist\n2) View saved playlists\n")


while choice != "1" and choice !="2":

    print("Not a valid choice, try again\n") 

    choice = input("1) Fetch a playlist\n2) View saved playlists\n")


if choice == "1":

    playlist_id = input("Enter the playlist's ID: ")

    fetch_and_save(playlist_id)
                    
else:

    view_db() 




