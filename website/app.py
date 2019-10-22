import os
# import sys
import sqlite3
import pandas as pd
import numpy as np

import queries
# import geojson

from flask import Flask, jsonify, render_template, url_for
# from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

# PATH = os.path.abspath(os.path.dirname(sys.argv[0]))
# DB_PATH = os.path.join(PATH, r'aaha.db')




#################################################
# Database Setup
#################################################


connection = queries.create_connection()
cursor = connection.cursor()

# app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///db/aaha.db"
# db = SQLAlchemy(app)
#
# # reflect an existing database into a new model
# Base = automap_base()
# # reflect the tables
# Base.prepare(db.engine, reflect=True)
#
# # Save references to each table
# # census_dataset = Base.classes.census_dataset
# Census_income_to_rent_dataset = Base.classes.census_income_to_rent_dataset
# censustract = Base.classes.censustract
# hud_dataset = Base.classes.hud_dataset
# nhpd_dataset = Base.classes.nhpd_dataset
#
#
#

census_income_to_rent_dataset = queries.get_df(connection, 'census_income_to_rent_dataset')
# census_dataset = queries.get_df(connection, 'census_dataset')
# censustract = queries.get_df(connection, 'censustract')
# hud_dataset = queries.get_df(connection, 'hud_dataset')
# nhpd_dataset = queries.get_df(connection, 'nhpd_dataset')

# geojson.geojson_convert(census_income_to_rent_dataset)

@app.route("/")
def index():
    """Return the homepage."""
    return render_template("index.html")


@app.route("/census_income_to_rent_dataset/income_brackets")
def incomes():
    """Return a list of sample names."""

    # Use Pandas to perform the sql query
    incomes = census_income_to_rent_dataset['Income'].drop_duplicates()

    # Return a list of the column names (sample names)
    # return jsonify(list(df.columns)[2:])
    return jsonify(list(incomes))


@app.route("/census_income_to_rent_dataset/years")
def years():
    """Return a list of sample names."""

    # Use Pandas to perform the sql query
    years = census_income_to_rent_dataset['YEAR'].drop_duplicates()

    # Return a list of the column names (sample names)
    # return jsonify(list(df.columns)[2:])
    return jsonify(list(years))



@app.route("/metadata/<sample>")
def sample_metadata(sample):
    """Return the MetaData for a given sample."""
    sel = [
        Samples_Metadata.sample,
        Samples_Metadata.ETHNICITY,
        Samples_Metadata.GENDER,
        Samples_Metadata.AGE,
        Samples_Metadata.LOCATION,
        Samples_Metadata.BBTYPE,
        Samples_Metadata.WFREQ,
    ]

    results = db.session.query(*sel).filter(Samples_Metadata.sample == sample).all()

    # Create a dictionary entry for each row of metadata information
    sample_metadata = {}
    for result in results:
        sample_metadata["sample"] = result[0]
        sample_metadata["ETHNICITY"] = result[1]
        sample_metadata["GENDER"] = result[2]
        sample_metadata["AGE"] = result[3]
        sample_metadata["LOCATION"] = result[4]
        sample_metadata["BBTYPE"] = result[5]
        sample_metadata["WFREQ"] = result[6]

    print(sample_metadata)
    return jsonify(sample_metadata)


@app.route("/census_income_to_rent_dataset/<sample>")
def samples(sample):
    """Return `otu_ids`, `otu_labels`,and `sample_values`."""
    stmt = db.session.query(Samples).statement
    df = pd.read_sql_query(stmt, db.session.bind)

    # Filter the data based on the sample number and
    # only keep rows with values above 1
    sample_data = df.loc[df[sample] > 1, ["otu_id", "otu_label", sample]]

    # Sort by sample
    sample_data.sort_values(by=sample, ascending=False, inplace=True)

    # Format the data to send as json
    data = {
        "otu_ids": sample_data.otu_id.values.tolist(),
        "sample_values": sample_data[sample].values.tolist(),
        "otu_labels": sample_data.otu_label.tolist(),
    }
    return jsonify(data)


@app.route('/story1.html')
def story1():
    return render_template('story1.html')


if __name__ == "__main__":
    app.run()
