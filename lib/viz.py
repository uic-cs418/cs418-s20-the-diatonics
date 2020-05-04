from sklearn.tree import DecisionTreeClassifier
import seaborn as sns
from matplotlib import pyplot as plt
from sklearn.manifold import TSNE
import pandas as pd


def spotify_property_dist_graph(data):
    plot = sns.boxplot(
        data=data.drop(columns=['tempo', 'loudness', 'key'])
    )
    plot.set(
        xlabel='Spotify Track Property', 
        ylabel='Scaled Value',
        title='Distribution of Spotify Track Property Values'
    )
    plot.set_xticklabels(
        plot.get_xticklabels(),
        rotation=75
    )
    plt.show()

def get_release_year_distribution_graph(raw_song_data):
    eda_data = raw_song_data.copy()
    eda_data = eda_data.loc[:, ['Release Year']]\
                    .dropna()\
                    .loc[eda_data['Release Year'] > 1500.0]
    plot = sns.violinplot(
        data=eda_data,
        x='Release Year'
    )
    plot.set(title='Distribution of Track Release Year')

def plot_TSNE(tracks_with_audio_features,cluster_type):
    tsnedf = tracks_with_audio_features.copy().drop(columns=['artist', 'title', 'cluster_km','cluster_ag'])
    model = TSNE(n_components=2, random_state=0, perplexity=50, learning_rate=900)
    tsne_object = model.fit_transform(tsnedf)
    tsne_df = pd.DataFrame(data=tsne_object, columns=('TSNE Dimension 1', 'TSNE Dimension 2'))
    if cluster_type == 'KM':
        tsne_df['cluster_km'] = tracks_with_audio_features.cluster_km
        sns.FacetGrid(tsne_df, hue='cluster_km', height=5).map(plt.scatter, 'TSNE Dimension 1', 'TSNE Dimension 2', 'cluster_km')
    elif cluster_type == 'AG':
        tsne_df['cluster_ag'] = tracks_with_audio_features.cluster_ag
        sns.FacetGrid(tsne_df, hue='cluster_ag', height=5).map(plt.scatter, 'TSNE Dimension 1', 'TSNE Dimension 2', 'cluster_ag')
    
    plt.show()

def compare_center_features(center):
    center2 = center.copy()
    plot = sns.boxplot(
    data=center2.drop(columns=['tempo', 'loudness', 'key', 'cluster_km','cluster_ag'])
    )
    plot.set(
        xlabel='Spotify Track Property', 
        ylabel='Scaled Value',
        title = 'Distribution of Spotify Track Properties of Representative Songs'
    )
    plot.set_xticklabels(
        plot.get_xticklabels(),
        rotation=75
    )

def compare_centers(centersDF):
    centersDF = centersDF.sort_values(by=['liveness'])
    toPlot = centersDF.copy()
    artistSeries = centersDF.artist
    songSeries = centersDF.title
    toPlot = toPlot.drop(columns=['title','artist','cluster'])
    fig = plt.figure()
    fig.set_size_inches(90,50)
    for i, row in enumerate(centersDF.iterrows()):
        ax = plt.subplot(10,5,i+1)
        ax.set_title(artistSeries.iloc[i] + " - " + songSeries.iloc[i] )
        ax.bar(toPlot.columns.values,toPlot.iloc[i])

def tree_viz(clusteredDF):
    features = clusteredDF.copy().drop(columns=['artist', 'title', 'cluster']).columns.values
    x = clusteredDF[features]
    y = clusteredDF['cluster']
    tree = DecisionTreeClassifier(min_samples_split=100)
    dt = tree.fit(x,y)
    return dt