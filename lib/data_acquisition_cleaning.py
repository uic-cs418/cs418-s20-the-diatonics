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

def read_api_key(filepath):
    with open(filepath, 'r') as f:
        return f.read().replace('\n','')

def get_url(title_artist):
    sp = spotipy.Spotify(client_credentials_manager = credentials)
    url_list = []
    for song in title_artist:
        try:
            url_list.append(sp.search(q=song, type='track', limit=1)['tracks']['items'][0]['external_urls']['spotify'])
        except:
            print(song)
    return url_list

def get_audio_features(urls):
    audio_features_dict = sp.audio_features(tracks=urls)
    df = pd.DataFrame.from_dict(audio_features_dict)
    df = df.drop(columns=['type', 'id', 'uri','track_href','analysis_url'])
    return df

