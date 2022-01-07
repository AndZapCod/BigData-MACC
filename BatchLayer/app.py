import pandas as pd

from  pyhive  import  hive

# CONNECTION

host_name = "localhost"
port = 10000   #default  is  10000
user = "ubuntu" # username  in  postgres
password = "" # password  in  postgres  - leave  empty  when usingNOSASL
database="default"

conn = hive.Connection(host=host_name, port=port,
username=user, database=database, auth='NOSASL')

# Get data

pos_neg_view = pd.read_sql('SELECT * FROM pos_neg_view', conn)
time_view = pd.read_sql('SELECT * FROM time_view', conn)
concurrency_view = pd.read_sql('SELECT * FROM concurrency_view', conn)

pos_neg_view.columns = ['Sentiment', 'Count']
time_view.columns = ['Month', 'Sentiment', 'Count']
concurrency_view.columns = ['Month', 'Day', 'Count']

concurrency_view['date'] = list(map(lambda x: str(x[0]) + '-' + str(x[1]) + '-2009', concurrency_view[['Month', 'Day']].values))
concurrency_view['date'] = pd.to_datetime(concurrency_view['date'])

# APPLICATION

import dash
import dash_core_components as dcc
import dash_html_components as html
import plotly.express as px

from dash.dependencies import Input, Output

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']
app = dash.Dash(__name__, external_stylesheets=external_stylesheets)
server = app.server

# figures

pie = px.pie(pos_neg_view, values='Count', names='Sentiment')

bar = px.bar(time_view, x='Month', y='Count', color='Sentiment')

line = px.area(concurrency_view, x='date', y='Count')


app.layout = html.Div(children=[

    html.H1(children='ANALISIS DE SENTIMIENTOS EN TWITTER'),
    html.H5(children='''El dataset consta de mas de un millon de Tweets capturados en el año 2009 los cuales han sido clasificados
    segun la catagoria de sentimientos expresados en el mismo positivos (0) y negativos (4)'''),
    html.H6(children='''
        Como primer paso vamos a ver como de balanceado esta este dataset
    '''),
    dcc.Graph(
        id='example-graph',
        figure=pie
    ),
	html.H6(children='''
        En el siguiente grafico se puede observer la frecuencia mensual de publicacion y su proporción en terminos de sentimiento, en los meses de Abril, Mayo y Junio
    '''),
    dcc.Graph(
        id='example-graph2',
        figure=bar
    ),
    html.H6(children='''
        Por ultimo tenemos la distrubución del numeró de publicaciones a lo largo del tiempo durante los tres meses en los que se hizo captura de Tweets.
    '''),
    dcc.Graph(
        id='example-graph3',
        figure=line
    )
])

if __name__ == '__main__':
    app.run_server(debug=True)