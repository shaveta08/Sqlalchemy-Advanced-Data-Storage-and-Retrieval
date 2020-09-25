# Sqlalchemy-Advanced-Data-Storage-and-Retrieval

* I have used Python and SQLAlchemy to do basic climate analysis of hawaii state and data exploration of its climate database for planning vacation in hawaii. 
All of the following analysis have been completed using SQLAlchemy ORM queries, Pandas, and Matplotlib.
* DataBase-File : hawaii.sqlite
* I have choosen a start date and end date for my trip for analysation of climate changes in previous years on those dates.
* Using SQLAlchemy create_engine to connect to my sqlite database.
* Using SQLAlchemy automap_base() to reflect the tables into classes and save a reference to those classes called Station and Measurement.
## Step1:  Climate Analysis and Exploration
## Precipitation Analysis
  * Desiged a query to retrieve the last 12 months of precipitation data.
  * Selected only the date and prcp values.
  * Loading the query results into a Pandas DataFrame and set the index to the date column.
  * Sorting the DataFrame values by date.
  * Ploting the results using the DataFrame plot method.
  ![alt text](https://github.com/shaveta08/Sqlalchemy-Advanced-Data-Storage-and-Retrieval/blob/master/Images/Precipitation_and_dates.png)
  
## Station Analysis
  * Designing a query to calculate the total number of stations.
  * Designing a query to find the most active stations.
  * List the stations and observation counts in descending order.
  * Finding the station with most number of observations.
  * Designing a query to retrieve the last 12 months of temperature observation data (TOBS).
  * Filtering by the station with the highest number of observations.
  * Ploting the results as a histogram with bins=12.
  ![alt text](https://github.com/shaveta08/Sqlalchemy-Advanced-Data-Storage-and-Retrieval/blob/master/Images/Temprature_frequency.png)
  
## Temperature Analysis I
  * Identifying the average temperature in June at all stations across all available years in the dataset. Did the same for December temperature. 
  * Ttest on Average Temp of June and December.
      We have used the unpaired ttest, as we have one depent variable here (Temprature) and two independent variables i.e. months June and December.
      Null hypothesis : There is no significant difference in the temprature in months june and december.
  * Result: 
      After doing ttest we have observed pvalue to be less then threshold value i.e. .05 So we Reject the null hypothesis. Which means there is significant difference between         the temprature means in both the months.
      
      
## Temprature Analysis II
  * Ploting the min, avg, and max temperature for our trip using the matching dates from the previous year (i.e., use "2017-01-01" if your trip start date was "2018-01-01").       query as a bar chart.
      - Using the average temperature as the bar height.
      - Using the peak-to-peak (TMAX-TMIN) value as the y error bar (YEAR).
      ![alt text](https://github.com/shaveta08/Sqlalchemy-Advanced-Data-Storage-and-Retrieval/blob/master/Images/Trip_avg_temp_bar_graph.png)
      ![alt text](https://github.com/shaveta08/Sqlalchemy-Advanced-Data-Storage-and-Retrieval/blob/master/Images/Temprature_and_trip_date_area_graph.png)
      
 ## Step2:  Climate App
 Now that we have completed our initial analysis, designing a Flask API based on the queries that w have just developed.
 Using Flask to create our routes.
 *  /
  Home page.
  Listing all routes that are available.
 * /api/v1.0/precipitation
  Converting the query results to a dictionary using date as the key and prcp as the value.
  Returning the JSON representation of your dictionary.
 * /api/v1.0/stations
  Returning a JSON list of stations from the dataset.
 * /api/v1.0/tobs
  Querying the dates and temperature observations of the most active station for the last year of data.
  Returning a JSON list of temperature observations (TOBS) for the previous year.
 * /api/v1.0/<start> and /api/v1.0/<start>/<end>
  Returning a JSON list of the minimum temperature, the average temperature, and the max temperature for a given start or start-end range.
  When given the start only, calculate TMIN, TAVG, and TMAX for all dates greater than and equal to the start date.
  When given the start and the end date, calculate the TMIN, TAVG, and TMAX for dates between the start and end date inclusive.


To run the Flask App:
Step1: Clone the repo.
Step2: Run the app.py file on your local host (Make sure all the Flask libraries are installed on your local environment)
