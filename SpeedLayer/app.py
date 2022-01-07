import dash
import dash_core_components as dcc
import dash_html_components as html
import plotly.express as px
import pandas as pd

from dash.dependencies import Input, Output
from datetime import datetime
from datetime import timedelta
from cassandra.cluster import Cluster
from kafka import KafkaConsumer
from json import loads


external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

server = app.server

app.layout = html.Div(
    html.Div([
        html.H1('AVIATION STACK VISUALIZATION'),
        html.H5('Resumen trafico aereo en tiempo real'),
        html.H6("""En esta grafica se observa la cantidad de vuelos que hay en cada momento
        en cada uno de sus posibles estados, exceptuando los vuelos que hayan aterrizado,
        esto nos permite tener una idea del trafico aereo presente """),
        dcc.Graph(id='live-update-graph'),
        html.H5('Vuelos con incidentes recientemente'),
        html.H6(""" En este grafico se muestran la cantidad y e tipo de incidente que han 
        presentado algunos vuelos en la ultima media hora, discriminando por el aeropuerto de partida,
        el más comun de los incidentes es el cancelamiento de vuelos y un aeropuerto con gran número de
        vuelos cancelados puede dar cuenta de una zona con condiciones climaticas adversas, entre otras causas.
        Por lo que viajeros que piensan salir de viaje deberian evitar estos aeropuertos."""),
        dcc.Graph(id='update_graph_1'),
        html.H5('Aeropuertos con retrasos en salidas'),
        html.H6(""" En esta grafica podemos ver una linea de tiempo con el promedio de retrasos en los vuelos de un grupo de aeropuertos,
        lo que informa que es posible que el vuelo de algun viajero se vea retrasado en alguno de estos aeropuertos."""),
        dcc.Graph(id='update_graph_2'),
        html.H5('Aeropuertos con llegadas retrasadas'),
        html.H6(""" En esta grafica podemos ver una linea de tiempo con el promedio de retrasos en los vuelos entrantes de un grupo de aeropuertos,
        lo que informa que es posible que el vuelo de algun viajero presente demoras en el aterrizaje"""),
        dcc.Graph(id='update_graph_3'),
        dcc.Interval(
            id='live',
            interval=4*1000, # 4 secs
            n_intervals=0
        ),
        dcc.Interval(
            id='cassandra',
            interval=300*1000, # 5 mins
            n_intervals=1 
        )
    ])
)

consumer = KafkaConsumer(
    'flights_json',
    bootstrap_servers=['localhost:9092'],
    auto_offset_reset='earliest',
    enable_auto_commit=True,
    group_id='dash',
    value_deserializer=lambda x: loads(x.decode('utf-8'))
)

figths_status = {}

@app.callback(Output('live-update-graph', 'figure'),
              Input('live', 'n_intervals'))
def update_graph_live(n):

    msg = next(consumer)
    message = msg.value
    fligth_iata = message.get('flight').get('iata')
    fligth_icao = message.get('flight').get('icao')
    flight_status = message.get('flight_status')

    if flight_status == 'landed':
        figths_status.pop((fligth_iata,fligth_icao), None)
    elif flight_status == 'unknown':
        pass
    else:
        figths_status[(fligth_iata,fligth_icao)] = flight_status
    status = {'scheduled': 0, 'active': 0, 'cancelled': 0, 'incident': 0, 'diverted': 0}
    for k in figths_status.keys():
        status[figths_status[k]] += 1

    df = pd.DataFrame({'Status' : status.keys(), 'Count': status.values()})
    fig = px.bar(df, x='Status', y='Count')
    return fig

def pandas_factory(colnames, rows):
    return pd.DataFrame(rows,columns=colnames)

cluster = Cluster()
session = cluster.connect('flights_ks')
session.row_factory = pandas_factory

@app.callback(Output('update_graph_1', 'figure'),
              Input('cassandra', 'n_intervals'))
def update_graph_1(n):
    now = datetime.now()
    ten_min_ago = now - timedelta(minutes=30)
    ten_min_ago = int(datetime.timestamp(ten_min_ago))
    query = f"SELECT time_stamp, flight_status, departure FROM flights WHERE time_stamp >= {ten_min_ago}  ALLOW FILTERING;"
    
    departure = session.execute(query)._current_rows
    departure = departure.groupby(['departure', 'flight_status'], as_index=False).count()
    departure = departure.set_index('flight_status')
    drop_list = list(set([label for label in departure.index if label in ['scheduled', 'landed','active', 'unknown']]))
    departure = departure.drop(drop_list)
    departure = departure.reset_index()
    
    departure.columns = ['flight_status', 'departure', 'count']

    fig = px.bar(departure, x='departure', y='count', color='flight_status') 
    return fig

@app.callback(Output('update_graph_2', 'figure'),
              Input('cassandra', 'n_intervals'))
def update_graph_2(n):
    now = datetime.now()
    ten_min_ago = now - timedelta(minutes=30)
    ten_min_ago = int(datetime.timestamp(ten_min_ago))
    query = f"SELECT time_stamp, departure, dep_delay FROM flights WHERE time_stamp >= {ten_min_ago}  ALLOW FILTERING;"

    delay = session.execute(query)._current_rows
    delay = delay.groupby(['time_stamp', 'departure'], as_index=False).mean()
    delay['time_stamp'] = delay['time_stamp'].apply(datetime.fromtimestamp)
    delay = delay.set_index('dep_delay').drop([0])
    delay = delay.reset_index()

    fig = px.line(delay, x='time_stamp', y='dep_delay', color='departure') 
    return fig

@app.callback(Output('update_graph_3', 'figure'),
              Input('cassandra', 'n_intervals'))
def update_graph_3(n):
    now = datetime.now()
    ten_min_ago = now - timedelta(minutes=30)
    ten_min_ago = int(datetime.timestamp(ten_min_ago))
    query = f"SELECT time_stamp, arrival, arr_delay FROM flights WHERE time_stamp >= {ten_min_ago}  ALLOW FILTERING;"

    delay = session.execute(query)._current_rows
    print(delay)
    delay = delay.groupby(['time_stamp', 'arrival'], as_index=False).mean()
    delay['time_stamp'] = delay['time_stamp'].apply(datetime.fromtimestamp)
    delay = delay.set_index('arr_delay').drop([0])
    delay = delay.reset_index()

    fig = px.line(delay, x='time_stamp', y='arr_delay', color='arrival') 
    return fig

if __name__ == '__main__':
    app.run_server(debug=True)