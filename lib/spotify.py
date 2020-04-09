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

def get_spotify_resource_url(title_artist, sp):
    '''
    Queries the Spotify API to retrieve the Spotify resource URL corresponding to a given track
    Input: List containing titles and artists to search for
    Output: List containing the Spotify resource URLS corresponding to each track
    '''
    url_list = []
    for song in title_artist:
        try:
            url_list.append(
                sp.search(
                    q=song, type='track', limit=1
                )['tracks']['items'][0]['external_urls']['spotify']
            )
        except:
            None
          # print(song)
    return url_list

def get_audio_features(urls, sp):
    '''
    Retrieves the Spotify audio features for a collection of urls.
    Input: List of Spotify song urls
    Output: Dataframe containing the audio features for each track
    '''
    audio_features_dict = sp.audio_features(tracks=urls)
    df = pd.DataFrame.from_dict(audio_features_dict)
    df = df.drop(columns=['time_signature', 'mode', 'type', 'id', 'uri','track_href','analysis_url'])
    return df

def audio_features(urls, sp):
    '''
    A wrapper for `get_audio_features()`, which gets the audio features of 100 songs 
    at a time, and then returns the combined results.
    Input: List of Spotify song urls
    Output: Dataframe containing the audio features for each track
    '''
    j=0
    dataframe = pd.DataFrame()
    while(True):
        if j+100 < len(urls):
            df = get_audio_features(urls[j:j+100], sp)
            dataframe = dataframe.append(df)
            j = j+100
        else:
            df = get_audio_features(urls[j:len(urls)], sp)
            dataframe = dataframe.append(df)
            break
    dataframe.reset_index(inplace = True)
    dataframe.drop(columns=['index'], inplace=True)
    return dataframe