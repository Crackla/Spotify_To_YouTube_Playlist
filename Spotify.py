from spotipy.oauth2 import SpotifyOAuth
import spotipy
import sys
import os


sp = spotipy.Spotify(auth_manager=SpotifyOAuth(client_id="8ed0d1e51d0f476a923e6811621cbfe0",
                                               client_secret="a0461fdf929a49a9a4356592f02ab027",
                                               redirect_uri="http://localhost:8080",
                                               scope="playlist-read-private"))

if os.path.exists("output.txt"):
    os.remove("output.txt")

playlist_id = "3TvifVpEro6FJ1vTD4LVfB"
results = sp.playlist_items(playlist_id, fields=None, limit=100, offset=0, additional_types=("track", ))
for idx, item in enumerate(results["items"]):
    track = item["track"]
    file = open("output.txt", "a")
    sys.stdout = file
    print(track["artists"][0]["name"], track["name"])
    file.close()
