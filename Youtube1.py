import os
import sys
import pickle
import googleapiclient.discovery
import google_auth_oauthlib.flow
import googleapiclient.errors


scopes = ["https://www.googleapis.com/auth/youtube.force-ssl"]
client_secrets_file = "client_secret.json"
api_service_name = "youtube"
api_version = "v3"

def main():
    os.environ["OAUTHLIB_INSECURE_TRANSPORT"] = "1"

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
        for idx, item in enumerate(response["items"]):
            file = open("output2.txt", "a")
            sys.stdout = file
            print(item["id"]["videoId"])
            file.close()


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
sys.stdout = file
print(create["id"])
file.close()

if __name__ == "__main__":
    main()