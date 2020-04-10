#below are some functions from Mahdi's branch from the original project idea

def clean(name):
    cl_str = ''
    for word in name.split():
        if word not in ['featuring', 'Featuring', '&', ',', 'X', 'x', '/', 'With', 'Carter', 'Presents']:
            cl_str = cl_str + word + ' '
    return cl_str

# returns a list of strings containing song titles and artists to be queried
def get_title_artist(chart):
    talist = []
    for i in range(0,100):
        title_artist = clean(chart[i].title)+' '+clean(chart[i].artist)
        talist.append(title_artist)
    return talist

def get_url(title_artist):
    sp = spotipy.Spotify(client_credentials_manager = credentials)
    url_list = []
    for song in title_artist:
        try:
            url_list.append(sp.search(q=song, type='track', limit=1)['tracks']['items'][0]['external_urls']['spotify'])
        except:
            print(song)
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

