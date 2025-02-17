from sklearn.cluster import KMeans
from sklearn.cluster import AgglomerativeClustering
from sklearn.metrics import pairwise_distances_argmin_min
from sklearn.preprocessing import MinMaxScaler
from sklearn.metrics import silhouette_score
import spotify

def scale_columns(cols, df):
    '''
    Replaces the data in the given columns with its scaled equivalent
    '''
    scaler = MinMaxScaler()
    for col in cols:
        scaler.fit(df[[col]])
        df[[col]] = scaler.transform(df[[col]])

def recommend(title,artist,dataframe,sp,tracks_to_query):
    track = spotify.get_spotify_resource_urls([(title,artist)],sp)
    df1 = spotify.audio_features(track,sp)
    
    df2 = spotify.audio_features(tracks_to_query, sp).append(df1)
    scaler = MinMaxScaler()
    
    scaler.fit(df2[['loudness']])
    df2[['loudness']] = scaler.transform(df2[['loudness']])
    scaler.fit(df2[['key']])
    df2[['key']] = scaler.transform(df2[['key']])
    scaler.fit(df2[['tempo']])
    df2[['tempo']] = scaler.transform(df2[['tempo']])
    
    df = df2.tail(1)
    dis = []
    for i in range(0,50):
        sse = 0
        for j in range(0,10):
            sse += pow(df.iloc[0,j] - dataframe[dataframe.cluster_km == i].drop(columns=['cluster_km', 'cluster_ag']).mean()[j],2)
        dis.append(sse)
    clst = dis.index(min(dis))
    return dataframe[dataframe.cluster_km == clst][['artist', 'title']]


def cluster_songs(df, num_clusters = 50):
    # k-means clustering algorithm with 50 clusters
    km = KMeans(n_clusters=num_clusters)
    prediction = km.fit_predict(df[['danceability', 'energy', 'key', 'loudness', 'speechiness',
            'acousticness','instrumentalness', 'liveness', 'valence', 'tempo']])
    df['cluster_km'] = prediction
    
    # agglomerative clustering algorithm with 50 clusters
    agg = AgglomerativeClustering(n_clusters=50)
    clustering = agg.fit(df[['danceability', 'energy', 'key', 'loudness', 'speechiness', 'acousticness', 
                                      'instrumentalness', 'liveness', 'valence', 'tempo']])
    df['cluster_ag'] = clustering.labels_
    
    # song that are closest to cluster centers of k-means clustering 
    closest, _ = pairwise_distances_argmin_min(km.cluster_centers_, df.iloc[:,0:10])
    center = df.iloc[closest,:]
    return (df, center)

def sil_elb(dataframe):
    sse = []
    sc = []
    for n_clusters in range(50,1500,50):
        km = KMeans(n_clusters=n_clusters)
        preds = km.fit_predict(dataframe[['danceability', 'energy', 'key', 'loudness', 'speechiness', 'acousticness', 
                                      'instrumentalness', 'liveness', 'valence', 'tempo']])
        centers = km.cluster_centers_

        score = silhouette_score(dataframe[['danceability', 'energy', 'key', 'loudness', 'speechiness', 'acousticness', 
                                      'instrumentalness', 'liveness', 'valence', 'tempo']], preds)
        sc.append(score)
        sse.append(km.inertia_)
    return (sse,sc)

def error(column, dataframe):
    total = 0
    for j in range(0,50):
        sum = 0
        for i in range(0,10):
            sum += pow(dataframe[dataframe[column] == j].iloc[:,i] - dataframe[dataframe[column] == j].mean()[i], 2).sum()
        total += sum
    return total