import pandas as pd

def load_song_data():
    return pd.read_csv("data/classic-rock-song-list.csv")

# returns a list of strings containing song titles and artists to be queried
def get_title_artist(song_data):
    return list(zip(
        song_data['Song Clean'], 
        song_data['ARTIST CLEAN']
    ))
