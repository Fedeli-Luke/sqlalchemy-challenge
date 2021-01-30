# Dependencies
from flask import Flask, jsonify
import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func
from datetime import datetime
import datetime as dt
 

# Set up database
engine = create_engine("sqlite:///Resources/hawaii.sqlite")
Base = automap_base()
Base.prepare(engine, reflect=True)



# Assign the classes to the matching tables
measurements = Base.classes.measurements
stations = Base.classes.stations

# Create app
app = Flask(__name__)

# Create the session
session = Session(engine)
 
@app.route("/")
def home():
    print("Home Page")
    """Listing of the available API routes"""
    return (
        f"Welcome to the Surf Up API<br>"
        f"Available Routes:<br>"
        f"/api/v1.0/precipitation<br>"
        f"/api/v1.0/stations<br>"
        f"/api/v1.0/tobs<br>"
        f"/api/v1.0/<start><br>"
        f"/api/v1.0<start>/<end><br>"
    )
  
@app.route("/api/v1.0/precipitation")
def precipitation():
   
    rain_results = session.query(Measurement.date, Measurement.prcp).filter(Measurement.date >= "08-23-2016").all()

    last_year_rain = list(np.ravel(rain_results))
    
    # Convert the query results from last year to a Dictionary using `date` as the key and `prcp` as the value 
    """"last_year_rain = []
    for result in results:
        prcp_dict = {}
        prcp_dict[Measurement.date] = prcp_dict[Measurement.prcp]
        last_year_rain.append(prcp_dict)"""

    # Return a json list of stations from the dataset.
    return jsonify(last_year_rain)

  
@app.route("/api/v1.0/stations")
def stations():
    
    # Return a json list of stations from the dataset.

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