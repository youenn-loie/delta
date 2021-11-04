import dash
from dash import dcc
from dash import html
from energies import energies
from population import population

# external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = dash.Dash(__name__,  title="Delta", suppress_callback_exceptions=True) # , external_stylesheets=external_stylesheets)
pop = population.WorldPopulationStats(app)
nrg = energies.Energies(app)

main_layout = html.Div([
    dcc.Location(id='url', refresh=False),
    html.Div(id='page_content'),
    dcc.Link(id='index_name', href='/'),
])

index_page = html.Div([
    dcc.Markdown("Choisissez la présention :"),
    dcc.Link('Energies', href='/energies'),
    html.Br(),
    dcc.Link('Population', href='/population'),
    html.Br(),
])

to_be_done_page = html.Div([
    dcc.Markdown("404 -- Désolé cette page n'est pas disponible."),
])

app.layout = main_layout

# "complete" layout (not sure that I need that)
app.validation_layout = html.Div([
    main_layout,
    index_page,
    to_be_done_page,
    pop.main_layout,
])

# Update the index
@app.callback([dash.dependencies.Output('page_content', 'children'),
               dash.dependencies.Output('index_name', 'children')],
              [dash.dependencies.Input('url', 'pathname')])
def display_page(pathname):
    if pathname == '/energies':
        return nrg.main_layout, 'Index'
    elif pathname == '/population':
        return pop.main_layout, 'Index'
    else:
        return index_page, ''


if __name__ == '__main__':
    app.run_server(debug=True)
