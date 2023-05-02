import geopandas as gpd
import matplotlib.pyplot as plt
from scipy.spatial.distance import cdist
import numpy as np
from data_split import _obtain_data

# radius
our_radius = 0.5

# Create a pandas DataFrame from the list of tuples:
our_df = _obtain_data()

print(our_df.value_counts('quality_num'))

##
def _find_neighbours(df, radius):
    lat_lon = df[['lat', 'lon']].values  # Extract latitude and longitude columns as numpy arrays
    dist_matrix = cdist(lat_lon, lat_lon, 'euclidean')  # pairwise Euclidean distance

    neighbours = [[[dist_matrix[i, j], df.index[j]] for j in range(len(df)) if dist_matrix[i, j] < radius] for i in
                  range(len(df))]

    return neighbours

def _top_n(nbs, n):
    new_nbs = []
    for nb_list in nbs:
        nb_list.sort()  # sorts by lowest distance
        if len(nb_list) >= n:
            nb_list = nb_list[:n]

        nb_list = [distance_index[1] for distance_index in nb_list]  # retrieve indices only
        new_nbs.append(nb_list)

    return new_nbs

def weights(df, radius, n_neighbours: int = 5):
    # Find each point's neighbours (this depends on the radius)
    neighbours = _find_neighbours(df, radius)

    neighbours = _top_n(neighbours, n_neighbours)  # Find closest neighbours
    df['neighbours'] = neighbours

    lens = [len(neighbour_l) for neighbour_l in neighbours]  # number of neighbours

    # weight for each point
    wts = [np.mean([df.loc[i]['quality_num'] for i in neighbours[j]]) for j in range(len(df))]
    df['wts'] = wts

    # Create a GeoDataFrame from the pandas dataframe
    gdf = gpd.GeoDataFrame(geometry=gpd.points_from_xy(df['lon'], df['lat']),
                           data=df[['nameText', 'quality_num', 'wts']])

    # plot distribution
    plt.hist(wts, bins=100)
    plt.show()

    # plot weights
    # load map of France using geopandas
    france = gpd.read_file('Data/Maps/gadm41_FRA_1.shp')

    # plot the map and locations
    fig, ax = plt.subplots(figsize=(10, 10))
    france.plot(ax=ax, alpha=0.4, color='grey')

    # plot the points
    gdf.plot(ax=ax, markersize=2, legend=True, column='wts')

    plt.show()

    # plot bad areas
    bad_in_bad = [df.index[j] for j in range(len(df)) if
                  wts[j] > np.percentile(wts, 97) and df.iloc[j]['quality_num'] > 0
                  and lens[j] >= 5]

    bad_df = df.loc[df.index.isin(bad_in_bad)]
    bad_gdf = gpd.GeoDataFrame(geometry=gpd.points_from_xy(bad_df['lon'], bad_df['lat']),
                               data=bad_df[['nameText', 'quality_num', 'wts']])

    # load map of France using geopandas
    france = gpd.read_file('Data/Maps/gadm41_FRA_1.shp')

    # plot the map and locations
    fig, ax = plt.subplots(figsize=(10, 10))
    france.plot(ax=ax, alpha=0.4, color='grey')

    # we plot different clusters in different colours
    bad_gdf.plot(ax=ax, markersize=2, legend=True, column='wts', vmin=0)

    plt.show()


weights(our_df, our_radius)
