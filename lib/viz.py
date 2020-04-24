import seaborn as sns

def spotify_property_dist_graph(data):
    plot = sns.boxplot(
        data=data.drop(columns=['tempo', 'loudness', 'key'])
    )
    plot.set(
        xlabel='Spotify Track Property', 
        ylabel='Scaled Value'
    )
    plot.set_xticklabels(
        plot.get_xticklabels(),
        rotation=75
    )

def get_release_year_distribution_graph(raw_song_data):
    eda_data = raw_song_data.copy()
    eda_data = eda_data.loc[:, ['Release Year']]\
                    .dropna()\
                    .loc[eda_data['Release Year'] > 1500.0]
    sns.violinplot(
        data=eda_data,
        x='Release Year'
    )