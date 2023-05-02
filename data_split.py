##
import mysql.connector
import pandas as pd
import geopandas as gpd
import matplotlib.pyplot as plt
from sklearn.cluster import KMeans
from sklearn.model_selection import train_test_split

from Cluster_analysis import cluster_data

n_optimal, omit = cluster_data()

def _obtain_data():
    # Obtain data
    with open('password.txt') as f:
        my_password = f.readline()

    # Create a connection to the MySQL database by specifying the host, user, password, and database name:
    mydb = mysql.connector.connect(
        host="localhost",
        user="root",
        password=my_password,
        database="my_database"
    )

    # Create a cursor object to execute SQL queries:
    mycursor = mydb.cursor()

    # SQL query
    query = '''
    SELECT
        nameText, specialisedZoneType, lon, lat,
        CAST(CASE quality2021
        WHEN 'Excellent' THEN 0
        WHEN 'Good' THEN 1
        WHEN 'Sufficient' THEN 4
        WHEN 'Poor' THEN 5
        ELSE NULL
    END AS FLOAT) AS quality_num
    FROM fr_bw2021 WHERE quality2021 <> 'Not classified' AND lon BETWEEN -20 AND 20 AND lat BETWEEN 30 AND 60
        AND specialisedZoneType <> 'TransitionalBathingWater'
    '''
    mycursor.execute(query)  # Issue SQL query
    myresult = mycursor.fetchall()  # Retrieve results

    # Create a pandas DataFrame from the list of tuples:
    df = pd.DataFrame(myresult, columns=['nameText', 'specialisedZoneType', 'lon', 'lat', 'quality_num'])

    # Remove omitted locations (maybe just do this via query)
    mask = ~df['nameText'].isin(omit)  # Create a boolean mask based on the list of names
    df = df[mask]

    return df


def _plot_clusters(dff_zones):
    # Plotting data
    # load map of France using geopandas
    france = gpd.read_file('Data/Maps/gadm41_FRA_1.shp')

    # create a geopandas dataframe for locations
    locations = gpd.GeoDataFrame(geometry=gpd.points_from_xy(dff_zones['lon'], dff_zones['lat']),
                                 data=dff_zones[['nameText', 'labels']])

    # group by cluster, in our desired order
    locations = locations.groupby('labels')

    # plot the map and locations
    fig, ax = plt.subplots(figsize=(10, 10))
    france.plot(ax=ax, alpha=0.4, color='grey')

    # we plot different clusters in different colours
    for cluster, dfff_zones_clusters in locations:
        dfff_zones_clusters.plot(ax=ax, markersize=2, label=f'cluster {hash(cluster) + 1}')

    plt.legend()
    plt.show()


def _obtain_clusters(dff_zone, water_type):
    # Initialize the clustering algorithm
    kmeans = KMeans(n_clusters=n_optimal[water_type], n_init=10)

    # Fit the algorithm to the data
    coords = dff_zone[['lon', 'lat']].values
    kmeans.fit(coords)

    return kmeans.labels_

def data_split(plot=False):
    df = _obtain_data()

    train_dfs, test_dfs = [], []
    for water_type, dff_zone in df.groupby('specialisedZoneType'):
        if water_type in n_optimal:
            # Get the cluster labels for each data point
            dff_zone['labels'] = _obtain_clusters(dff_zone, water_type)

            # Plot
            if plot:
                _plot_clusters(dff_zone)

            # Split by cluster
            for cluster, dfff_zones_cluster in dff_zone.groupby('labels'):
                train_df, test_df = train_test_split(dfff_zones_cluster.drop('labels', axis=1),
                                                     test_size=0.2, random_state=42)
                train_dfs.append(train_df)
                test_dfs.append(test_df)

        else:
            train_df, test_df = train_test_split(dff_zone, test_size=0.2, random_state=42)
            train_dfs.append(train_df)
            test_dfs.append(test_df)

    training_set = pd.concat(train_dfs)
    test_set = pd.concat(test_dfs)

    return training_set, test_set
