import json
import pandas as pd
import spotipy
import spotipy.oauth2 as oauth2

#def get_spotify_client():
#    '''
#    Returns an instantiated Spotify API client, using the client id and secret provided in the files ClientID.txt and #ClientSecret.txt
#    '''

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

