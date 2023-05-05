# SQL Project: Bathing water qualities in France
See [here](https://github.com/L-Arscott/SQL_Project_Water_Quality/blob/master/README.md) for optimal view.  
Data obtained [here](https://www.eea.europa.eu/data-and-maps/data/bathing-water-directive-status-of-bathing-water-14) (European Environment Agency).

<p>
 <img src="https://user-images.githubusercontent.com/64332150/235879883-ad6b6379-938e-447e-8505-8f91b352c38b.png" height="378" />
  <img src="https://user-images.githubusercontent.com/64332150/235956932-1caa5f17-bd0c-4646-8503-7e1af7b12049.png" height="378" />
</p>

<p>
 <img src="https://user-images.githubusercontent.com/64332150/235955789-ff57094b-bf15-4b45-8d43-87a2c2e7ab4e.png" height="355" />
 <img src="https://user-images.githubusercontent.com/64332150/235956305-3ef03df5-ba0c-430b-ade7-97a16358bb2d.png" height="355" />
</p>
 
## Case study: Corsica
We take Corsica as a case study:
<p>
 <img src="https://user-images.githubusercontent.com/64332150/236468392-3696aaf7-8fe3-4e74-bc1c-f46e99fca4fd.png" height="400" />
 <img src="https://user-images.githubusercontent.com/64332150/236476413-2516e4c8-1d6b-4c1d-9897-e7ce9bc08630.png" height="500" />
</p>

We note 28% of river spots are rated sufficient or poor in Corsica against 16% for the general population.  
Additionally, only 1 out of 169 coastal locations is rated sufficient or poor (~0.59%), while 5% are rated sufficient or poor accross France.  
There appears to be a high rate of (sufficient or) poor river locations in Corsica, and a low rate of (sufficient or) poor coastal locations in Corsica.  
If this discrepency can be made concrete, this appears to be strong evidence against geospatial correlation of river and coastal locations.

### Analysis: Hypergeoetric distribution
(To do)


## Coastal bathing spots: identification of neighbourhoods with poor bathing spots
We assume spatial correlation of data points.  
In this section we identify particularly poors bathing locations on the coast.  
To account for varying spatial density in data points, and to smooth out effects of outliers, each point is assigned a weight based on its own quality
and that of its 4 nearest neighbours. To account for the skewed nature of our data, we assign weights as follows:  
'Excellent': 0  
'Good': 1  
'Sufficient': 4  
'Poor': 5  

<p>
 <center>
 <img src="https://user-images.githubusercontent.com/64332150/236251849-b1d7401d-e7ac-44d9-8637-743b4f6540f8.png" height="450" />
 </center>
</p>
