import zipfile
from IPython.display import display
from matplotlib.pyplot import bar
import numpy as np
import pandas as pd
import folium
import plotly.express as px
import seaborn as sns
import sys
import dash
import flask
from dash import dcc
from dash import html
import plotly.graph_objs as go
import plotly.express as px
import dateutil as du



def init_postal_code():
    postalCodes = pd.read_csv('https://bano.openstreetmap.fr/data/full.csv.gz', compression='gzip', usecols=['01400', '46.147624', '4.923727'], dtype={'01400': str, '46.147624': np.float64, '4.923727': np.float64})
    postalCodes.columns = ['Postal code', 'Latitude', 'Longitude']
    postalCodes['Latitude'] = postalCodes['Latitude'].apply(lambda lat: round(lat, 3))
    postalCodes['Longitude'] = postalCodes['Longitude'].apply(lambda long: round(long, 3))
    return postalCodes

def init_data_bars():
    data_bars = pd.read_csv('./bars/data/osm-fr-bars.csv', sep=';')
    data_bars = data_bars[["Geo Point", "Code postal", "Nom"]]
    data_bars.drop("Code postal", axis=1, inplace=True)

    latitudes = []
    longitudes = []
    for row in data_bars['Geo Point']:
        try:
            latitudes.append(row.split(',')[0])
            longitudes.append(row.split(',')[1])
        except:
            latitudes.append(np.NaN)
            longitudes.append(np.NaN)

    data_bars['Latitude'] = latitudes
    data_bars['Longitude'] = longitudes
    data_bars.drop('Geo Point', 1)

    data_bars.isnull().sum().sum()

    data_bars['Latitude'] = data_bars['Latitude'].astype(float)
    data_bars['Longitude'] = data_bars['Longitude'].astype(float)
    data_bars['Latitude'] = data_bars['Latitude'].apply(lambda lat: round(lat, 3))
    data_bars['Longitude'] = data_bars['Longitude'].apply(lambda long: round(long, 3))
    return data_bars

# is there a reason to avoid os.system(f'tar -xvzf {filename}') and instead use zipfile (e.g. zip = ZipFile('file.zip'); zip.extractall() )

#zip = ZipFile('file.zip')
#zip.extractall()