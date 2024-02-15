# Import the dependencies.

import numpy as np

import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func

from flask import Flask, jsonify

#################################################
# Database Setup
engine = create_engine("sqlite:///titanic.sqlite")
#################################################


# reflect an existing database into a new model
engine = create_engine("sqlite:///Resources/hawaii.sqlite")

# reflect the tables
base=automap_base()
base.prepare(autoload_with=engine)

# Save references to each table
station=base.classes.station
measurement=base.classes.measurement

# Create our session (link) from Python to the DB
session=Session(engine)

#################################################
# Flask Setup
#################################################

app= Flask(__name__)

#################################################
# Flask Routes
#################################################

# - Start at the homepage 
# - list all the available routes
@app.route("/")
def home():
    return(
        f"Available Routes <br/>"
        f"/api/v1.0/precipitation<br/>" 
        f"/api/v1.0/stations<br/>"
        f"/api/v1.0/tobs<br/>"
        f"/api/v1.0/<start> (enter as YYYY-MM-DD)<br/>"
        f"/api/v1.0/<start>/<end> (enter as YYYY-MM-DD/YYYY-MM-DD)"
    )

## Question 2 - '/api/v1.0/precipitation'
# Return the JSON representation of your dictionary

@app.route("/api/v1.0/precipitation")
def precipitation():

    # Create our session (link) from Python to the DB
    session = Session(engine)

 # Query and summarize daily precipitation across all stations for the last year of available data
    
    start_date = '2016-08-23'
    sel = [measurement.date, 
        func.sum(measurement.prcp)]
    precipitation = session.query(*sel).\
            filter(measurement.date >= start_date).\
            group_by(measurement.date).\
            order_by(measurement.date).all()
   
    session.close()

 # Return a dictionary with the date as key and the daily precipitation total as value
    precipitation_dates = []
    precipitation_totals = []

    for date, dailytotal in precipitation:
        precipitation_dates.append(date)
        precipitation_totals.append(dailytotal)
    
    precipitation_dict = dict(zip(precipitation_dates, precipitation_totals))

    return jsonify(precipitation_dict)

# Query the last 12 months of temperature observation data for the most active station
@app.route("/api/v1.0/tobs")
def tobs():
    session = Session(engine)
    start_date = '2016-08-23'
    sel=[measurement.date,measurement.tobs]
    station_temps=session.query(*sel).\
            filter(measurement.date >= start_date, measurement.station == 'USC00519281').\
            group_by(measurement.date).\
            order_by(measurement.date).all()
    session.close()

# Return a dictionary with the date as key and the daily temperature observation as value
    observation_dates = []
    temperature_observations = []

    for date, observation in station_temps:
        observation_dates.append(date)
        temperature_observations.append(observation)
    
    most_active_tobs_dict = dict(zip(observation_dates, temperature_observations))

    return jsonify(most_active_tobs_dict)

# Calculate minimum, average and maximum temperatures for the range of dates starting with start date.# If no end date is provided, the function defaults to 2017-08-23.

@app.route("/api/v1.0/<start>")
def start(start_date, end_date='2017-08-23'):
    
    session = Session(engine)
    query_result = session.query(func.min(measurement.tobs), func.avg(measurement.tobs),\
    func.max(measurement.tobs)).\
    filter(measurement.date >= start_date).filter(measurement.date <= end_date).all()
    session.close()

    start_stats = []
    for min, avg, max in query_result:
        start_dict = {}
        start_dict["Min"] = min
        start_dict["Average"] = avg
        start_dict["Max"] = max
        start_stats.append(start_dict)

        return jsonify(start_stats)

@app.route("/api/v1.0/<start>/<end>")
def start_end(start_date, end_date='2017-08-23'):

    session = Session(engine)
    query_result = session.query(func.min(measurement.tobs), func.avg(measurement.tobs),\
    func.max(measurement.tobs)).\
    filter(measurement.date >= start_date).filter(measurement.date <= end_date).all()
    session.close()

    start_end_stats = []
    for min, avg, max in query_result:
        start_end_dict = {}
        start_end["Min"] = min
        start_end["Average"] = avg
        start_end["Max"] = max
        start_end_stats.append(start_end_dict)

        return jsonify(start_end_stats)

if __name__ == "__main__":
    app.run(debug=True)
