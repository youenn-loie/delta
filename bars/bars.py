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

class Bars():


    def __init__(self, application = None):
        data_bars = pd.read_csv('../../data/osm-fr-bars.csv', sep=';')
        #postalCodes = pd.read_csv('../../data/postal-code.csv', usecols=['01400', '46.147624', '4.923727'], dtype={'01400': str, '46.147624': np.float64, '4.923727': np.float64} )
        data_revenus = pd.read_excel('../../data/revenus_communes_2019.xlsx')  #header=3
        code_commune = pd.read_csv('../../data/code-commune.csv', sep=';')
        print("coucou")

        self.main_layout = html.Div(children=[
            html.H3(children='Nombre de décès par jour en France'),
            html.Div([ dcc.Graph(id='mpj-main-graph'), ], style={'width':'100%', }),
            html.Div([ dcc.RadioItems(id='mpj-mean', 
                                     options=[{'label':'Courbe seule', 'value':0},
                                              {'label':'Tendence générale', 'value':1}, 
                                              {'label':'Moyenne journalière (les décalages au 1er janv. indique la tendence)', 'value':2}], 
                                     value=0,
                                     labelStyle={'display':'block'}) ,
                                     ]),
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