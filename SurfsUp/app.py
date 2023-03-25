# Import the dependencies.
import numpy as np

import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func

import datetime as dt
from dateutil.relativedelta import relativedelta

from flask import Flask, jsonify


#################################################
# Database Setup
#################################################
# reflect an existing database into a new model
engine = create_engine("sqlite:///Resources/hawaii.sqlite")
Base = automap_base()

# reflect the tables
Base.prepare(autoload_with=engine)

# Save references to each table
measurement = Base.classes.measurement
Station = Base.classes.station

# Create our session (link) from Python to the DB
session = Session(engine)

#################################################
# Flask Setup
#################################################
app = Flask(__name__)

#################################################
# Flask Routes
#################################################

@app.route("/")
def welcome():
    """List all available api routes."""
    return (
        f"Hawaii Weather Data:<br/><br>"
        f"<a href=\"/api/v1.0/precipitation\">/api/v1.0/precipitation<a><br/>"
        f"<a href=\"/api/v1.0/stations\">/api/v1.0/stations<a><br/>"
        f"<a href=\"/api/v1.0/tobs\">/api/v1.0/tobs<a><br/>"
        f"/api/v1.0/start_date<br/>"
        f"/api/v1.0/start/end<br/>"
        f"Note: Please ensure you enter both dates using format: YYYY-mm-dd/YYYY-mm-dd"
    )

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

@app.route("/api/v1.0/stations")
def stations():
    
    # Create our session (link) from Python to the DB
    session = Session(engine)

    #Create a list of stations 
    station_query_results = session.query(Station.station,Station.id).all()

    session.close()

    # Create a dictionary from the row data and append to a list
    stations_all = []
    for station, id in station_query_results:
        stations_values_dict = {}
        stations_values_dict['station'] = station
        stations_values_dict['id'] = id
        stations_all.append(stations_values_dict)

    return jsonify (stations_all)

@app.route("/api/v1.0/tobs")
def temps():

    # Create our session (link) from Python to the DB
    session = Session(engine)

    # Query the data
    results = session.query(measurement.date, measurement.tobs, measurement.prcp).\
        filter(measurement.date >= '2016-08-23').\
        filter(measurement.station=='USC00519281').\
        order_by(measurement.date).all()
    
    session.close()

    # Create a dictionary using the query results 

    all_temps = []
    for prcp, date, tobs in results:
        temps_dict = {}
        temps_dict["precip"] = prcp
        temps_dict["date"] = date
        temps_dict["temp"] = tobs
        
        all_temps.append(temps_dict)

    return jsonify(all_temps)

@app.route("/api/v1.0/<start_date>")
def date_1(start_date, end_date='2017-08-23'):

    # Create our session (link) from Python to the DB
    session = Session(engine)

    #Calculate minimum, average and maximum temperatures for the date range.
    query_result = session.query(func.min(measurement.tobs), func.avg(measurement.tobs), func.max(measurement.tobs)).\
        filter(measurement.date >= start_date).filter(measurement.date <= end_date).all()
    
    session.close()

    #Create a dictionary
    date_stats = []

    for min, avg, max in query_result:
        date_dict = {}
        date_dict["Min"] = min
        date_dict["Average"] = avg
        date_dict["Max"] = max
        date_stats.append(date_dict)

    return jsonify(date_stats)

@app.route("/api/v1.0/<start_date>/<end_date>")
def date_2(start_date, end_date):

    # Create our session (link) from Python to the DB
    session = Session(engine)

    #Calculate minimum, average and maximum temperatures for the date range.
    query_result2 = session.query(func.min(measurement.tobs), func.avg(measurement.tobs), func.max(measurement.tobs)).\
        filter(measurement.date >= start_date).filter(measurement.date <= end_date).all()
    
    session.close()

    #Create a dictionary
    date2_stats = []

    for min, avg, max in query_result2:
        date2_dict = {}
        date2_dict["Min"] = min
        date2_dict["Average"] = avg
        date2_dict["Max"] = max
        date2_stats.append(date2_dict)

    return jsonify(date2_stats)