from config import SPOTIFY_CLIENT_ID, SPOTIFY_CLIENT_SECRET, SPOTIFY_REDIRECT
import spotipy
from spotipy.oauth2 import SpotifyOAuth

SCOPE = "user-library-read user-top-read"
### Source for all Spotipy related functionality (where it was learned from): https://spotipy.readthedocs.io/en/2.22.1/
class PopularRec:
    def __init__(self, data):
        self.data = data

    def recommend(self, track_id, num_recs=30):
        if track_id in self.data['track_id'].values:
            target_song = self.data.loc[self.data['track_id'] == track_id]
            song_name = target_song['track_name'].values[0]
            artist = target_song['artist_name'].values[0]
            target_genre = target_song['genre'].values[0]
        else:
            # If track_id is not in the dataset, use Spotipy API to get the track features
            try:
                SPOT_CLIENT =  spotipy.Spotify(auth_manager=SpotifyOAuth(SPOTIFY_CLIENT_ID, SPOTIFY_CLIENT_SECRET, SPOTIFY_REDIRECT, scope=SCOPE))
                track = SPOT_CLIENT.track(track_id)
                song_name = track['name']
                artist = track['artists'][0]['name']
                target_genre = SPOT_CLIENT.artist(track['artists'][0]['id'])['genres'][0]
            except:
                print("The specified track_id is invalid or not found on Spotify.")
                return
        
        same_genre_songs = self.data[self.data['genre'] == target_genre]
        same_genre_songs = same_genre_songs[same_genre_songs['track_id'] != track_id]  # make sure we do not recommend the song sent by the user
        same_genre_songs = same_genre_songs.sort_values('popularity', ascending=False)
        
        results = []
        print("Recommendations for:", song_name, "by", artist)
        for i, (_, row) in enumerate(same_genre_songs.head(num_recs).iterrows(), start=1): # print out and return results of reocmmendations
            song_title = row['track_name']
            artist = row['artist_name']
            print(f"Recommendation #{i}: {song_title} by {artist}")
        results.append(f"Recommendation #{i}: {song_title} by {artist}")
        return results