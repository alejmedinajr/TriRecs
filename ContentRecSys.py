import pandas as pd
from sklearn.preprocessing import OneHotEncoder, StandardScaler
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.metrics.pairwise import cosine_similarity
import random

class ContentBasedRecSys:
    def __init__(self, song_dataset, liked_songs_dataset, n_songs=100, test_size=0.2):
        self.song_dataset = song_dataset
        self.liked_songs_dataset = liked_songs_dataset
        self.n_songs = n_songs
        self.test_size = test_size
        self.categorical_cols = ['track_id', 'track_name', 'artist_names', 'genre']
        self.numerical_cols = ['popularity', 'duration_ms']
        self.onehot_encoder = OneHotEncoder(handle_unknown='ignore')
        self.scaler = StandardScaler()
        self.model = None
        self.preprocessed_data = None
        self.train_data = None
        self.test_data = None

    def preprocess_data(self):
        # Drop unwanted columns
        columns_to_drop = ['Unnamed: 0', 'danceability','energy','key','loudness','mode','speechiness','acousticness','instrumentalness','liveness','valence','tempo','time_signature']

        self.song_dataset = self.song_dataset.drop(columns=columns_to_drop)
        # Rename columns
        column_mapping = {'artist_name': 'artists_names'}
        self.song_dataset = self.song_dataset.rename(columns=column_mapping)
                                                     
        columns_to_drop = ['explicit','album','uri']
        self.liked_songs_dataset = self.liked_songs_dataset.drop(columns=columns_to_drop)
        column_mapping = {'release_date': 'year'}
        self.liked_songs_dataset = self.liked_songs_dataset.rename(columns=column_mapping)
        self.liked_songs_dataset['year'] = self.liked_songs_dataset['year'].str.split('-').str[0].astype(int)

        # Create 'decade' column
        self.liked_songs_dataset['decade'] = (self.liked_songs_dataset['year'] // 10) * 10
        self.song_dataset['decade'] = (self.song_dataset['year'] // 10) * 10
        # Combine the song dataset and liked songs dataset
        combined_dataset = pd.concat([self.song_dataset, self.liked_songs_dataset])

        # One-hot encoding for categorical columns
        onehot_encoded = self.onehot_encoder.fit_transform(combined_dataset[self.categorical_cols])

        # Normalization for numerical columns
        normalized_data = self.scaler.fit_transform(combined_dataset[self.numerical_cols])

        # Combine one-hot encoded and normalized data
        self.preprocessed_data = pd.concat([pd.DataFrame(onehot_encoded.toarray()), pd.DataFrame(normalized_data)], axis=1)

    def train_model(self):
        # Select random songs from the liked songs dataset and the overall song dataset
        liked_songs_sample = self.liked_songs_dataset.sample(n=self.n_songs)
        song_dataset_sample = self.song_dataset.sample(n=self.n_songs)

        # Combine the sampled datasets
        train_dataset = pd.concat([liked_songs_sample, song_dataset_sample])

        # Preprocess the train dataset
        train_onehot = self.onehot_encoder.transform(train_dataset[self.categorical_cols])
        train_normalized = self.scaler.transform(train_dataset[self.numerical_cols])
        train_preprocessed = pd.concat([pd.DataFrame(train_onehot.toarray()), pd.DataFrame(train_normalized)], axis=1)

        # Create target labels (1 for liked songs, 0 for randomly sampled songs)
        target = [1] * self.n_songs + [0] * self.n_songs

        # Split the preprocessed data into train and test sets
        self.train_data, self.test_data, train_target, test_target = train_test_split(
            train_preprocessed, target, test_size=self.test_size, stratify=target
        )

        # Create and train the Logistic Regression model
        self.model = LogisticRegression()
        self.model.fit(self.train_data, train_target)

    def get_recommendations(self, song_id, num_recs=30):
        # Find the song in the song dataset
        song_data = self.song_dataset[self.song_dataset['track_id'] == song_id]

        if song_data.empty:
            print(f"Song with ID {song_id} not found in the dataset.")
            return None

        # Preprocess the song data
        song_onehot = self.onehot_encoder.transform(song_data[self.categorical_cols])
        song_normalized = self.scaler.transform(song_data[self.numerical_cols])
        song_preprocessed = pd.concat([pd.DataFrame(song_onehot.toarray()), pd.DataFrame(song_normalized)], axis=1)

        # Predict the probability of the song being liked
        song_prob = self.model.predict_proba(song_preprocessed)[:, 1]

        # Calculate the cosine similarity between the song and all songs in the test set
        test_onehot = self.onehot_encoder.transform(self.test_data[self.categorical_cols])
        test_normalized = self.scaler.transform(self.test_data[self.numerical_cols])
        test_preprocessed = pd.concat([pd.DataFrame(test_onehot.toarray()), pd.DataFrame(test_normalized)], axis=1)
        similarities = cosine_similarity(song_preprocessed, test_preprocessed).flatten()

        # Combine the similarity scores and predicted probabilities
        recommendation_scores = similarities * song_prob

        # Get the indices of the top-k recommended songs
        top_indices = recommendation_scores.argsort()[-num_recs:][::-1]

        # Return the top-k recommended songs
        return self.test_data.iloc[top_indices]