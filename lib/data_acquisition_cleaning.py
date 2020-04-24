import pandas as pd

def load_song_data():
    return pd.read_csv("data/classic-rock-song-list.csv")

# returns a list of strings containing song titles and artists to be queried
def get_title_artist(song_data):
    return list(zip(
        song_data['Song Clean'], 
        song_data['ARTIST CLEAN']
    ))

def get_artists_and_song_count(raw_song_data):
    artist_count = raw_song_data.loc[:, ['ARTIST CLEAN', 'Song Clean']]\
             .groupby('ARTIST CLEAN')\
             .count()

    return artist_count.reset_index()\
                .rename(columns={
                    'ARTIST CLEAN': 'Artist Name',
                    'Song Clean': 'Num Songs Included'})\
                .sort_values(by='Num Songs Included', ascending=False)