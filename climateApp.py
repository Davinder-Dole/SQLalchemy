import numpy as np
import pandas as pd

import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func
import datetime as dt

from flask import Flask, jsonify


 #Database Setup_________

engine = create_engine("sqlite:///Resources/hawaii.sqlite")

# reflect an existing database into a new model
Base = automap_base()
# reflect the tables
Base.prepare(engine, reflect=True)

# Save reference to the table
Measurements = Base.classes.measurement
Stations = Base.classes.station


# Create our session (link) from Python to the DB
session = Session(engine)


# Flask Setup
app = Flask(__name__)

# Flask Routes

@app.route("/")
def welcome():
    return (
        f"List of all the available api routes.<br>"
        f"/api/v1.0/precipitation<br/>"
        f"/api/v1.0/stations<br>"
        f"/api/v1.0/tobs<br>"
        f"/api/v1.0/<start>/<end><br>"
    )


@app.route("/api/v1.0/precipitation")
def precipitation():
    last_date = session.query(Measurements.date).order_by(Measurements.date.desc()).first()
    last_year = dt.date(2017, 8, 23) - dt.timedelta(days=365)
    """Return a list of all precipitation data"""
    # Query all passengers
    precipitation_data = session.query(Measurements.date, Measurements.prcp).\
                            filter(Measurements.date > last_year).\
                                order_by(Measurements.date).all()
# Create a list of dicts with `date` and `prcp` as the keys and values
    prcp_totals = []
    for data in precipitation_data:
        row = {}
        row["date"] = data[0]
        row["prcp"] = data[1]
        prcp_totals.append(row)
    return jsonify(prcp_totals)
    
        
@app.route("/api/v1.0/stations")
def stations():
    """Return a list of all stations names"""
    # Query all passengers
    stations_data = session.query(Stations.id, Stations.station,Stations.name)
    s = []
    for data in stations_data:
        s.append(data)
    return jsonify(s)

@app.route("/api/v1.0/station")
def station():
    results = session.query(Stations.station).all()

    # Convert list of tuples into normal list
    all_stations = list(np.ravel(results))

    return jsonify(all_stations)

@app.route("/api/v1.0/tob")
def tob():
    last_date = session.query(Measurements.date).order_by(Measurements.date.desc()).first()
    last_year = dt.date(2017, 8, 23) - dt.timedelta(days=365)
    temp_data = session.query(Measurements.date, Measurements.tobs).\
                            filter(Measurements.date > last_year).\
                                order_by(Measurements.date).all()
    temp_totals = []
    for data in temp_data:
         temp_totals.append(data)
    return jsonify(temp_totals)
    
@app.route("/api/v1.0/<start>")
def trip1(start):
    last_date = session.query(Measurements.date).order_by(Measurements.date.desc()).first()
    start = dt.date(2017, 8, 23) - dt.timedelta(days=365)
    calc_data=session.query(func.min(Measurements.tobs),func.max(Measurements.tobs),func.avg(Measurements.tobs)).\
                filter(Measurements.date>=start)
    data=[]
    for i in calc_data:
        data.append(i)
    dict_values={"min Temp":data[0][0],
                 "max Temp":data[0][1],
                 "Average Temp":data[0][2]}
    return jsonify(dict_values)

@app.route("/api/v1.0/<start>/<end>")
def trip2(start,end):
    last_date = session.query(Measurements.date).order_by(Measurements.date.desc()).first()
    start = dt.date(2017, 8, 23) - dt.timedelta(days=365)
    end= start + dt.timedelta(days=100)
    calc_data=session.query(func.min(Measurements.tobs),func.max(Measurements.tobs),func.avg(Measurements.tobs)).\
                filter(Measurements.date>=start).\
                filter(Measurements.date<=end)
    data=[]
    for i in calc_data:
        data.append(i)
    dict_values={"min Temp":data[0][0],
                 "max Temp":data[0][1],
                 "Average Temp":data[0][2]}
    return jsonify(dict_values)



if __name__ == '__main__':
    app.run(debug=True)
