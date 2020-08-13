import numpy as np
import pandas as pd
import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func
from datetime import datetime
from dateutil.relativedelta import relativedelta
from flask import Flask, jsonify


#################################################
# Database Setup
#################################################
engine = create_engine("sqlite:///Resources/hawaii.sqlite")

# reflect an existing database into a new model
Base = automap_base()
# reflect the tables
Base.prepare(engine, reflect=True)

# Save reference to the tables
measurement = Base.classes.measurement
Station = Base.classes.station

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
        f"Available Routes:<br/>"
        f"/api/v1.0/precipitation<br/>"
        f"/api/v1.0/stations<br/>"
        f"/api/v1.0/tobs<br/>"
        f"/api/v1.0/start_date<br/>"
        f"/api/v1.0/start_date/end_date<br/>"
        f"Please enter the date in format: Year-Month-Date"
    )


@app.route("/api/v1.0/precipitation")
def prcp_values():
    # Create our session (link) from Python to the DB
    session = Session(engine)

    # Query date and prcp values
    results = session.query(measurement.date, measurement.prcp).all()

    session.close()

    prcp_data = []
    for date, prcp in results:
        prcp_dict = {}
        prcp_dict[date] = prcp
        prcp_data.append(prcp_dict)

    return jsonify(prcp_data)


@app.route("/api/v1.0/stations")
def Station_names():
    # Create our session (link) from Python to the DB
    session = Session(engine)

    # Query station names.
    results = session.query(Station.name).all()

    session.close()

    # Convert list of tuples into normal list
    all_names = list(np.ravel(results))

    return jsonify(all_names)


@app.route("/api/v1.0/tobs")
def tobs_values():
    # Create our session (link) from Python to the DB
    session = Session(engine)

    # Calculating the Date of one year back.
    latest_date_from_db = str(session.query(measurement.date).order_by(
        measurement.date.desc()).first()).strip('(),\'')
    # print(latest_date_from_db)
    latest_date_from_db = datetime.strptime(latest_date_from_db, '%Y-%m-%d')
    # print(date_dt3)
    one_year_ago_date = latest_date_from_db - relativedelta(months=12)

    # Calculating the most active station.
    active_stations = pd.read_sql_query(session.query(Station.name, measurement.station, func.count(measurement.tobs)).
                                        filter(measurement.station == Station.station).
                                        group_by(measurement.station).
                                        order_by(func.count(measurement.prcp).desc()).statement, session.bind)
    most_active_station = active_stations.iloc[active_stations['count_1'].idxmax(
    ), 1]
    print(most_active_station)

    # Temp obs for last year of the most active station.
    result = session.query(measurement.tobs).\
        filter(measurement.station == most_active_station).filter(
            measurement.date > one_year_ago_date).all()

    session.close()

    all_temp = list(np.ravel(result))

    return jsonify(all_temp)


@app.route("/api/v1.0/<start_date>/<end_date>")
@app.route("/api/v1.0/<start_date>")
def date_values(start_date, end_date=0):
    # Create our session (link) from Python to the DB
    session = Session(engine)

    # Query temp values
    if (end_date == 0):
        results = session.query(func.min(measurement.tobs), func.avg(measurement.tobs), func.max(measurement.tobs)).\
            filter(measurement.date >= start_date).all()
    else:
        results = session.query(func.min(measurement.tobs), func.avg(measurement.tobs), func.max(measurement.tobs)).\
            filter(measurement.date >= start_date).filter(
            measurement.date <= end_date).all()

    session.close()

    temp_data = []
    for minimum, average, maximum in results:
        temp_dict = {}
        temp_dict['miminum'] = minimum
        temp_dict['average'] = average
        temp_dict['maximum'] = maximum
        temp_data.append(temp_dict)

    return jsonify(temp_data)


if __name__ == '__main__':
    app.run(debug=True)
