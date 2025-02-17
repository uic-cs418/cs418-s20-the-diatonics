import json
import pandas as pd
import spotipy
import spotipy.oauth2 as oauth2

def get_spotify_client():
    '''
    Returns an instantiated Spotify API client, using the client id and secret provided in the files ClientID.txt and ClientSecret.txt
    '''

    def read_api_key(filepath):
        with open(filepath, 'r') as f:
            return f.read().replace('\n','')

    clientID = read_api_key('ClientID.txt')
    clientSecret = read_api_key('ClientSecret.txt')
    username = read_api_key('username.txt')
    credentials = spotipy.oauth2.SpotifyClientCredentials(client_id = clientID, client_secret = clientSecret)

    return spotipy.Spotify(client_credentials_manager = credentials)

def get_spotify_resource_urls(title_artist, sp):
    '''
    Queries the Spotify API to retrieve the Spotify resource URL corresponding to a given track
    Input: List of tuples containing titles and artists to search for
    Output: List containing the Spotify resource URLS corresponding to each track
    '''

    url_list = []
    for track_name, artist_name in title_artist:
        try:
            url_list.append(
                (
                    track_name,
                    artist_name,
                    sp.search(
                        q=track_name + ' ' + artist_name, type='track', limit=1
                    )['tracks']['items'][0]['external_urls']['spotify']
                )
            )
        except:
            None
          # print(song)
    return url_list

def get_audio_features(tracks_to_query, sp):
    '''
    Retrieves the Spotify audio features for a collection of urls.
    Input: List of Spotify song urls
    Output: Dataframe containing the audio features for each track
    '''
    urls = [track[2] for track in tracks_to_query]
    audio_features_dict = sp.audio_features(tracks=urls)
    tracks = []
    cleaned_features = []
    for index, item in enumerate(audio_features_dict):
        if item:
            tracks.append(tracks_to_query[index])
            cleaned_features.append(audio_features_dict[index])
    df = pd.DataFrame.from_dict(cleaned_features)
    df = df.drop(columns=['time_signature', 'duration_ms', 'mode', 'type', 'id', 'uri','track_href','analysis_url'])

    track_names = [track[0] for track in tracks]
    artist_names = [track[1] for track in tracks]
    df['title'] = track_names
    df['artist'] = artist_names

    return df


def audio_features(tracks_to_query, sp):
    '''
    A wrapper for `get_audio_features()`, which gets the audio features of 100 songs 
    at a time, and then returns the combined results.
    Input: List of tuples containing track names, artist names, and Spotify song urls
    Output: Dataframe containing the audio features for each track
    '''
    j=0
    dataframe = pd.DataFrame()
    while(True):
        if j+100 < len(tracks_to_query):
            df = get_audio_features(tracks_to_query[j:j+100], sp)
            dataframe = dataframe.append(df)
            j = j+100
        else:
            df = get_audio_features(tracks_to_query[j:len(tracks_to_query)], sp)
            dataframe = dataframe.append(df)
            break
    dataframe.reset_index(inplace = True)
    dataframe.drop(columns=['index'], inplace=True)
    return dataframe