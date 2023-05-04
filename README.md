# SQL Project: Bathing water qualities in France
Data obtained [here](https://www.eea.europa.eu/data-and-maps/data/bathing-water-directive-status-of-bathing-water-14) (European Environment Agency)

<p>
 <img src="https://user-images.githubusercontent.com/64332150/235879883-ad6b6379-938e-447e-8505-8f91b352c38b.png" height="378" />
  <img src="https://user-images.githubusercontent.com/64332150/235956932-1caa5f17-bd0c-4646-8503-7e1af7b12049.png" height="378" />
</p>

<p>
 <img src="https://user-images.githubusercontent.com/64332150/235955789-ff57094b-bf15-4b45-8d43-87a2c2e7ab4e.png" height="355" />
 <img src="https://user-images.githubusercontent.com/64332150/235956305-3ef03df5-ba0c-430b-ade7-97a16358bb2d.png" height="355" />
</p>
 
## Case study: Corsica
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
