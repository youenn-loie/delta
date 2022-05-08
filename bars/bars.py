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

from bars.get_data_bars import *


class Bars():

    def __init__(self, application = None):
        data_bars = pd.read_csv('./bars/data/osm-fr-bars.csv', sep=';')
        #postalCodes = init_postal_code()
        data_revenus = init_data_revenus()
        code_commune = init_code_commune()

        self.main_layout = html.Div(children=[
            html.H3(children='Répartition des bars en France'),
            html.Div([ dcc.Graph(id='mpj-main-graph'), ], style={'width':'100%', }),
            html.Br(),
            dcc.Markdown("""
            Le graphique est interactif. En passant la souris sur les courbes vous avez une infobulle. 
            
            Notes :
               * La grippe de l'hiver 1989-1990 a fait 20 000 morts (4,6 millions de malades en 11 semaines). La chute de la courbe au premier janvier 1990 est quand même très surprenante.
               """)
        ], style={
            'backgroundColor': 'white',
             'padding': '10px 50px 10px 50px',
             }
        )

        if application:
            self.app = application
        else:
            self.app = dash.Dash(__name__)
            self.app.layout = self.main_layout

        


if __name__ == '__main__':
    bars = Bars()
    bars.app.run_server(debug=True, port=8051)