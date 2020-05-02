from sklearn.tree import DecisionTreeClassifier
import seaborn as sns
from matplotlib import pyplot as plt

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