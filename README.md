# Hawaii Weather Analysis

Part 1: Analysis 

The purpose of this code is to analyze climate data from Hawaii using SQLAlchemy and pandas in Python. The code connects to an SQLite database with two tables: measurement and station. The measurement table contains information about precipitation, temperature, and other weather data, while the station table contains information about weather stations. The code analyzes and visualizes the data to provide insights into Hawaii's climate.

Exploratory Precipitation Analysis
In this section, the code retrieves the precipitation data from the measurement table and saves it as a pandas DataFrame. The code also calculates the summary statistics for the precipitation data and plots it over time.

Exploratory Station Analysis
In this section, the code retrieves the station data from the station table and calculates the number of stations in the dataset. The code also finds the most active station and calculates the lowest, highest, and average temperature for that station. Finally, the code plots a histogram of the temperature data for the most active station

Part 2: Flask App

This code is a Flask app that retrieves weather data from an database for Hawaii climate. The app has the following functionality:

/api/v1.0/precipitation: Returns a JSON representation of precipitation observations recorded in Hawaii from 2016-08-23 to the last available date in the dataset. The results are grouped by date.

/api/v1.0/stations: Returns a JSON list of stations from which weather data were recorded.

/api/v1.0/tobs: Returns a JSON representation of temperature observations recorded in Hawaii from 2016-08-23 to the last available date in the dataset for the most active station.

/api/v1.0/start_date: Returns a JSON list of the minimum temperature, the average temperature, and the maximum temperature for a given date range. The start_date should be in the format YYYY-mm-dd.

/api/v1.0/start_date/end_date: Returns a JSON list of the minimum temperature, the average temperature, and the maximum temperature for a given date range. Both the start_date and end_date should be in the format YYYY-mm-dd.

An example of the code used is 

```ruby 
@app.route("/api/v1.0/precipitation")
def precip():
    # Create our session (link) from Python to the DB
    session = Session(engine)

    #create a dictionary of the precipitation
    start_date = '2016-08-23'
    results = [measurement.date, measurement.prcp]
    precip_results = session.query(*results).\
            filter(measurement.date >= start_date).\
            group_by(measurement.date).\
            order_by(measurement.date).all()

    session.close()

    precip_results_final =[]

    for date, prcp in precip_results:
        precip_dict = {}
        precip_dict["date"] = date
        precip_dict["precipitation"] = prcp
        precip_results_final.append(precip_dict)

    return jsonify(precip_results_final)
```
