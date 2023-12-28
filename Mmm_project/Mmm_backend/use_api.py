import requests
import json 
import base64

class UseApi:
    def __init__(self, cli_id, cli_sec):
        client_id = cli_id
        client_secret = cli_sec
        token_endpoint = 'https://accounts.spotify.com/api/token'
        payload = {'grant_type': 'client_credentials'}
        headers = {
        'Content-Type': 'application/x-www-form-urlencoded',
        'Authorization': 'Basic ' + base64.b64encode(f"{client_id}:{client_secret}".encode()).decode()
        }
        token_response = requests.post(token_endpoint, data=payload, headers=headers)
        token_data = token_response.json()
        access_token = token_data['access_token']
        # Fetch data from Spotify API using search query
        self.headers = {'Authorization': 'Bearer ' + access_token}
        print("Authorization complete")
        
    def search_tracks(self, track_names):
        search_endpoint = f'https://api.spotify.com/v1/search?q={" AND ".join(track_names)}&type=track'
        search_response = requests.get(search_endpoint, headers=self.headers)
        search_data = search_response.json()
        tracks_data = search_data['tracks']['items']  # Get multiple track items from the search result

        tracks = []  # List to hold track data
        for track_item in tracks_data:
            # 각 트랙의 정보를 가공하여 리스트에 추가
            track_id = track_item['id']
            album_id = track_item['album']['id']
            album_name = track_item['album']['name']
            release_date = track_item['album']['release_date']
            artist_id = track_item['artists'][0]['id']
            name = track_item['name']
            artist_name = track_item['artists'][0]['name']
            image = track_item['album']['images'][0]['url']
            popularity = track_item['popularity']
            link = track_item['external_urls']['spotify']

            track_data = {
                'track_id': track_id,
                'album_id': album_id,
                'artist_id': artist_id,
                'album_name': album_name,
                'release_date': release_date,
                'track_name': name,
                'artist_name': artist_name,
                'popularity': popularity,
                'image': image,
                'link': link
            }
            tracks.append(track_data)

        return tracks
    
    def get_track_details(self, track_id):
        track_endpoint = f'https://api.spotify.com/v1/tracks/{track_id}'
        track_response = requests.get(track_endpoint, headers=self.headers)
        self.track_data = track_response.json()
        artist_name = self.track_data['artists'][0]['name']
        artist_data = self.search_artist(artist_name)
        related_artists = self.get_related_artists(artist_data['id'])
        audio_features = self.get_audio_features(track_id)
        self.track_data['related_artists'] = related_artists
        self.track_data['artist_info'] = artist_data  # Adding artist info to track_data
        track_features = dict(popularity = self.track_data["popularity"], acousticness = audio_features["acousticness"], danceability = audio_features["danceability"], energy = audio_features["energy"], valence = audio_features["valence"], tempo = audio_features["tempo"])
        related_artist = []
        for track in related_artists:
            artist_id = track["id"]
            artist_name = track["name"]
            genres = ", ".join(track["genres"])
            image = track["images"][0]["url"]
            popularity = track["popularity"]
            link = track["external_urls"]["spotify"]
            related_artist.append(dict(artist_id = artist_id, artist_name = artist_name, genres = genres, popularity = popularity, image = image, link = link))
            
       
        self.album_data = dict(album_id = self.track_data["album"]["id"], album_name = self.track_data["album"]["name"], release_date = self.track_data["album"]["release_date"], album_image = self.track_data["album"]["images"][0]["url"], album_link = self.track_data["album"]["external_urls"]["spotify"])
        self.artist_data = dict(artist_id = self.track_data["artist_info"]["id"], artist_name = self.track_data["artist_info"]["name"], artist_popularity = self.track_data["artist_info"]["popularity"], genres = ", ".join(self.track_data["artist_info"]["genres"]), artist_image = self.track_data["artist_info"]["images"][0]["url"], artist_link = self.track_data["artist_info"]["external_urls"]["spotify"])
        self.song_data = dict(track_id = self.track_data["id"], track_name = self.track_data["name"], track_popularity = self.track_data["popularity"], track_image = self.track_data["album"]["images"][0]["url"], track_link= self.track_data["external_urls"]["spotify"])
        return self.album_data, self.artist_data, self.song_data, track_features
    
    
    def search_artist(self, artist_name):
        search_endpoint = f'https://api.spotify.com/v1/search?q={artist_name}&type=artist'
        search_response = requests.get(search_endpoint, headers=self.headers)
        search_data = search_response.json()
        artist_id = search_data['artists']['items'][0]['id']  # Get artist ID from the first search result
        # Fetch artist data from Spotify API using artist ID
        artist_endpoint = f'https://api.spotify.com/v1/artists/{artist_id}'
        artist_response = requests.get(artist_endpoint, headers=self.headers)
        self.artist_data = artist_response.json()
        return self.artist_data
    
    def get_related_artists(self, artist_id):
        related_artists_endpoint = f'https://api.spotify.com/v1/artists/{artist_id}/related-artists'
        related_artists_response = requests.get(related_artists_endpoint, headers=self.headers)
        related_artists_data = related_artists_response.json()
        return related_artists_data['artists'] if 'artists' in related_artists_data else []        
    
    def get_audio_features(self, track_id):
        audio_features_endpoint = f'https://api.spotify.com/v1/audio-features/{track_id}'
        audio_features_response = requests.get(audio_features_endpoint, headers=self.headers)
        audio_features_data = audio_features_response.json()
        return audio_features_data
