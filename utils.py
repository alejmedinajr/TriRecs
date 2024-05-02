import pandas as pd
import re

def process_artist(spotify_client, artist_name):
    """
    This helper function searches for an artist on Spotify using the Spotify API and retrieves their genres.

    Parameters:
        spotify_client (spotipy.Spotify): Spotify client object used to interact with Spotify API.
        artist_name (str): Name of the artist.

    Returns:
        str: Comma-separated string of genres, or 'No Genre' if genres are not found.
    """
    search_results = spotify_client.search(q=artist_name, type='artist') # Search for the artist on Spotify
    genres_info = [] # Create an empty list to store the genres

    if 'artists' in search_results and 'items' in search_results['artists']: # Check if the search results contain artists and items
        artists = search_results['artists']['items'] # Get the list of artists from the search results

        for artist in artists: # Iterate over the list of artists
            if artist['name'] == artist_name: # Check if the artist's name matches the provided artist name
                genres_info = artist.get('genres', []) # Get the genres for the artist, or an empty list if not available
                break # This loops through all artists, so breaking would save computation time

    genre_string = ', '.join(genres_info) if genres_info else 'No Genre' # Join the genres into a comma-separated string, or use 'No Genre' if the list is empty

    return genre_string

def get_user_liked_songs(spotify_client, user_id):
    """
    This helper function retrieves the user's liked songs from Spotify and saves them to a CSV file.

    Parameters:
        spotify_client (spotipy.Spotify): Spotify client object used to interact with Spotify API.
        user_id (str): ID of the user.

    Returns:
        pandas.DataFrame: DataFrame containing the user's liked songs.
    """
    liked_songs = [] # Create an empty list to store the liked songs
    results = spotify_client.current_user_saved_tracks() # Get the user's liked tracks
    liked_tracks = results['items']

    while results['next']: # Loop through the user's liked tracks and extract the necessary information
        for track in liked_tracks: # Extract track information
            track_id = track['track']['id']
            track_name = track['track']['name']
            artists = [artist['name'] for artist in track['track']['artists']] # there could be more than one artist
            artist_names = ', '.join(artists) # join artists name with a comma
            popularity = track['track']['popularity']
            duration_ms = track['track']['duration_ms']
            explicit = track['track']['explicit']
            album = track['track']['album']['name']
            release_date = track['track']['album']['release_date'] # in a time format, maybe drop and get year only
            uri = track['track']['uri']

            genre = process_artist(spotify_client, artists[0]) # Get the genres for the main artist (assuming the first artist is the main artist)
            liked_songs.append({  # Append the track information to the list of liked songs
                'track_id': track_id,
                'track_name': track_name,
                'artist_names': artist_names,
                'popularity': popularity,
                'duration_ms': duration_ms,
                'explicit': explicit,
                'album': album,
                'release_date': release_date,
                'uri': uri,
                'genre': genre
            })

        results = spotify_client.next(results) # Move to the next set of liked tracks
        liked_tracks = results['items']

    liked_songs_df = pd.DataFrame(liked_songs) # Convert the list of dictionaries to a DataFrame
    liked_songs_df.to_csv(f'{user_id}_liked_songs.csv', index=False) # Save the DataFrame to a CSV file before returning
    return liked_songs_df

def get_playlist_id(playlist_url):
    pattern = r'spotify\.com/playlist/([a-zA-Z0-9]+)'
    match = re.search(pattern, playlist_url)
    if match:
        return match.group(1)
    else:
        raise ValueError(f"Invalid playlist URL: {playlist_url}")

def get_playlist_songs(spotify_client, playlist_url):
    """
    This function retrieves the songs from a given Spotify playlist and saves them to a CSV file.

    Parameters:
    spotify_client (spotipy.Spotify): Spotify client object used to interact with Spotify API.
    playlist_url (str): URL of the Spotify playlist.

    Returns:
    pandas.DataFrame: DataFrame containing the songs in the playlist.
    """
    # Extract the playlist ID from the URL
    playlist_id = get_playlist_id(playlist_url)

    # Get the track IDs from the playlist
    track_ids = get_playlist_track_ids(spotify_client, playlist_id)

    # Get track details for each track ID
    playlist_songs = []
    for track_id in track_ids:
        track_info = spotify_client.track(track_id)
        track_name = track_info['name']
        artists = [artist['name'] for artist in track_info['artists']]
        artist_names = ', '.join(artists)
        popularity = track_info['popularity']
        duration_ms = track_info['duration_ms']
        explicit = track_info['explicit']
        album = track_info['album']['name']
        release_date = track_info['album']['release_date']
        uri = track_info['uri']
        genre = process_artist(spotify_client, artists[0])  # Get the genres for the main artist

        playlist_songs.append({
            'track_id': track_id,
            'track_name': track_name,
            'artist_names': artist_names,
            'popularity': popularity,
            'duration_ms': duration_ms,
            'explicit': explicit,
            'album': album,
            'release_date': release_date,
            'uri': uri,
            'genre': genre
        })

    playlist_songs_df = pd.DataFrame(playlist_songs)

    # Get the playlist name
    playlist = spotify_client.playlist(playlist_id)
    playlist_name = playlist['name']

    # Save the DataFrame to a CSV file
    playlist_songs_df.to_csv(f'{playlist_name}_songs.csv', index=False)

    return playlist_songs_df

def get_playlist_track_ids(spotify_client, playlist_id):
    track_ids = []
    results = spotify_client.playlist_tracks(playlist_id)
    tracks = results['items']
    for track in tracks:
        track_ids.append(track['track']['id'])

    while results['next']:
        results = spotify_client.next(results)
        tracks = results['items']
        for track in tracks:
            track_ids.append(track['track']['id'])

    return track_ids