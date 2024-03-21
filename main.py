import spotipy
import sys
from spotipy.oauth2 import SpotifyClientCredentials, SpotifyOAuth
from config import SPOTIFY_CLIENT_ID, SPOTIFY_CLIENT_SECRET, SPOTIFY_REDIRECT
lz_uri = 'spotify:artist:36QJpDe2go2KgaRleHCDTp'

#results = spotify.artist_top_tracks(lz_uri)

def print_top_songs(artist_name, spotify_client):
    # Search for the artist
    results = spotify_client.search(q='artist:' + artist_name, type='artist')
    items = results['artists']['items']
    
    if not items:
        print("Artist not found")
        return
    
    artist = items[0]
    artist_id = artist['id']

    # Get the top tracks for the artist
    top_tracks = spotify_client.artist_top_tracks(artist_id)

    print(f"Top 10 Songs by {artist_name}:")
    print("===================")
    for track in top_tracks['tracks']:
        print(f"{track['name']} - {', '.join([artist['name'] for artist in track['artists']])}")

def print_most_played_songs(username, spotify_client):
    # Get the user's top tracks
    top_tracks = spotify_client.current_user_top_tracks(limit=50, time_range='long_term')

    print(f"Most Played Songs for {username}:")
    for i, track in enumerate(top_tracks['items']):
        print(f"{i+1}. {track['name']} - {', '.join([artist['name'] for artist in track['artists']])}")

spotify_client = spotipy.Spotify(client_credentials_manager=SpotifyClientCredentials(SPOTIFY_CLIENT_ID, SPOTIFY_CLIENT_SECRET))
print_top_songs('Rage Against The Machine', spotify_client)
print("")
print_top_songs('Michael Jackson', spotify_client)

scope = 'user-top-read'
spotify_client = spotipy.Spotify(auth_manager=SpotifyOAuth(SPOTIFY_CLIENT_ID, SPOTIFY_CLIENT_SECRET,SPOTIFY_REDIRECT,scope=scope))
print_most_played_songs('ahhhhhhhhhhhhhhhhhhhhhlejandro', spotify_client)