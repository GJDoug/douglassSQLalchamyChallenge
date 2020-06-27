import numpy as np
import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func, inspect
from flask import Flask, jsonify
import numpy as np
import pandas as pd
import datetime as dt

engine = create_engine("sqlite:///hawaii.sqlite")

Base = automap_base()
Base.prepare(engine, reflect=True)

Measurement = Base.classes.measurement
Station = Base.classes.station

app = Flask(__name__)


@app.route("/")
def welcome():
    return (
        f"Available Routes:<br/>"
        f"/api/v1.0/precipitation<br/>"
        f"/api/v1.0/stations<br/>"
        f"/api/v1.0/tobs<br/>"
        f"/api/v1.0/start<br/>"
        f"/api/v1.0/start/end<br>"
    )


@app.route("/api/v1.0/precipitation")

def precipitation():
    session = Session(engine)

    # Perform a query to retrieve the data and precipitation scores
    data = session.query(Measurement.date, Measurement.prcp).all()

    session.close()
    
    all_measurements = []
    for date, prcp in data:
        measurement_dict = {}
        measurement_dict['date'] = date
        measurement_dict['prcp'] = prcp
        all_measurements.append(measurement_dict)

    return jsonify(all_measurements)


@app.route("/api/v1.0/stations")
def stations():
    session = Session(engine)
    
    results = session.query(Station.name, Station.station).all()
    
    session.close()

    return jsonify(results)


@app.route("/api/v1.0/tobs")
def tobs():
    session = Session(engine)

    data = session.query(Measurement.date, Measurement.tobs).all()

    session.close()
    
    all_temps = []
    for date, tobs in data:
        temps_dict = {}
        temps_dict['date'] = date
        temps_dict['tobs'] = tobs
        all_temps.append(temps_dict)

    return jsonify(all_temps)


@app.route("/api/v1.0/<start>")
def start(start):
    session = Session(engine)

    start_date = dt.datetime.strptime(start,'%Y-%m-%d')
    results = session.query(func.min(Measurement.tobs).label("min temp"),
    func.avg(Measurement.tobs).label("mean temp"),func.max(Measurement.tobs).label("max temp"))\
        .filter(Measurement.date>=start_date).all()

    return jsonify(results)


@app.route("/api/v1.0/<start>/<end>")
def start_end(start,end):
    session = Session(engine)
    start_date = dt.datetime.strptime(start,'%Y-%m-%d')
    end_date = dt.datetime.strptime(end,'%Y-%m-%d')
    
    lastdate = session.query(Measurement.date).order_by(Measurement.date.desc()).first()
    lastdate = dt.datetime.strptime(str(lastdate[0]), '%Y-%m-%d')

    if end_date > lastdate:  
        return('Out of Range')

    else:
        results = session.query(func.min(Measurement.tobs),func.avg(Measurement.tobs),func.max(Measurement.tobs))\
        .filter(Measurement.date.between(start_date, end_date)).all()
        
        return(jsonify(results))
    

if __name__ == '__main__':
    app.run(debug=True)