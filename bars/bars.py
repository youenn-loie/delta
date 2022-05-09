import dash
from dash import dcc
from dash import html
import plotly.express as px
import json
import seaborn as sns
from matplotlib import pyplot as plt
import plotly.graph_objects as go

from bars.get_data_bars import *


class Bars():

    def __init__(self, application=None):

        fig = go.Figure(data=[go.Scatter(x=[1, 2, 3], y=[4, 1, 2])])
        fig2 = go.Figure(data=[go.Scatter(x=[1, 2, 3], y=[6, 2, 7])])
        fig3 = go.Figure(data=[go.Scatter(x=[1, 2, 3], y=[8, 4, 9])])
        
        self.main_layout = html.Div(children=[
            html.H3(children='Répartition des bars en France'),
            html.Div([
                    html.Label(['Choose a graph:'],style={'font-weight': 'bold'}),
                    dcc.Graph(id='multi_chart', figure=fig),
                    dcc.RadioItems(
                          id='radio_items',
                          options=[{'label':'Valeur 1', 'value':'graph1'},
                                    {'label':'Valeur 2', 'value':'graph2'},
                                    {'label':'Valeur 3', 'value':'graph3'}],
                          value='graph1',
                          labelStyle={'display': 'block'},
                      )
                      ], style={'width': '15em', 'margin': "0px 0px 0px 40px"}),
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

        self.app.callback(dash.dependencies.Output('multi_chart', 'figure'),
                [dash.dependencies.Input('radio_items', 'value')])(self.update_graph)

    def update_graph(self, value):
            if value == 'graph1':
                fig1 = go.Figure(data=[go.Scatter(x=[1, 2, 3], y=[4, 1, 2])])
                return fig1
            elif value == 'graph2':
                fig2 = go.Figure(data=[go.Scatter(x=[1, 2, 3], y=[6, 2, 7])])
                return fig2
            else:
                fig3 = go.Figure(data=[go.Scatter(x=[1, 2, 3], y=[8, 4, 9])])
                return fig3
            


if __name__ == '__main__':
    bars = Bars()
    bars.app.run_server(debug=True, port=8051)
