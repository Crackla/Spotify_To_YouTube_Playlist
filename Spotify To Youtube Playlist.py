import os
from spotipy.oauth2 import SpotifyOAuth
import spotipy
import pickle
import googleapiclient.discovery
import google_auth_oauthlib.flow
import googleapiclient.errors



def main():
#Youtube API authentication
    os.environ["OAUTHLIB_INSECURE_TRANSPORT"] = "1"
    scopes = ["https://www.googleapis.com/auth/youtube.force-ssl"]
    client_secrets_file = "client_secret.json"
    api_service_name = "youtube"
    api_version = "v3"

    def get_authenticated_service():
            if os.path.exists("Save_Credentials"):
                with open("Save_Credentials", "rb") as f:
                    credentials = pickle.load(f)
            else:
                flow = google_auth_oauthlib.flow.InstalledAppFlow.from_client_secrets_file(client_secrets_file, scopes)
                credentials = flow.run_local_server()
                with open("Save_Credentials", "wb") as f:
                    pickle.dump(credentials, f)
            return googleapiclient.discovery.build(
                api_service_name, api_version, credentials=credentials)
    youtube = get_authenticated_service()
#Spotify API authentication
    sp = spotipy.Spotify(auth_manager=SpotifyOAuth(client_id="8ed0d1e51d0f476a923e6811621cbfe0",
                                                   client_secret="a0461fdf929a49a9a4356592f02ab027",
                                                   redirect_uri="http://localhost:8080",
                                                   scope="playlist-read-private"))

    if os.path.exists("output.txt"):
        os.remove("output.txt")
#Request song names in a playlist from spotify
    playlist_id = "3TvifVpEro6FJ1vTD4LVfB"
    results = sp.playlist_items(playlist_id, fields=None, limit=100, offset=0, additional_types=("track", ))
    for item in results["items"]:
        track = item["track"]
        file = open("output.txt", "a")
        print(track["artists"][0]["name"], track["name"], file=file)
        file.close()
#Search youtube for song names and request IDs
    if os.path.exists("output2.txt"):
        os.remove("output2.txt")

    with open("output.txt", "r") as f:
        songs = f.read().splitlines(True)
        for line in songs:
            request = youtube.search().list(
            part="snippet",
            type="video",
            videoCategoryId="10",
            maxResults=1,
            q=line,
            topicId="/m/04rlf",
            videoDefinition="high",
            )
            response = request.execute()
            for item in response["items"]:
                file = open("output2.txt", "a")
                print(item["id"]["videoId"], file=file)
                file.close()
#Create Youtube playlist
    if os.path.exists("output3.txt"):
        os.remove("output3.txt")

    playlist = youtube.playlists().insert(
        part="snippet,status",
        body={
            "snippet": {
                "title": "Spotify Playlist",
                "description": "Playlist from Spotify",
                "tags": [
                "sample playlist",
                "API call",
                ],
            "defaultLanguage": "en"
                    },
            "status": {
            "privacyStatus": "private"
                    }
            }
        )
    create = playlist.execute()
    file = open("output3.txt", "a")
    print(create["id"], file=file)
    file.close()
#Insert song IDs in created playlist
    with open("output2.txt", "r") as file:
        song_id = file.read().splitlines()
        for song in song_id:
            with open("output3.txt", "r") as file:
                playlist_id = file.read().splitlines()
                for playlist in playlist_id:
                    insert = youtube.playlistItems().insert(
                        part="snippet",
                        body={
                            "snippet": {
                                "playlistId": playlist,
                                "resourceId": {
                                    "kind": "youtube#video",
                                    "videoId": song
                                }
                            }
                        }
                    )
                    insert.execute()
                    print(f'Song "{song}" added to playlist "{playlist}"')

if __name__ == "__main__":
    main()
