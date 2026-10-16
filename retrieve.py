import os 
import requests 


PROJECT_ROOT = os.path.dirname(os.path.abspath(__file__))

key_path = os.path.join(PROJECT_ROOT, "key.txt") 

with open(key_path, "r") as file:

    key = file.read().strip() 

#print(key) 

url = "https://www.googleapis.com/youtube/v3/playlistItems?part=snippet&playlistId="

playlist_id = input("Enter the Playlist ID: ") 

url += (playlist_id + "&" + f"key={key}")

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

        print(vids)

    else: 

        print(f"An error occurred during request: {response.status_code}")

except requests.exceptions.RequestException as e:

    print(f"Something went wrong: {e}") 

