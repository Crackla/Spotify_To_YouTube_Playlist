import os
from spotipy.oauth2 import SpotifyOAuth
import spotipy
import pickle
import googleapiclient.discovery
import google_auth_oauthlib.flow
import googleapiclient.errors

#Save google account credentials for repeated use
def get_authenticated_service(flow, api_service, api_version):
    if os.path.exists("Save_Credentials"):
        with open("Save_Credentials", "rb") as f:
            credentials = pickle.load(f)
    else:
        credentials = flow.run_local_server()
        with open("Save_Credentials", "wb") as f:
            pickle.dump(credentials, f)
    return googleapiclient.discovery.build(
        api_service, api_version, credentials=credentials)



def main():
#YouTube API authentication
    os.environ["OAUTHLIB_INSECURE_TRANSPORT"] = "1"
    scopes = ["https://www.googleapis.com/auth/youtube.force-ssl"]
    client_secrets_file = "client_secret.json"
    #client_secret.json from https://console.cloud.google.com/apis/dashboard
    api_service_name = "youtube"
    api_version = "v3"

    flow = google_auth_oauthlib.flow.InstalledAppFlow.from_client_secrets_file(
        client_secrets_file, scopes)
    youtube = get_authenticated_service(flow, api_service_name, api_version)
#Spotify API authentication
    sp = spotipy.Spotify(auth_manager=SpotifyOAuth(client_id="insert_client_ID",
                                                   #client_ID from https://developer.spotify.com/dashboard
                                                   client_secret="insert_client_secret",
                                                   #client_secret from https://developer.spotify.com/dashboard
                                                   redirect_uri="http://localhost:8080",
                                                   scope="playlist-read-private"))
#Create YouTube playlist
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
    playlist_id = create["id"]
#Request song names from Spotify playlist
    results = sp.playlist_items("insert_playlist_id", fields=None, limit=100, offset=0, additional_types=("track",))
    #Playlist_id from the playlist URL e.g. https://open.spotify.com/playlist/(playlist_id)
    track_results = []
    yt_results = []
#Search YouTube for song names and request song IDs
    for item in results["items"]:
        songs = item.get("track")
        if songs:
            track = (songs["artists"][0]["name"], (songs["name"]))
            track_results.append(track)

            request = youtube.search().list(
                part="snippet",
                type="video",
                videoCategoryId="10",
                maxResults=1,
                q=track,
                topicId="/m/04rlf",
                videoDefinition="high", )
            response = request.execute()
            video_id = response["items"][0].get("id", {}).get("videoId")
            if video_id:
                yt_results.append(video_id)
#Insert song IDs in created playlist
    for video_id in yt_results:
        insert = youtube.playlistItems().insert(
            part="snippet",
            body={
                "snippet": {
                    "playlistId": playlist_id,
                    "resourceId": {
                        "kind": "youtube#video",
                        "videoId": video_id
                    }
                }
            }
        )
        insert.execute()
        print(f'Song "{video_id}" added to playlist "{playlist_id}"')


if __name__ == "__main__":
    main()
