import pandas as pd
from ContentRecSys import ContentBasedRecSys
from RandomRecSys import RandomRec
from PopularRecSys import PopularRec
from CollaborativeFilteringRecSys import CollaborativeFilteringRecSys

track_ids = ['6EtAJUmBqj57hkiBxDy27I', '3yZdQkCzLVKXDEsr9672Db', '0zmitk2ty065TMAvEtGWQ6', '4NOdVqCo6n2Bzsyhl00oB5', '6XdMns9ysH61ngwt7wMh0u']
playlist_ds = ['200_songs.csv', 'Digital Desert_songs.csv', 'Pico_songs.csv','Resolve._songs.csv', 'Tizón_songs.csv']

num_recs = 10
num_training_songs = 25

for i in range(len(track_ids)): 
    spotify_data = pd.read_csv('spotify_data.csv')
    track_id = track_ids[i]
    print('====Popular Recommendation System====')
    popular_rec = PopularRec(spotify_data)
    recommendations = popular_rec.recommend(track_id, num_recs)
    pd.DataFrame(recommendations).to_csv(f'Results/{i}_popular_recs.csv', index=False) # Save the DataFrame to a CSV file before returning

    print('')
    print('====Random Recommendation System====')
    random_rec = RandomRec(spotify_data)
    random_rec.recommend(track_id, num_recs)
    pd.DataFrame(recommendations).to_csv(f'Results/{i}_random_recs.csv', index=False) # Save the DataFrame to a CSV file before returning
    
    print('')
    print('====Collaborative Filtering Recommendation System====')
    playlist_df = pd.read_csv(playlist_ds[i])
    song_df = pd.read_csv('spotify_data.csv')

    collab_rec = CollaborativeFilteringRecSys(playlist_df, song_df, k=num_recs)
    collab_rec.preprocess_data()
    collab_rec.train_model()
    playlist_data = playlist_df.iloc[0]  # Example: Get recommendations for the first playlist
    recommendations = collab_rec.recommend(playlist_data)
    print(recommendations)
    pd.DataFrame(recommendations).to_csv(f'Results/{i}_collab_recs.csv', index=False) # Save the DataFrame to a CSV file before returning

    num_recs+=5
    num_training_songs += 10

num_recs = 10
num_training_songs = 25
for i in range(len(track_ids)): 
    
    print('')
    print('====Content Filtering Recommendation System====')

    liked_songs_dataset = pd.read_csv('ahhhhhhhhhhhhhhhhhhhhhlejandro_liked_songs.csv')
    song_df = pd.read_csv('spotify_data.csv')

    # Create an instance of the ContentBasedRecSys class
    rec_sys = ContentBasedRecSys(
        song_dataset=song_df,
        liked_songs_dataset=liked_songs_dataset,
        n_songs=num_training_songs,
        test_size=0.2
    )

    # Preprocess the data
    rec_sys.preprocess_data()

    # Train the model
    rec_sys.train_model()

    # Get recommendations for a specific song
    song_id = track_ids[i]  # Turn off the lights track id 
    recommendations = rec_sys.recommend(song_id, num_recs)

    # Print the recommendations
    if recommendations is not None:
        print(f"Recommendations for song ID {song_id}:")
        print(recommendations[['track_id', 'track_name', 'artist_names']])

        # Convert the list of dictionaries to a DataFrame
    pd.DataFrame(recommendations).to_csv(f'Results/{i}_content_recs.csv', index=False) # Save the DataFrame to a CSV file before returning

    num_recs+=5
    num_training_songs += 10