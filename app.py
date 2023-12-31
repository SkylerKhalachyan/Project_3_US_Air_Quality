# Flask app goes here
import numpy as np
import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func, text

from flask import Flask, jsonify, render_template
import psycopg2
from pathlib import Path
# Use hidden file to import postgres db pwd
from config import postgres_key, db_name
#################################################
# Database Setup
#################################################
engine = create_engine(f"postgresql+psycopg2://postgres:{postgres_key}@localhost/{db_name}")

#################################################
# Flask Setup
#################################################
app = Flask(__name__)


#################################################
# Flask Routes
#################################################

@app.route("/")
def welcome():
    return render_template("index.html")
# Connecting to index.html static file

@app.route("/api/v1.0/aqi/100")
def aqi_test():
    # Create our session (link) from Python to the DB
    conn = engine.connect()
    # Connected to engine
    # Reading in the aqi data from database
    aqi_data = conn.execute(text('SELECT * FROM aqi LIMIT 100'))
    output_data = [{"CBSA Code" : row[0],
	                "Date" : row[1],
	                "AQI"  : row[2],
	                "Category" : row[3],
	                "Defining Parameter" : row[4],
	                "Number of Sites Reporting" : row[5],
	                "city_ascii" : row[6],
	                "state_id" : row[7],
	                "state_name" : row[8],
	                "lat" : row[9],
	                "lng" : row[10],
	                "population" : row[11],
	                "density" : row[12],
	                "timezone" : row[13]} for row in aqi_data]
    # Closing connection
    conn.close()
    # Returning data from database as json
    #return jsonify(dict.to_json())
    return jsonify(output_data)

@app.route("/api/v1.0/aqi/month/<i>")
def month(i):
    # Create our session (link) from Python to the DB
    """Return a list of all aqi data between a start and end date"""
    conn = engine.connect()
    # Connected to engine
    # Reading in the aqi data from database
    aqi_data = conn.execute(text(f"SELECT * FROM aqi WHERE \"Date\" LIKE '{i}/%'"))
    output_data = [{"CBSA Code" : row[0],
	                "Date" : row[1],
	                "AQI"  : row[2],
	                "Category" : row[3],
	                "Defining Parameter" : row[4],
	                "Number of Sites Reporting" : row[5],
	                "city_ascii" : row[6],
	                "state_id" : row[7],
	                "state_name" : row[8],
	                "lat" : row[9],
	                "lng" : row[10],
	                "population" : row[11],
	                "density" : row[12],
	                "timezone" : row[13]} for row in aqi_data]
    # Closing connection
    conn.close()
    # Returning data from database as json
    return jsonify(output_data)

@app.route("/api/v1.0/aqi/state/<i>")
def state(i):
    # Create our session (link) from Python to the DB
    """Return a list of all aqi data between a start and end date"""
    conn = engine.connect()
    # Connected to engine
    # Reading in the aqi data from database
    aqi_data = conn.execute(text(f"SELECT * FROM aqi WHERE \"state_id\" = '{i.upper()}'"))
    output_data = [{"CBSA Code" : row[0],
	                "Date" : row[1],
	                "AQI"  : row[2],
	                "Category" : row[3],
	                "Defining Parameter" : row[4],
	                "Number of Sites Reporting" : row[5],
	                "city_ascii" : row[6],
	                "state_id" : row[7],
	                "state_name" : row[8],
	                "lat" : row[9],
	                "lng" : row[10],
	                "population" : row[11],
	                "density" : row[12],
	                "timezone" : row[13]} for row in aqi_data]
    # Closing connection
    conn.close()
    # Returning data from database as json
    #return jsonify(dict.to_json())
    return jsonify(output_data)

@app.route("/api/v1.0/aqi-avg/month/<i>")
def avg_aqi(i):
    # Create our session (link) from Python to the DB
    """Return a list of aqi state avg"""
    conn = engine.connect()
    # Connected to engine
    # Reading in the aqi data from database
    aqi_data = conn.execute(text(f"SELECT state_id, avg(\"AQI\") over(partition by state_id) as AVG_AQI from aqi WHERE \"Date\" LIKE '{i}/%'"))
    output_data = [{"state_id" : row[0],
	                "avg" : row[1]} for row in aqi_data]
    # Closing connection
    conn.close()
    # Returning data from database as json
    #return jsonify(dict.to_json())
    return jsonify(output_data)


# Completing flask setup
if __name__ == '__main__':
    app.run(debug=True)
