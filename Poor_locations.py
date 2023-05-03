## Locations on map by cluster
import mysql.connector
import pandas as pd
import geopandas as gpd
import matplotlib.pyplot as plt
import re  # Used in sentence_case function


def _obtain_data():
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

    # Create query
    query = "SELECT nameText, specialisedZoneType, lon, lat, quality2021 " \
            "FROM fr_bw2021 WHERE lon BETWEEN -20 AND 20 AND lat BETWEEN 30 AND 60 AND quality2021 <> 'Not classified'"

    # Issue SQL queries by calling the execute() method of the cursor object:
    mycursor.execute(query)

    # Retrieve the results of the query using the fetchall() method:
    myresult = mycursor.fetchall()

    # Create a pandas DataFrame from the list of tuples:
    df = pd.DataFrame(myresult, columns=['nameText', 'specialisedZoneType', 'lon', 'lat', 'quality2021'])

    return df


def map_bathing_quality():
    df = _obtain_data()

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
    plt.xlabel('Longitude (degrees)')
    plt.ylabel('Latitude (degrees)')
    plt.legend()
    plt.show()

    # we now display bathing water types
    locations = gdf.groupby('specialisedZoneType')

    # plot the map and locations
    fig, ax = plt.subplots(figsize=(10, 10))
    france.plot(ax=ax, alpha=0.4, color='grey')

    # we plot different types in different colours
    colors = {'coastalBathingWater': 'lightseagreen', 'riverBathingWater': 'green', 'lakeBathingWater': 'purple',
              'transitionalBathingWater': 'red'}
    for water_type, dff in locations:
        dff.plot(ax=ax, markersize=2, color=colors[water_type], label=f'{water_type[:-12].title()}')

    plt.title('Bathing water type')
    plt.legend()
    plt.xlabel('Longitude (degrees)')
    plt.ylabel('Latitude (degrees)')
    plt.show()


def _sentence_case(ind):
    string = str(ind)[0].lower() + str(ind)[1:]
    result = re.sub('([A-Z])', r' \1', string)
    return result[0].upper() + result[1:].lower()


def _process_series(series, color_dict):
    df_from_series = series.to_frame()
    df_from_series.apply(_sentence_case, axis=0)
    df_from_series['colour'] = df_from_series.index.map(color_dict)

    return df_from_series


def _pie_chart(df, col: str, colour_dict: dict):
    series_qual_counts = df.value_counts(col)

    df_qual_counts = _process_series(series_qual_counts, colour_dict)

    # Create pie chart with custom colors and labels
    labels_sentence_case = [_sentence_case(index) for index in df_qual_counts.index]
    label_font = {'size': 14}
    plt.pie(df_qual_counts['count'], labels=labels_sentence_case, colors=df_qual_counts['colour'], autopct='%1.1f%%',
            pctdistance=1.15, labeldistance=1.35, textprops=label_font)


def data_distribution():
    df = _obtain_data()
    qual_colors = {'Excellent': 'blue', 'Good': 'green', 'Sufficient': 'yellow', 'Poor': 'red'}

    _pie_chart(df, 'quality2021', qual_colors)
    font = {'weight': 'bold', 'size':18}
    plt.title('Water quality distribution', fontdict=font)
    plt.show()

    loc_colors_dict = {'coastalBathingWater': 'lightseagreen', 'riverBathingWater': 'green',
                       'lakeBathingWater': 'purple',
                       'transitionalBathingWater': 'red'}

    _pie_chart(df, 'specialisedZoneType', loc_colors_dict)

    # Display pie chart
    plt.title('Bathing spot type \n \n', fontdict=font)
    plt.show()
