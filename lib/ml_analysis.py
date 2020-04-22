from sklearn.cluster import KMeans

def scale_columns(cols, df, scaler):
    '''
    Replaces the data in the given columns with its scaled equivalent
    '''
    for col in cols:
        scaler.fit(df[[col]])
        df[[col]] = scaler.transform(df[[col]])

def recommend(song, dataframe):
    try:
        clt = dataframe[dataframe.title == song].cluster.values[0]
        df = dataframe[dataframe.cluster == clt][['title', 'artist']].reset_index().drop(columns=['index'])
        return df
    except:
        print('The requested song is not in dataframe.')


def cluster_songs(df, num_clusters = 50):
    # k-means clustering algorithm with 50 clusters
    km = KMeans(n_clusters=num_clusters)
    return km.fit_predict(
        df[['danceability', 'energy', 'key', 'loudness', 'speechiness',
            'acousticness','instrumentalness', 'liveness', 'valence', 'tempo']])