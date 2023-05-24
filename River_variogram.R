# Computing river bathing spot variogram
library(RMySQL)
library(geoR)

my_password <- readLines("password.txt", n = 1)

conn <- dbConnect(
  MySQL(),
  dbname = "my_database",
  host = "localhost",
  user = "root",
  password = my_password
)

query <- "SELECT nameText, specialisedZoneType, lon, lat,
  CAST(CASE quality2021
    WHEN 'Excellent' THEN 0
    WHEN 'Good' THEN 0
    WHEN 'Sufficient' THEN 1
    WHEN 'Poor' THEN 1
    ELSE NULL
  END AS FLOAT) AS quality_num
  FROM fr_bw2021 
  WHERE quality2021 <> 'Not classified' 
    AND lon BETWEEN -20 AND 20 AND lat BETWEEN 30 AND 60
    AND specialisedZoneType = 'RiverBathingWater'"

result <- dbGetQuery(conn, query)
geor_data <- as.geodata(result, 
                        coords.col = c("lon", "lat"), data.col = "quality_num")

plot(variog(geor_data, max.dist = 6, option = "bin", distmatrix = "dist"),
     main='Variogram: \nRiver Bathing Spots',
     xlab = "Distance (degrees)", ylab = "Semivariance")
