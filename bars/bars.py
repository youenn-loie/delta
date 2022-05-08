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
import plotly.express as px
import json

from bars.get_data_bars import *


class Bars():

    def __init__(self, application=None):
        data_bars = init_data_bars()
        # postalCodes = init_postal_code()
        data_revenus = init_data_revenus()
        code_commune = init_code_commune()
        barNumber = init_barNumber()
        departements = json.load(open('./bars/data/departements-version-simplifiee.geojson'))

        fig = px.choropleth_mapbox(barNumber, geojson=departements,
                                   locations='Département', featureidkey='properties.code',  # join keys
                                   color='Nombre de bars', color_continuous_scale=px.colors.sequential.turbid,
                                   mapbox_style="carto-positron",
                                   range_color=(0, 1000),
                                   zoom=4.5, center={"lat": 47, "lon": 2},
                                   opacity=0.75,
                                   labels={'prix': 'Nombre de bars'}
                                   )
        fig.update_layout(margin={"r": 0, "t": 0, "l": 0, "b": 0})
        fig2 = px.choropleth_mapbox(barNumber.sort_values(by='Nombre de bars'), geojson=departements,
                                   locations='Département', featureidkey='properties.code',  # join keys
                                   color='Nombre de bars', color_continuous_scale=px.colors.sequential.turbid,
                                   mapbox_style="carto-positron",
                                   range_color=(0, 1000),
                                   zoom=4.5, center={"lat": 47, "lon": 2},
                                   opacity=0.75,
                                   animation_frame='Nombre de bars',
                                   labels={'prix': 'Nombre de bars'}
                                   )
        fig2.update_layout(margin={"r": 0, "t": 0, "l": 0, "b": 0})

        fig3 = px.density_mapbox(data_bars, lat='Latitude', lon='Longitude', z='Département', radius=4.3,
                                   color_continuous_scale=px.colors.sequential.Plasma,
                                   zoom=4.5, center={"lat": 47, "lon": 2},
                                   mapbox_style="stamen-terrain", )

        fig3.update_layout(mapbox_style="carto-darkmatter")
        fig3.update_layout(margin=dict(b=0, t=0, l=0, r=0))

        fig4 = px.density_mapbox(data_bars, lat='Latitude', lon='Longitude', z='Département', radius=4.3,
                                   animation_frame='Département',
                                   zoom=4.5, center={"lat": 47, "lon": 2},
                                   mapbox_style="stamen-terrain", )

        fig4.update_layout(mapbox_style="carto-darkmatter")
        fig4.update_layout(margin=dict(b=0, t=0, l=0, r=0))

        # data_revenus.insert(1, "Code commune",
        #                     data_revenus['Dép.'].str.strip().apply(lambda dep: dep[:2]) + data_revenus['Commune'])
        # data_revenus.drop(["Dép.", "Commune"], axis=1, inplace=True)
        # data_revenus['Code commune'] = data_revenus['Code commune'].str.strip()

        self.main_layout = html.Div(children=[
            html.H3(children='Répartition des bars en France'),
            html.Div(
                [dcc.Graph(id='sond_t2', figure=fig)], style={'width': '100%', }),
            html.Br(),
            html.Div(
                [dcc.Graph(id='sond_t2', figure=fig2)], style={'width': '100%', }),
             html.Br(),
            html.Div(
                [dcc.Graph(id='sond_t2', figure=fig3)], style={'width': '100%', }),
             html.Br(),
            html.Div(
                [dcc.Graph(id='sond_t2', figure=fig4)], style={'width': '100%', }),
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
