# Dependencies
from flask import Flask, jsonify
import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func

# Set up database
engine = create_engine("sqlite:///Resources/hawaii.sqlite")
Base = automap_base()
Base.prepare(engine, reflect=True)



# Assign the classes to the matching tables
measurement = Base.classes.measurement
station = Base.classes.station

# Create app
app = Flask(__name__)

# Create the session
session = Session(engine)

 
@app.route("/")
def home():
    print("Home Page")
    
    return (
        f"Welcome to my API<br>"
        f"Available Routes:<br>"
        f"/api/v1.0/precipitation<br>"
        f"/api/v1.0/stations<br>"
        f"/api/v1.0/tobs<br>"
        f"/api/v1.0/<start><br>"
        f"/api/v1.0<start>/<end><br>"
    )
  
@app.route("/api/v1.0/precipitation")
def precipitation():
   
    session = Session(engine)
    results = session.query(Measurement.date,Measurement.precipitation).all()
    session.close()
    precipitation_dict = dict(results)
    return jsonify(precipitation_dict)

  
@app.route("/api/v1.0/stations")
def stations():
    
    # Return a json list of stations from the dataset.
    session = Session(engine)
    stations_data = session.query(Station.station).all()

    return jsonify(stations_data)

  
@app.route("/api/v1.0/tobs")
def temperature():
    
    #Return a json list of Temperature Observations (tobs) for the previous year
    
    last_year_temps = []
    
    temp_data = session.query(Measurement.tobs).filter(Measurement.date >= "08-23-2016").all()

    last_year_temps = list(np.ravel(temp_data))

    return jsonify(last_year_temps)

  
@app.route("/api/v1.0/<start>")
def start_temp(start_date):
    
    # Return a JSON list of the minimum temperature, the average temperature, and the max temperature for a given start or start-end range.

    starting = []

    results_min = session.query(func.min(Measurement.tobs)).filter(Measurement.date == start_date).all()
    results_max = session.query(func.max(Measurement.tobs)).filter(Measurement.date == start_date).all()
    results_avg = session.query(func.avg(Measurement.tobs)).filter(Measurement.date == start_date).all()

    starting = list(np.ravel(results_min, results_max, results_avg))

    return jsonify(starting)

def greater_start_date(start_date):

    starting_date_temps = []

    results_min = session.query(func.min(Measurement.tobs)).filter(Measurement.date >= start_date).all()
    results_max = session.query(func.max(Measurement.tobs)).filter(Measurement.date >= start_date).all()
    results_avg = session.query(func.avg(Measurement.tobs)).filter(Measurement.date >= start_date).all()

    starting_date_temps = list(np.ravel(results_min,results_max, results_avg))

    return jsonify(starting_date_temps)

  
@app.route("/api/v1.0/<start>/<end>")

def start_end(start_date, end_date):

    start_end_temps = []

    results_min = session.query(func.min(Measurement.tobs)).filter(Measurement.date == start_date, Measurement.date == end_date).all()
    results_max = session.query(func.max(Measurement.tobs)).filter(Measurement.date == start_date, Measurement.date == end_date).all()
    results_avg = session.query(func.avg(Measurement.tobs)).filter(Measurement.date == start_date, Measurement.date == end_date).all()

    start_end_temps = list(np.ravel(results_min,results_max, results_avg))

    return jsonify(start_end_temps)

def start_end_trip(start_date, end_date):

    range_temps = []

    results_min = session.query(func.min(Measurement.tobs)).filter(Measurement.date >= start_date, Measurement.date >= end_date).all()
    results_max = session.query(func.max(Measurement.tobs)).filter(Measurement.date >= start_date, Measurement.date >= end_date).all()
    results_avg = session.query(func.avg(Measurement.tobs)).filter(Measurement.date >= start_date, Measurement.date >= end_date).all()

    range_temps = list(np.ravel(results_min,results_max, results_avg))

    return jsonify(range_temps)


if __name__ == '__main__':
    app.run(debug=True)