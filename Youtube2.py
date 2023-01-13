import os
import pickle
import google_auth_oauthlib.flow
import googleapiclient.discovery
import googleapiclient.errors

scopes = ["https://www.googleapis.com/auth/youtube.force-ssl"]


def main():
    os.environ["OAUTHLIB_INSECURE_TRANSPORT"] = "0"

api_service_name = "youtube"
api_version = "v3"
client_secrets_file = "client_secret.json"

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



flow = google_auth_oauthlib.flow.InstalledAppFlow.from_client_secrets_file(
client_secrets_file, scopes)
youtube = get_authenticated_service()

with open("output2.txt", "r") as file:
    song_id = file.read().splitlines()
    for song in song_id:
        with open("output3.txt", "r") as file:
            playlist_id = file.read().splitlines()
            for playlist in playlist_id:
                request = youtube.playlistItems().insert(
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
                response = request.execute()
                print(f'Song "{song}" added to playlist "{playlist}"')


if __name__ == "__main__":
    main()

