# Import dependencies
import numpy as np
import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func
import datetime as dt
from flask import Flask, jsonify


#################################################
# Database Setup
#################################################
engine = create_engine("sqlite:///Resources/hawaii.sqlite")

# reflect an existing database into a new model
Base = automap_base()

# reflect the tables
Base.prepare(engine, reflect=True)

# Save reference to the table
measurement = Base.classes.measurement
station = Base.classes.station
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
        f"Available Routes:<br>"
        f"/api/v1.0/precipitation<br>"
        f"/api/v1.0/stations<br>"
        f"/api/v1.0/tobs<br>"
        f"/api/v1.0/start<br>"
        f"/api/v1.0/start/end<br>"
    )


@app.route("/api/v1.0/precipitation")
def prcp():

    """Return precipitation """
    # Convert the query results to a dictionary using date as the key and prcp as the value.
    query_date = dt.date(2017,8,23) - dt.timedelta(days=365)
    prcp_results = session.query(measurement.date, measurement.prcp).filter(measurement.date >= query_date).all()


    prcp_dict = {}
    for date, prcp in prcp_results:
        prcp_dict[date] = prcp
    session.close()

    # Return the JSON representation of your dictionary.
    return jsonify(prcp_dict)

    
@app.route("/api/v1.0/stations")
def stations():
   
    """Return a JSON list of stations from the dataset."""
    # Query all stations
    station_results = session.query(station.station).all()

    
    # Convert list of tuples into normal list
    all_stations = list(np.ravel(station_results))
    session.close()
    return jsonify(all_stations=all_stations)


@app.route("/api/v1.0/tobs")
def tobs():

    """Query the dates and temperature observations of the most active station for the last year of data."""
    # Query all dates and tobs for the last year of data
    query_date = dt.date(2017,8,23) - dt.timedelta(days=365)
    tobs_results = session.query(measurement.tobs).filter(measurement.station == "USC00519281").filter(measurement.date >= query_date).all()

    # Convert list of tuples into normal list
    all_tobs = list(np.ravel(tobs_results))
    session.close()
    return jsonify(all_tobs)


@app.route("/api/v1.0/<start>")
def start(start):

    """Return a JSON list of the minimum temperature, the average temperature, and the max temperature for a given start."""
    # Query temperatures for a given start date
    start_results = session.query(func.min(measurement.tobs), func.max(measurement.tobs), func.avg(measurement.tobs)).filter(measurement.station == 'USC00519281').filter(measurement.date >= start).all()
    
    # Convert list of tuples into normal list
    all_start = list(np.ravel(start_results))
    session.close()
    return jsonify(all_start)


@app.route("/api/v1.0/<start>/<end>")
def start_end(start, end):

    """Return a JSON list of the minimum temperature, the average temperature, and the max temperature for a given start and end date."""
    # Query temperatures for a given start and end date.
    startEnd_results = session.query(func.min(measurement.tobs), func.max(measurement.tobs), func.avg(measurement.tobs).filter(measurement.station == 'USC00519281').filter(measurement.date >= start, measurement.date <= end)).all()

    # Convert list of tuples into normal list
    all_startEnd = list(np.ravel(startEnd_results))
    session.close()
    return jsonify(all_startEnd)


if __name__ == '__main__':
     app.run(debug=True)