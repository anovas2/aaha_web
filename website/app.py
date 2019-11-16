import os
# import sys
import sqlite3
import pandas as pd
import numpy as np
import censusgeocode as cg
import time

import queries
# import geojson

from flask import Flask, jsonify, render_template, url_for
from geopy.geocoders import Nominatim

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
census_dataset = queries.get_df(connection, 'census_dataset')

geolocator = Nominatim()




# census_dataset = queries.get_df(connection, 'census_dataset')
# censustract = queries.get_df(connection, 'censustract')
# hud_dataset = queries.get_df(connection, 'hud_dataset')
# nhpd_dataset = queries.get_df(connection, 'nhpd_dataset')

# geojson.geojson_convert(census_income_to_rent_dataset)

@app.route("/")
def index():
    """Return the homepage."""
    return render_template("index.html")


@app.route("/census_income_to_rent_dataset/incomes")
def incomes():
    """Return a list of sample names."""

    # Use Pandas to perform the sql query
    incomes = census_income_to_rent_dataset['Income'].drop_duplicates()

    # Return a list of the column names (sample names)
    # return jsonify(list(df.columns)[2:])
    return jsonify(list(incomes))


@app.route("/census_income_to_rent_dataset/burdens")
def burdens():
    """Return a list of sample names."""

    # Use Pandas to perform the sql query
    burdens = census_income_to_rent_dataset['Rent as % of Income'].drop_duplicates()

    # Return a list of the column names (sample names)
    # return jsonify(list(df.columns)[2:])
    return jsonify(list(burdens))


@app.route("/census_income_to_rent_dataset/years")
def years():
    """Return a list of sample names."""

    # Use Pandas to perform the sql query
    years = census_income_to_rent_dataset['YEAR'].drop_duplicates()

    # Return a list of the column names (sample names)
    # return jsonify(list(df.columns)[2:])
    return jsonify(list(years))


@app.route("/address_data/<address>")
def lat_lon(address):
    """Return a list of sample names."""

    # Use Pandas to perform the sql query

    location = geolocator.geocode(address)


    # Return a list of the column names (sample names)
    # return jsonify(list(df.columns)[2:])
    # address_data = location.raw
    lat = location.latitude
    lon = location.longitude
    # frm = fmr()
    fmr = 1500
    geoid = geo_id(lat,lon)
    try:
        af_rent = af_rent_f(geoid)*.30/12
    except:
        af_rent = 1000
    burden_data_html = burden_data_f(geoid)
    address_data = {
        "lat": lat,
        "lon": lon,
        "geoid": geoid,
        "fmr" : fmr,
        "af_rent": af_rent,
        "address" : location.address,
        "burden_data_html": burden_data_html,

    }
    return jsonify(address_data)


# @app.route("/burden_data/<address>")
def burden_data_f(GEOID):
    """Return a list of sample names."""

    # Use Pandas to perform the sql query
    burden_data = census_income_to_rent_dataset[(census_income_to_rent_dataset['GEOID']==int(GEOID)) & (census_income_to_rent_dataset['YEAR']==2017)].drop(columns=['GEOID','YEAR'])
    # burden_data.to_clipboard(excel=True)
    # burden_data = burden_data.groupby(['HHs']).mean().T
    burden_data = burden_data.pivot(columns='Rent as % of Income', values='HHs', index='Income')
    total_hhs = burden_data.to_numpy().sum()
    burden_data = burden_data.div(total_hhs)*100
    burden_data = burden_data.astype(int).astype(str) + '%'
    burden_data = burden_data.reindex(["Low Income", "Med Income", "High Income"])
    burden_data = burden_data[['Low Burden', 'Med Burden', 'High Burden']]
    burden_data_html = burden_data.to_html()

    # burden_data = pd.pivot_table(burden_data, index=['Rent as % of Income'], values=burden_data.HHs, aggfunc='mean')

    # burden_data = pd.crosstab(burden_data['Rent as % of Income'],burden_data['Income'],values=burden_data.HHs, aggfunc='mean').apply(lambda r: r/r.sum(), axis=1)
    # burden_data = pd.crosstab(burden_data['Rent as % of Income'], burden_data['Income'])

    # burden_data = pd.pivot_table(burden_data, values='HHs', index=['GEOID', 'YEAR'], columns=['Income','Rent as % of Income'], aggfunc=np.sum)

    # Return a list of the column names (sample names)
    # return jsonify(list(df.columns)[2:])
    # address_data = location.raw
    # lat = location.latitude
    # lon = location.longitude
    # # frm = fmr()
    # fmr = 1500
    # geoid = geo_id(lat,lon)
    # address_data = {
    #     "lat": lat,
    #     "lon": lon,
    #     "geoid": geoid,
    #     "fmr" : fmr,
    #     "address" : location.address,
    # }
    return burden_data_html


def af_rent_f(GEOID):
    af_rent = census_dataset[census_dataset['GEOID']==int(GEOID)]['MedianIncomeHH']
    return int(af_rent)


def geo_id(lat, lon, retries=0):
    if retries > 10: return
    try:
        geoid = cg.coordinates(x=lon, y=lat)['Census Tracts'][0]['GEOID']
        if not geoid:
            raise ValueError('A very specific bad thing happened.')
        return geoid
    except:
        retries += 1
        time.sleep(retries)
        geoid = geo_id(lat, lon, retries)
        return geoid




# @app.route("/metadata/<sample>")
# def sample_metadata(sample):
#     """Return the MetaData for a given sample."""
#     sel = [
#         Samples_Metadata.sample,
#         Samples_Metadata.ETHNICITY,
#         Samples_Metadata.GENDER,
#         Samples_Metadata.AGE,
#         Samples_Metadata.LOCATION,
#         Samples_Metadata.BBTYPE,
#         Samples_Metadata.WFREQ,
#     ]
#
#     results = db.session.query(*sel).filter(Samples_Metadata.sample == sample).all()
#
#     # Create a dictionary entry for each row of metadata information
#     sample_metadata = {}
#     for result in results:
#         sample_metadata["sample"] = result[0]
#         sample_metadata["ETHNICITY"] = result[1]
#         sample_metadata["GENDER"] = result[2]
#         sample_metadata["AGE"] = result[3]
#         sample_metadata["LOCATION"] = result[4]
#         sample_metadata["BBTYPE"] = result[5]
#         sample_metadata["WFREQ"] = result[6]
#
#     print(sample_metadata)
#     return jsonify(sample_metadata)


@app.route("/census_income_to_rent_dataset/<year>/<GEOID>")
def samples(year, GEOID):
    """Return `otu_ids`, `otu_labels`,and `sample_values`."""
    # stmt = db.session.query(Samples).statement
    # df = pd.read_sql_query(stmt, db.session.bind)

    # Filter the data based on the sample number and
    # only keep rows with values above 1
    test = census_income_to_rent_dataset
    sample_data = census_income_to_rent_dataset[(census_income_to_rent_dataset['YEAR'] == year) & (census_income_to_rent_dataset['GEOID'] == GEOID)]

    # sample_data = df.loc[df[sample] > 1, ["otu_id", "otu_label", sample]]

    # Sort by sample
    # sample_data.sort_values(by=sample, ascending=False, inplace=True)

    # Format the data to send as json
    # data = {
    #     "otu_ids": sample_data.otu_id.values.tolist(),
    #     "sample_values": sample_data[sample].values.tolist(),
    #     "otu_labels": sample_data.otu_label.tolist(),
    # }
    html = sample_data.to_html(table_id='maptable')

    return html


@app.route('/story1/')
def story1():
    return render_template('story1.html')


@app.route('/story2/')
def story2():
    return render_template('story2.html')


@app.route('/story3/')
def story3():
    return render_template('story3.html')


@app.route('/map/')
def story4():
    return render_template('story4.html')


@app.route('/tool/')
def tool():
    return render_template('tool.html')


@app.route('/data/')
def data():
    return render_template('data.html')

@app.route('/team/')
def team():
    return render_template('team.html')

# @app.route('/map/')
# def map():
#     return render_template('index_map.html')



if __name__ == "__main__":
    app.run()
