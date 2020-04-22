import pandas as pd

def load_song_data():
    return pd.read_csv("data/classic-rock-song-list.csv")

# returns a list of strings containing song titles and artists to be queried
def get_title_artist(song_data):
    # extracting title and names of the artists/bands
    titles = song_data['Song Clean'].tolist()
    artists = song_data['ARTIST CLEAN'].tolist()

    # creating a list of titles+aritsts to be queried
    ta_list = []
    for i in range(0, len(titles)):
        ta_list.append(titles[i] + " " + artists[i])

    return ta_list
