import sys
import dash
import flask
from dash import dcc
from dash import html
import pandas as pd
import numpy as np
import plotly.graph_objs as go
import plotly.express as px
import dateutil as du

mois = {'janv':1, 'févr':2, 'mars':3, 'avr':4, 'mai':5, 'juin':6, 'juil':7, 'août':8, 'sept':9, 'oct':10, 'nov':11, 'déc':12}

quoi = {"Prix d'une tonne de propane":[1000, 'Propane'], "Bouteille de butane de 13 kg":[13, 'Butane'],
       "100 litres de FOD au tarif C1":[100, 'Fioul'], "Un litre d'essence ordinaire":[1, 'Essence'],
       "Un litre de super carburant ARS":[1, 'Essence'], "Un litre de super sans plomb 95":[1, 'Essence'],
       "Un litre de super sans plomb 98":[1, 'Essence'], "Un litre de gazole":[1, 'Gazole'],
       "Un litre de GPLc":[1, 'GPL'], "1 kWh (contrat 3 kW)":[1, 'Electricité'], "1 kWh (contrat 9 kW)":[1, 'Electricité'],
       "Une tonne de granulés de bois en vrac":[1000*4.8, 'Electricité'], "100 kWh PCI de bois en vrac":[100, 'Electricité']}

densité =  {'Essence':0.75, 'Gazole':0.85, 'Fioul':0.85, 'GPL':0.55} # kg / l

# https://fr.wikipedia.org/wiki/Pouvoir_calorifique
calor = {'Essence':47.3, 'Gazole':44.8, 'Fioul':42.6, 'Propane':50.35, 'Butane':49.51, 'GPL':46, 'Bois':15, 'Charbon':20 ,
        'Electricité':3.6} # en MJ / kg sauf électicité en MJ / kWh

def conv_date(d):
    ma = d.split('-')                                      # coupe la chaine au - et ainsi ma[0] est le mois et ma[1] l'année
    return du.parser.parse(f"15-{mois[ma[0].lower()]}-{ma[1]}")  # parfois le mois a une majuscule d'où lower()

def make_dataframe_from_pegase(filename):
    df = pd.read_csv(filename, sep=";", encoding="latin1", skiprows=[0,1,3], header=None)
    df = df.set_index(0).T
    df['date'] = df['Période'].apply(conv_date)
    df = df.set_index('date')
    df.drop(columns=['Période'], inplace=True)
    df = df.replace('-', np.nan).astype('float64')
    return df

bois = make_dataframe_from_pegase("pegase_prix_bois_particulier.csv")
petrole = make_dataframe_from_pegase("pegase_prix_petrole_particulier.csv")

bois.drop(columns=['Une tonne de granulés de bois en sacs', '100 kWh PCI de bois en sacs'], inplace=True)
petrole.drop(columns=["Tarif d'une tonne de propane en citerne","100 kWh PCI de propane en citerne", "100 kWh PCS de propane",
                    "100 kWh PCI de propane", "100 kWh PCI de FOD au tarif C1"], inplace=True)  # doublons

electricite = pd.read_csv('prix_reglemente_electricite.csv', sep=';', decimal=',', parse_dates=['DATE_DEBUT'])
electricite = electricite.set_index(['P_SOUSCRITE',"DATE_DEBUT"])
electricite.drop(columns=['DATE_FIN', 'PART_FIXE_HT', 'PART_FIXE_TTC', 'PART_VARIABLE_HT'], inplace=True)
electricite.dropna(inplace=True)
electricite = electricite.unstack().T.reset_index(0, drop=True)
electricite = electricite.rename(columns={i:f"1 kWh (contrat {i:.0f} kW)" for i in electricite.columns})
duration = pd.DatetimeIndex(electricite.index.values)
new_index = pd.DatetimeIndex([f"{y}-{m:02d}-15" for y in range(duration[0].year, duration[-1].year+1) for m in range(1,13)])
electricite = electricite.reindex(np.concatenate([electricite.index.values , new_index.values]))
electricite.sort_index(inplace=True)
electricite = electricite.fillna(method='ffill')
electricite = electricite.loc[new_index]
electricite = electricite.reindex(bois.index)
electricite.drop(columns=["1 kWh (contrat 6 kW)", "1 kWh (contrat 12 kW)", "1 kWh (contrat 15 kW)"], inplace=True)

energie = pd.concat([petrole, bois, electricite])

years =np.arange(petrole.index.min().year, petrole.index.max().year+1)

app = dash.Dash()
app.layout = html.Div(children=[
    html.H3(children='Évolution des prix de différentes énergies'),
    html.Div([ dcc.Graph(id='main-graph'), ], style={'width':'100%', }),
    html.Div([
        html.Div([ html.Div('Prix'),
                   dcc.RadioItems(
                       id='price-type',
                       options=[{'label':'Absolu', 'value':0}, 
                                {'label':'Équivalent J','value':1},
                                {'label':'Relatif : 1 en ','value':2}],
                       value=0,
                       labelStyle={'display':'block'},
                   )
                 ], style={'width': '9em'} ),
        html.Div([ html.Div('Mois ref.'),
                   dcc.Dropdown(
                       id='which-month',
                       options=[{'label': i, 'value': mois[i]} for i in mois],
                       value=1,
                       disabled=True,
                   ),
                 ], style={'width': '6em', 'padding':'2em 0px 0px 0px'}), # bas D haut G
        html.Div([ html.Div('Annee ref.'),
                   dcc.Dropdown(
                       id='which-year',
                       options=[{'label': i, 'value': i} for i in years],
                       value=2000,
                       disabled=True,
                   ),
                 ], style={'width': '6em', 'padding':'2em 0px 0px 0px'} ),
        html.Div([ html.Div('Échelle en x'),
                   dcc.RadioItems(
                       id='xaxis-type',
                       options=[{'label': i, 'value': i} for i in ['Linéaire', 'Logarithmique']],
                       value='Logarithmique',
                       labelStyle={'display':'block'},
                   )
                 ], style={'width': '15em', 'margin':"0px 0px 0px 40px"} ), # bas D haut G
        ], style={
                    'padding': '10px 50px', 
                    'display':'flex',
                    'flexDirection':'row',
                    'justifyContent':'flex-start',
                }),
        html.P(),
        dcc.Markdown("""
        Le graphique est interactif. En passant la souris sur les courbes vous avez une infobulle. 
        En cliquant ou double-cliquant sur les lignes de la légende, vous choisissez les courbes à afficher.
        
        Notes :
           * Pour les prix relatifs, seules les énergies fossiles sont prises en compte par manque de données pour les autres.
           * Sources : 
              * [base Pégase](http://developpement-durable.bsocom.fr/Statistiques/) du ministère du développement durable
              * [tarifs réglementés de l'électricité](https://www.data.gouv.fr/en/datasets/historique-des-tarifs-reglementes-de-vente-delectricite-pour-les-consommateurs-residentiels/) sur data.gouv.fr
        """)
    ], style={
         'borderBottom': 'thin lightgrey solid',
         'backgroundColor': 'white',
          'padding': '10px 50px 10px 50px',
          }
)
    
@app.callback(
            dash.dependencies.Output('main-graph', 'figure'),
            [ dash.dependencies.Input('price-type', 'value'),
              dash.dependencies.Input('which-month', 'value'),
              dash.dependencies.Input('which-year', 'value'),
              dash.dependencies.Input('xaxis-type', 'value')])
def update_graph(price_type, month, year, xaxis_type):
    if price_type == 0 or month == None or year == None:
        df = energie
    elif price_type == 1:
        df = energie.copy()
        for c in df.columns:
            alias = quoi[c][1]
            try:
                df[c] = df[c] / (quoi[c][0] * densité[alias] * calor[alias])
            except:  # l'unité est déjà en kg et donc densité n'existe pas
                df[c] = df[c] / (quoi[c][0] * calor[alias])
    else:
        df = petrole.copy()
        df /= df.loc[f"{year}-{month}-15"]
    fig = px.line(df[df.columns[0]])
    for c in df.columns[1:]:
        fig.add_scatter(x = df.index, y=df[c], mode='lines', name=c, text=c)
    ytitle = ['Prix en €', 'Prix en € pour 1 MJ', 'Prix relative (sans unité)']
    fig.update_layout(
        #title = 'Évolution des prix de différentes énergies',
        yaxis = dict( title = ytitle[price_type],
                      type= 'linear' if xaxis_type == 'Linéaire' else 'log',),
        height=450,
        hovermode='closest',
    )
    return fig

@app.callback(
            [ dash.dependencies.Output('which-month', 'disabled'),
              dash.dependencies.Output('which-year', 'disabled')],
              dash.dependencies.Input('price-type', 'value') )
def disable_month_year(price_type):
    if price_type == 2:
        return False, False
    else:
        return True, True
    
if __name__ == '__main__':
    app.run_server(debug=True, port=8051)
