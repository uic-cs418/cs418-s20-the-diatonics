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