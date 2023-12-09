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

cors = CORS(app, resources={r"/api/*": {"origins": "*"} })

@app.route('/api/getsrdata', methods=['GET'])
def GetSRData():
    df = pd.read_csv('Data/sr_hex_filtered.csv')

    df = df.drop(columns='notification_number')
    df = df.drop(columns='reference_number')
    df = df.drop(columns='directorate')
    df = df.drop(columns='department')
    # df.to_csv('Data/sr_hex_filtered.csv')

    #Group by and count
    df = df.groupby('official_suburb').count()
    data = df.to_json()
  
    
    return data



@app.route('/api/getsuburbcountdata', methods=['GET'])
def getsuburbcountdata():  
    df = getCSVData()
    #Group by and count
    df2 = df.groupby(['official_suburb']).agg(Count=('official_suburb','count')).reset_index().copy()
    df2 = df2.sort_values('Count',ascending=False);
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


def getCSVData():
    # Get the filtered csv
    # It has been filtered based on h3_level8_index != "0"
    # It has been filtered based on directorate = "WATER AND SANITATION"
    # It has been filtered based on department = "Distribution Services"
    # The filtered csv file was produced using the Jupyter notebook ProcessData.ipynb
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