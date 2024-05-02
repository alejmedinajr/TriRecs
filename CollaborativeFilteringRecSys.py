import pandas as pd
from sklearn.preprocessing import OneHotEncoder, StandardScaler
from sklearn.neighbors import NearestNeighbors
from sklearn.metrics.pairwise import cosine_similarity

class CollaborativeFilteringRecSys:
    def __init__(self, playlist_data, song_dataset, k=30):
        self.playlist_data = playlist_data
        self.song_dataset = song_dataset
        self.k = k
        self.categorical_cols = ['track_id', 'track_name', 'artist_names', 'genre']
        self.numerical_cols = ['popularity', 'duration_ms']
        self.onehot_encoder = OneHotEncoder(handle_unknown='ignore')
        self.scaler = StandardScaler()
        self.knn_model = None
        self.preprocessed_data = None

    def preprocess_data(self):
        # Drop unwanted columns
        columns_to_drop = ['Unnamed: 0', 'danceability','energy','key','loudness','mode','speechiness','acousticness','instrumentalness','liveness','valence','tempo','time_signature']

        self.song_dataset = self.song_dataset.drop(columns=columns_to_drop)
        # Rename columns
        column_mapping = {'artist_name': 'artists_names'}
        self.song_dataset = self.song_dataset.rename(columns=column_mapping)
                                                     
        columns_to_drop = ['explicit','album','uri']
        self.playlist_data = self.playlist_data.drop(columns=columns_to_drop)
        column_mapping = {'release_date': 'year'}
        self.playlist_data = self.playlist_data.rename(columns=column_mapping)
        self.playlist_data['year'] = self.playlist_data['year'].str.split('-').str[0].astype(int)

        # Create 'decade' column
        self.playlist_data['decade'] = (self.playlist_data['year'] // 10) * 10
        self.song_dataset['decade'] = (self.song_dataset['year'] // 10) * 10

        # One-hot encoding for categorical columns
        onehot_encoded = self.onehot_encoder.fit_transform(self.playlist_data[self.categorical_cols])

        # Normalization for numerical columns
        normalized_data = self.scaler.fit_transform(self.playlist_data[self.numerical_cols])

        # Combine one-hot encoded and normalized data
        self.preprocessed_data = pd.concat([pd.DataFrame(onehot_encoded.toarray()), pd.DataFrame(normalized_data)], axis=1)

    def train_model(self):
        # Create KNN model based on https://scikit-learn.org/stable/modules/neighbors.html
        self.knn_model = NearestNeighbors(n_neighbors=self.k, metric='cosine')
        self.knn_model.fit(self.preprocessed_data)

    def recommend(self, playlist_data):
        # Convert playlist_data to a DataFrame if it's a Series
        if isinstance(playlist_data, pd.Series):
            playlist_data = pd.DataFrame([playlist_data])

        # Preprocess the playlist data
        playlist_onehot = self.onehot_encoder.transform(playlist_data[self.categorical_cols])
        playlist_normalized = self.scaler.transform(playlist_data[self.numerical_cols])
        playlist_preprocessed = pd.concat([pd.DataFrame(playlist_onehot.toarray()), pd.DataFrame(playlist_normalized)], axis=1)

        # Find the nearest neighbors
        distances, indices = self.knn_model.kneighbors(playlist_preprocessed)

        # Get the recommended songs from the song dataset
        recommended_songs = []
        for idx in indices.flatten():
            recommended_song = self.song_dataset.iloc[idx]
            if recommended_song['track_id'] not in playlist_data['track_id'].values:
                recommended_songs.append(recommended_song)

        # Return the top-n recommended songs
        return pd.DataFrame(recommended_songs[:self.k])