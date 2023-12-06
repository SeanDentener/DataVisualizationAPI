from flask import Flask, request, jsonify
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import csv
import json
from flask_cors import CORS

 
# constants
HOST = 'datavisualizationapi.azurewebsites.net'
PORT = 80

# initialize flask application
app = Flask(__name__)

# cors = CORS(app, resources={r"/api/getsrdata": {"origins": "http://localhost:4200"}, r"/api/getgeojsondata": {"origins": "http://localhost:4200"}})
cors = CORS(app, resources={r"/api/*": {"origins": "*"} })

@app.route('/api/getsrdata', methods=['GET'])
# @cross_origin(origin='localhost',headers=['Content- Type','Authorization'])
def GetSRData():
    df = pd.read_csv('Data/sr_hex_filtered.csv')

    df = df.drop(columns='notification_number')
    df = df.drop(columns='reference_number')
    df = df.drop(columns='directorate')
    df = df.drop(columns='department')
    # df.to_csv('Data/sr_hex_filtered.csv')

    #Group by and sum
    df = df.groupby('official_suburb').count()

    data = df.to_json()
    # data = convert_csv_json('Data/sr_hex.csv')
    
    
    return data



@app.route('/api/getsuburbcountdata', methods=['GET'])
def getsuburbcountdata():  
    df = getCSVData()
    #Group by and count
    df2 = df.groupby('official_suburb').agg(Count=('official_suburb','count')).reset_index().copy()
    data = df2.to_json(orient ='table')
    return data

@app.route('/api/getHexcountdata', methods=['GET'])
def getHexcountdata():  
    df = getCSVData()
    #Group by and count
    df2 = df.groupby('h3_level8_index').agg(Count=('h3_level8_index','count')).reset_index().copy()
    df2 = df2.sort_values('Count',ascending=False);
    data = df2.to_json(orient ='table')
    return data

@app.route('/api/getAlldata', methods=['GET'])
def getAlldata():  
    df = getBigCSVData()
    data = df.to_json(orient ='table')
    return data

# Commented out due to sr_hex.csv being to large for free public gihub repository with out large file support
# Kept here for further local development and use
# @app.route('/api/getDirectoratedata', methods=['GET'])
# def getDirectoratedata():  
#     df = getBigCSVData()
#     data = pd.DataFrame(df['directorate'].unique()).to_json(orient ='table')
#     return data

# Commented out due to sr_hex.csv being to large for free public gihub repository with out large file support
# Kept here for further local development and use
# @app.route('/api/getDepartmentdata', methods=['GET'])
# def getDepartmentdata():  
#     query = request.args.getlist('directorate')
#     print(query[0])
#     df = getBigCSVData()
#     df2 = df.query('directorate=="' + query[0] + '"').copy()
#     data = pd.DataFrame(df2.department.unique()).to_json(orient ='table')
#     return data

@app.route('/api/getgeojsondata', methods=['GET'])
def getgeoJsonData():
    with open('Data/city-hex-polygons-8.geojson') as f:
        js = json.load(f)
    return js


def convert_csv_json(csvFilePath):
     # create a dictionary
    data = {}
    # Open a csv reader called DictReader
    with open(csvFilePath, encoding='utf-8') as csvf:
        csvReader = csv.DictReader(csvf)
        # Convert each row into a dictionary 
        # and add it to data
        for rows in csvReader:
            # set primary key
            key = rows['notification_number']
            data[key] = rows
    return data

# Commented out due to sr_hex.csv being to large for free public gihub repository with out large file support
# Kept here for further local development and use
# def getBigCSVData():
#      # Get the csv
#     df = pd.read_csv('Data/sr_hex.csv')
#     df = df.drop(columns='notification_number')
#     df = df.drop(columns='reference_number')
#     return df

def getCSVData():
    # Get the filtered csv
    # It has been filtered based on h3_level8_index != "0"
    # It has been filtered based on directorate = "WATER AND SANITATION"
    # It has been filtered based on department = "Distribution Services"
    # This is to limit the data to infrastructure related service requests
    df = pd.read_csv('Data/sr_hex_filtered.csv')
    # Removed no longer needed columns
    df = df.drop(columns='notification_number')
    df = df.drop(columns='reference_number')
    # Removed no longer needed columns due to previous filtering
    df = df.drop(columns='directorate')
    df = df.drop(columns='department')
    return df

if __name__ == '__main__':
    # run web server
    app.run(host=HOST,
            debug=True,  # automatic reloading enabled
            port=PORT)