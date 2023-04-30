##
import mysql.connector
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.cluster import KMeans

##
def cluster_analysis(zone: str, max_clusters: int = 20):
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
        nameText, lon, lat
    FROM fr_bw2021 WHERE quality2021 <> 'Not classified' AND lon BETWEEN -20 AND 20 AND lat BETWEEN 30 AND 60
        AND specialisedZoneType = %s
    '''
    mycursor.execute(query, (zone,))  # Issue SQL query
    myresult = mycursor.fetchall()  # Retrieve results

    # Create a pandas DataFrame from the list of tuples:
    df = pd.DataFrame(myresult, columns=['nameText', 'lon', 'lat'])

    # Create numpy array of coordinates
    coords = df[['lon', 'lat']].values

    inertia = []  # Will hold SSE for each number of clusters
    for n_clusters in range(1, max_clusters + 1):
        # Initialize the clustering algorithm
        kmeans = KMeans(n_clusters=n_clusters, n_init=10)

        # Fit the algorithm to the data
        kmeans.fit(coords)

        # Get the cluster labels for each data point
        df['labels'] = kmeans.labels_

        # Append SSE
        inertia.append(kmeans.inertia_)

    # Plot SSE by number of clusters to find "elbow point"
    plt.plot(inertia)
    plt.show()


def cluster_data():
    # Used to record optimal number of clusters
    # Also records points that don't fit in
    n_optimal = {'RiverBathingWater': 4, 'LakeBathingWater': 7}
    omit = ['CAMPING-PLAGE DU FLECKENSTEIN LEMBACH']

    return n_optimal, omit
