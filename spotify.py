import spotipy
import sys
import numpy as np
import csv
from spotipy.oauth2 import SpotifyClientCredentials, SpotifyOAuth
from config import SPOTIFY_CLIENT_ID, SPOTIFY_CLIENT_SECRET, SPOTIFY_REDIRECT, USER

def create_dataset(user_data, output):
    """
    Helper function that creates a new dataset to a specified file location using existing user data.

    Parameters:
        user_data: A dictionary of songs where each song has various attributes
        output: Specified location where the dataset will be saved to (csv)

    Returns:
        Nothing.
    """
    header = ["track_id", "track_name", "artist_names", "album_name", "duration_ms", "popularity", "genres"] # headers for the dataset

    with open(output, "w", newline="", encoding="utf-8") as file: # opening a new file with the purpose to write (creating dataset)
        writer = csv.writer(file) # initializing csv writer object
        writer.writerow(header) # writing the first row (contains the header information)

        for track in user_data: # each track will be a row, so all track information needs to be included in the current row
            track_id = track["id"] # unique id of the track
            track_name = track["name"] # name of the track
            artist_names = ", ".join(track["artists"]) # artists who made the track
            album_name = track["album"] # album of the track
            duration_ms = track["duration_ms"] # length of track (in milliseconds)
            popularity = track["popularity"] # Spotify's popularity metric for the track
            explicit = track["explicit"] # binary classification detailing if the song is explicit
            genres = ", ".join(track["genres"]) # the genres need to be joined because they are currently unique elements in a list

            row = [track_id, track_name, artist_names, album_name, duration_ms, popularity, explicit, genres] # initializing the current row parameter
            writer.writerow(row) # writing the current row

    print(f'Dataset saved as {output}') # if we were successful, print message notifying where the dataset was saved (filename)

def get_genres(spotify, artist_id):
    """
    This helper function gets all of the genres from a single song (since a single song can have different genres associated with it).

    Parameters:
        spotify: Spotify API Client that can be used to make queries to Spotify for song or artist information
        artist_id: Unique id that is associated with an artist on Spotify (useful for getting genre information)

    Returns:
        List containing the genres associated with the specified artist
    """
    artist_info = spotify.artist(artist_id)
    return artist_info["genres"] # we only want the artist's associated genres (not all other information pertaining to artist)

def get_user_data(user, song_limit):
    """
    Helper function that retrieves a specified number of most played songs for a specific user.

    Parameters:
        user: The user whose top songs will be retrieved
        song_limit: The maximum number of most played songs from the user (may be less if the user has not listened to at least the same number of songs as this parameter)

    Returns:
        List of dictionaries, where each dictionary represents the information of one 'most listened to' song from the user
    """
    client_id = SPOTIFY_CLIENT_ID # Spotify client id used to initialize API client
    client_secret = SPOTIFY_CLIENT_SECRET # Spotify client secret used to initialize API client
    redirect_uri = SPOTIFY_REDIRECT # Spotify redirect uri used to initialize API client
    scope = "user-library-read user-top-read" # the scope of the client (needs to be specified so we can access the user's data)

    spotify = spotipy.Spotify(auth_manager=SpotifyOAuth(client_id=client_id, client_secret=client_secret, redirect_uri=redirect_uri, scope=scope)) # initializing Spotify API Client

    user_data = []
    LIMIT = 50 # hard limit on the number of songs that can be retrieved at a time by Spotify's API
    offset = 0 # used to get around the limit, will be used to shift the current top song (while still not reaching the Spotify API imposed limit)

    while len(user_data) < song_limit: # want to continue getting the user's top played songs until we either run out of songs from the user or we reach the specified target limit
        top_tracks = spotify.current_user_top_tracks(limit=LIMIT, offset=offset, time_range="long_term") # using built in API function to retrieve 50 top songs (from an all time period)
        
        if not top_tracks["items"]: return user_data # if the user does not have enough songs in their top tracks collection, then return the songs already obtained (if any)

        for track in top_tracks["items"]: # for each track, the information of the track need to be stored
            song_data = { # represents a song
                "id": track["id"], # unique track id
                "name": track["name"], # track name
                "artists": [artist["name"] for artist in track["artists"]], # artisits who made the track
                "album": track["album"]["name"], # album name for the track
                "duration_ms": track["duration_ms"], # duration of the track (in milliseconds) 
                "popularity": track["popularity"], # Spotify's popularity metric for the specific track
                "explicit": track["explicit"], # binary classification detailing if the song is explicit
                "genres": [] # list containing the track's associated genres
            }

            for artist in track["artists"]: # each artist has associated genres, which need to be obtained since tracks do not have that information inherently stored in the object
                artist_id = artist["id"] # using artist id to get the genres
                genres = get_genres(spotify, artist_id) # using helper function to get genres
                song_data["genres"].extend(genres) # adding genres to existing genres (since we do not want to overwrite existing genres in the case of multiple artists)
            
            user_data.append(song_data) # add the current track dictionary to user data list

        offset += LIMIT # increase the offset so that we can process the next 50 songs (avoiding the spotify hard limit of 50 songs per API call)

    return user_data # return the user data

### USED TO CREATE INITIAL DATASET ###
user_data = get_user_data(USER, 1500)
create_dataset(user_data, f'datasets/{USER}_top_1500_spotify_songs.csv')