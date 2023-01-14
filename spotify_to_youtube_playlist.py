import os
from spotipy.oauth2 import SpotifyOAuth
import spotipy
import pickle
import googleapiclient.discovery
import google_auth_oauthlib.flow
import googleapiclient.errors


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
    os.environ["OAUTHLIB_INSECURE_TRANSPORT"] = "1"
    scopes = ["https://www.googleapis.com/auth/youtube.force-ssl"]
    client_secrets_file = "client_secret.json"
    api_service_name = "youtube"
    api_version = "v3"

    flow = google_auth_oauthlib.flow.InstalledAppFlow.from_client_secrets_file(
        client_secrets_file, scopes)
    youtube = get_authenticated_service(flow, api_service_name, api_version)
    sp = spotipy.Spotify(auth_manager=SpotifyOAuth(client_id="8ed0d1e51d0f476a923e6811621cbfe0",
                                                   client_secret="a0461fdf929a49a9a4356592f02ab027",
                                                   redirect_uri="http://localhost:8080",
                                                   scope="playlist-read-private"))

    playlist_id = "3TvifVpEro6FJ1vTD4LVfB"
    results = sp.playlist_items(playlist_id, fields=None, limit=100, offset=0, additional_types=("track",))

    # results = [
    #     {
    #         "name": "TracknameXY",
    #         "artists": [
    #             {"name": "ArtistXY"}
    #         ]
    #     },
    #     {"name": "TracknameXY2",
    #      "artists": [
    #          {"name": "ArtistXY2"}
    #      ]
    #      },
    #     {"name": "TracknameXY3",
    #      "artists": [
    #          {"name": "ArtistXY3"}
    #      ]
    #      },
    # ]

    for track_item in results:
        request = youtube.search().list(
            part="snippet",
            type="video",
            videoCategoryId="10",
            maxResults=1,
            q=f"{track_item.get('artist', [])[0].get('name')} {track_item.get('name')}",
            topicId="/m/04rlf",
            videoDefinition="high",
        )
        response = request.execute()

        yt_results = []
        for item in response["items"]:
            video_id = item.get("id", {}).get("videoId")
            if video_id:
                yt_results.append(video_id)


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

    for video_id in yt_results:
        request = youtube.playlistItems().insert(
            part="snippet",
            body={
                "snippet": {
                    "playlistId": playlist,
                    "resourceId": {
                        "kind": "youtube#video",
                        "videoId": video_id
                    }
                }
            }
        )
        response = request.execute()
        print(f'Song "{video_id}" added to playlist "{playlist_id}"')


if __name__ == "__main__":
    main()
