{
 "cells": [
  {
   "cell_type": "code",
   "execution_count": null,
   "metadata": {},
   "outputs": [],
   "source": [
    "from flask import Flask, jsonify\n",
    "import sqlalchemy\n",
    "from sqlalchemy.ext.automap import automap_base\n",
    "from sqlalchemy.orm import Session\n",
    "from sqlalchemy import create_engine, func\n",
    "import numpy as np"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": null,
   "metadata": {},
   "outputs": [],
   "source": [
    "engine = create_engine(\"sqlite:///hawaii.sqlite\")\n",
    "# engine = create_engine(\"sqlite:///resources/hawaii.sqlite\")\n",
    "Base = automap_base()\n",
    "Base.prepare(engine, reflect=True)"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": null,
   "metadata": {},
   "outputs": [],
   "source": [
    "Measurement = Base.classes.measurement\n",
    "Station = Base.classes.station"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": null,
   "metadata": {},
   "outputs": [],
   "source": [
    "# Setup Flask\n",
    "app = Flask(__name__)\n",
    "\n",
    "@app.route(\"/\")\n",
    "def welcome():\n",
    "    return (\n",
    "        f\"Available Routes:<br/>\"\n",
    "        f\"/api/v1.0/precipitation<br/>\"\n",
    "        f\"/api/v1.0/stations<br/>\"\n",
    "        f\"/api/v1.0/tobs<br/>\"\n",
    "        f\"/api/v1.0/start<br/>\"\n",
    "        f\"/api/v1.0/start/end<br>\"\n",
    "    )"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": null,
   "metadata": {},
   "outputs": [],
   "source": [
    "# Convert the query results to a dictionary using `date` as the key and `prcp` as the value. \n",
    "# Return the JSON representation of your dictionary.\n",
    "@app.route(\"/api/v1.0/precipitation\")\n",
    "\n",
    "def precipitation():\n",
    "    session = Session(engine)\n",
    "\n",
    "    # Get data and precipitation scores\n",
    "    data = session.query(Measurement.date, Measurement.prcp).all()\n",
    "\n",
    "    session.close()\n",
    "    \n",
    "    all_measurements = []\n",
    "    for date, prcp in data:\n",
    "        measurement_dict = {}\n",
    "        measurement_dict['date'] = date\n",
    "        measurement_dict['prcp'] = prcp\n",
    "        all_measurements.append(measurement_dict)\n",
    "\n",
    "    return jsonify(all_measurements)"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": null,
   "metadata": {},
   "outputs": [],
   "source": [
    "# Return a JSON list of stations from the dataset.\n",
    "@app.route(\"/api/v1.0/stations\")\n",
    "def stations():\n",
    "    session = Session(engine)\n",
    "    \n",
    "    results = session.query(Station.name, Station.station).all()\n",
    "    \n",
    "    session.close()\n",
    "\n",
    "    return jsonify(results)"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": null,
   "metadata": {},
   "outputs": [],
   "source": [
    "# Query the dates and temperature observations of the most active station for the last year of data.\n",
    "# Return a JSON list of temperature observations (TOBS) for the previous year.\n",
    "@app.route(\"/api/v1.0/tobs\")   \n",
    "def tobs_page():\n",
    "    session = Session(engine) \n",
    "\n",
    "    last_date = session.query(temp_mea.date).order_by(temp_mea.date.desc()).first()\n",
    "    one_year_ago = str(int(last_date[0][:4]) - 1)\n",
    "    last_year_date = one_year_ago + last_date[0][4:]\n",
    "\n",
    "    last_year_tobs = session.query(temp_mea.date, temp_mea.tobs).\\\n",
    "        filter(temp_mea.date >= last_year_date).\\\n",
    "        filter(temp_mea.station == most_active_station).\\\n",
    "        order_by(temp_mea.date).all()\n",
    "\n",
    "    session.close()\n",
    "\n",
    "    station_tobs = [{\"Station\": most_active_station}]\n",
    "    for date, tobs in last_year_tobs:\n",
    "        tob_list = []\n",
    "        tob_list.append(date)\n",
    "        tob_list.append(tobs)\n",
    "        station_tobs.append(tob_list)\n",
    "\n",
    "    return jsonify(station_tobs)\n"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": null,
   "metadata": {},
   "outputs": [],
   "source": [
    "# Return a JSON list of the minimum temperature, the average temperature, and the max temperature for a given start or start-end range.\n",
    "# When given the start only, calculate `TMIN`, `TAVG`, and `TMAX` for all dates greater than and equal to the start date.\n",
    "# When given the start and the end date, calculate the `TMIN`, `TAVG`, and `TMAX` for dates between the start and end date inclusive.\n",
    "@app.route(\"/api/v1.0/<start>\")\n",
    "def start(start):\n",
    "    session = Session(engine)\n",
    "\n",
    "    start_date = dt.datetime.strptime(start,'%Y-%m-%d')\n",
    "    results = session.query(func.min(Measurement.tobs).label(\"min temp\"),\n",
    "    func.avg(Measurement.tobs).label(\"mean temp\"),func.max(Measurement.tobs).label(\"max temp\"))\\\n",
    "        .filter(Measurement.date>=start_date).all()\n",
    "\n",
    "    return jsonify(results)"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": null,
   "metadata": {},
   "outputs": [],
   "source": [
    "@app.route(\"/api/v1.0/<start>/<end>\")\n",
    "def start_end(start,end):\n",
    "    session = Session(engine)\n",
    "    start_date = dt.datetime.strptime(start,'%Y-%m-%d')\n",
    "    end_date = dt.datetime.strptime(end,'%Y-%m-%d')\n",
    "    \n",
    "    lastdate = session.query(Measurement.date).order_by(Measurement.date.desc()).first()\n",
    "    lastdate = dt.datetime.strptime(str(lastdate[0]), '%Y-%m-%d')\n",
    "\n",
    "    if end_date > lastdate:  \n",
    "        return('Out of Range')\n",
    "\n",
    "    else:\n",
    "        results = session.query(func.min(Measurement.tobs),func.avg(Measurement.tobs),func.max(Measurement.tobs))\\\n",
    "        .filter(Measurement.date.between(start_date, end_date)).all()\n",
    "        \n",
    "        return(jsonify(results))"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": null,
   "metadata": {},
   "outputs": [],
   "source": [
    "if __name__ == '__main__':\n",
    "    app.run(debug=True)"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": null,
   "metadata": {},
   "outputs": [],
   "source": []
  }
 ],
 "metadata": {
  "kernelspec": {
   "display_name": "Python 3",
   "language": "python",
   "name": "python3"
  },
  "language_info": {
   "codemirror_mode": {
    "name": "ipython",
    "version": 3
   },
   "file_extension": ".py",
   "mimetype": "text/x-python",
   "name": "python",
   "nbconvert_exporter": "python",
   "pygments_lexer": "ipython3",
   "version": "3.7.4"
  }
 },
 "nbformat": 4,
 "nbformat_minor": 4
}
