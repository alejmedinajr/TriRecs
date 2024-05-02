# Spotify Recommender Systems

## Introduction
This project focuses on developing various recommender systems for Spotify using Python and the Spotipy library. The main objective is to provide personalized song recommendations based on user preferences and song features.

## Why Recommender Systems?
Recommender systems play a crucial role in enhancing user experience and engagement on platforms like Spotify. By analyzing user behavior, preferences, and song attributes, these systems can generate highly relevant and personalized recommendations. This not only improves user satisfaction but also helps in discovering new music tailored to individual tastes.

## Using Spotipy
Spotipy is a Python library that simplifies the interaction with the Spotify API. It allows developers to access various features and data related to songs, artists, and user profiles. In this project, Spotipy is used to establish a connection between Python and the Spotify API, enabling seamless retrieval of song information and user data. The official documentation of Spotify can be found here: [Spotipy Documentation](https://spotipy.readthedocs.io/en/2.22.1/)

## Recommender Systems Implemented

### 1. Collaborative Filtering Recommender System
- File: `CollaborativeFilteringRecSys.py`
- This recommender system utilizes collaborative filtering techniques to generate recommendations based on user-item interactions.
- It preprocesses the playlist and song data by encoding categorical variables and normalizing numerical features.
- The system trains a k-Nearest Neighbors (KNN) model using the preprocessed data to find similar songs.
- Given a playlist, it recommends songs based on the nearest neighbors found by the KNN model.

### 2. Content-Based Recommender System
- File: `ContentRecSys.py`
- The content-based recommender system focuses on the intrinsic features of songs to provide recommendations.
- It preprocesses the song dataset and liked songs dataset by encoding categorical variables and normalizing numerical features.
- The system trains a Logistic Regression model using the preprocessed data to predict the likelihood of a song being liked.
- It calculates the cosine similarity between a given song and the songs in the test set.
- The recommendations are generated based on the combination of similarity scores and predicted probabilities.

### 3. Popular Recommender System
- File: `PopularRecSys.py`
- The popular recommender system suggests songs based on their popularity within a specific genre.
- It identifies the target song's genre using the Spotify API if the song is not found in the dataset.
- The system sorts the songs within the same genre by their popularity and recommends the top-N most popular songs.

### 4. Random Recommender System
- File: `RandomRecSys.py`
- The random recommender system provides random song recommendations from the same genre as the target song.
- It retrieves the target song's genre using the Spotify API if the song is not found in the dataset.
- The system randomly selects N songs from the same genre as the target song and recommends them.

## Datasets
The project utilizes various Spotify datasets to train and evaluate the recommender systems. The main datasets used are:
- `spotify_data.csv`: Contains information about songs, including track ID, track name, artist name, genre, and other features (all from the Spotify 1 Million Dataset).
- `ahhhhhhhhhhhhhhhhhhhhhlejandro_liked_songs.csv`: Contains a list of liked songs by a specific user. (This is a comprehensive list, including track information, for one of the users)
- Playlist datasets: `200_songs.csv`, `Digital Desert_songs.csv`, `Pico_songs.csv`, `Resolve._songs.csv`, `Tizón_songs.csv`. (these are user-based playlists that had track information extracted using the Spotify API)
- *The main spotify dataset can be obtained here (it is too large for GitHub): [Spotify 1 Million Dataset](https://www.aicrowd.com/challenges/spotify-million-playlist-dataset-challenge)*

## Utility Functions
The project includes a `utils.py` file that contains several utility functions to streamline the data retrieval and processing tasks. These functions leverage the Spotipy library to interact with the Spotify API and retrieve relevant information. Some of the key utility functions include:

- `process_artist`: Searches for an artist on Spotify and retrieves their genres.
- `get_user_liked_songs`: Retrieves the user's liked songs from Spotify and saves them to a CSV file.
- `get_playlist_id`: Extracts the playlist ID from a given Spotify playlist URL.
- `get_playlist_songs`: Retrieves the songs from a given Spotify playlist and saves them to a CSV file.
- `get_playlist_track_ids`: Retrieves the track IDs from a given Spotify playlist.

These utility functions play a crucial role in gathering the necessary data for training and evaluating the recommender systems.

## Configuration
The project includes a `config.py` file that stores the configuration variables required for connecting to the Spotify API. These variables include:

- `SPOTIFY_WEBSITE`: The URL of the Spotify website.
- `SPOTIFY_REDIRECT`: The redirect URL for the Spotify authentication flow.
- `SPOTIFY_CLIENT_ID`: The client ID obtained from the Spotify Developer Dashboard.
- `SPOTIFY_CLIENT_SECRET`: The client secret obtained from the Spotify Developer Dashboard.
- `USER`: The username of the Spotify user.

Make sure to replace these variables with your own Spotify API credentials and user information before running the project.
You can find more about Spotify for Developers [here](https://developer.spotify.com/)

## Dependencies
The project relies on several Python libraries and packages, which are listed in the `requirements.txt` file. These dependencies include popular libraries such as Keras, Pandas, Scikit-learn, Spotipy, and TensorFlow. To install the required dependencies, you can use the following command:

```
pip install -r requirements.txt
```

This command will install all the necessary packages and their specified versions, ensuring compatibility and smooth execution of the project.

## Results
The project includes an `experiment.py` file that demonstrates the usage of the implemented recommender systems. It iterates over a list of track IDs and generates recommendations using each recommender system. The recommended songs are saved in separate CSV files in the `Results` directory for further analysis and evaluation.

Please refer to the individual recommender system files and the `experiment.py` file for more details on how each system works and how to run the experiments.
