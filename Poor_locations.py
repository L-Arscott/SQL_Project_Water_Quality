## Locations on map by cluster
import mysql.connector
import pandas as pd
import geopandas as gpd
import matplotlib.pyplot as plt

with open('password.txt') as f:
    my_password = f.readline()

def map_bathing_quality():
    # Create a connection to the MySQL database by specifying the host, user, password, and database name:
    mydb = mysql.connector.connect(
        host="localhost",
        user="root",
        password=my_password,
        database="my_database"
    )

    # Create a cursor object to execute SQL queries:
    mycursor = mydb.cursor()

    # Create query
    query = "SELECT nameText, specialisedZoneType, lon, lat, quality2021 " \
            "FROM fr_bw2021 WHERE lon BETWEEN -20 AND 20 AND lat BETWEEN 30 AND 60 AND quality2021 <> 'Not classified'"

    # Issue SQL queries by calling the execute() method of the cursor object:
    mycursor.execute(query)

    # Retrieve the results of the query using the fetchall() method:
    myresult = mycursor.fetchall()

    # Create a pandas DataFrame from the list of tuples:
    df = pd.DataFrame(myresult, columns=['nameText', 'specialisedZoneType', 'lon', 'lat', 'quality2021'])
    print(df.value_counts('quality2021'))  # Provide a count
    print(df.value_counts('specialisedZoneType'))

    # Plotting data
    # load map of France using geopandas
    france = gpd.read_file('Data/Maps/gadm41_FRA_1.shp')

    # create a geopandas dataframe for locations
    gdf = gpd.GeoDataFrame(geometry=gpd.points_from_xy(df['lon'], df['lat']),
                           data=df[['nameText', 'specialisedZoneType', 'quality2021']])
    print(gdf.head())

    # group by cluster, in our desired order
    desired_order = {'Excellent': 0, 'Good': 1, 'Sufficient': 2, 'Poor': 3}
    qualities = pd.Categorical(df['quality2021'], categories=desired_order, ordered=True)
    locations = gdf.groupby(qualities)

    # plot the map and locations
    fig, ax = plt.subplots(figsize=(10, 10))
    france.plot(ax=ax, alpha=0.4, color='grey')

    # we plot different qualities in different colours
    colors = {'Excellent': 'blue', 'Good': 'green', 'Sufficient': 'yellow', 'Poor': 'red'}
    for quality, dff in locations:
        dff.plot(ax=ax, markersize=2, color=colors[quality], label=f'{quality} quality')

    plt.title('Bathing water quality')
    plt.legend()
    plt.show()

    # we now display bathing water types
    locations = gdf.groupby('specialisedZoneType')

    # plot the map and locations
    fig, ax = plt.subplots(figsize=(10, 10))
    france.plot(ax=ax, alpha=0.4, color='grey')

    # we plot different types in different colours
    colors = {'coastalBathingWater': 'blue', 'riverBathingWater': 'green', 'lakeBathingWater': 'purple',
              'transitionalBathingWater': 'red'}
    for water_type, dff in locations:
        dff.plot(ax=ax, markersize=2, color=colors[water_type], label=f'{water_type[:-12]}')

    plt.title('Bathing water type')
    plt.legend()
    plt.show()

    # conduct some simple statistics
    for water_type, dff in locations:
        print(water_type)
        print(dff['quality2021'].value_counts())


map_bathing_quality()
