from kafka import KafkaConsumer
from cassandra.cluster import Cluster
from json import loads

consumer = KafkaConsumer(
    'flights_json',
    bootstrap_servers=['localhost:9092'],
    auto_offset_reset='latest',
    enable_auto_commit=True,
    group_id='cassandra',
    value_deserializer=lambda x: loads(x.decode('utf-8'))
)

cluster = Cluster()
session = cluster.connect('flights_ks')

for msg in consumer:
    message = msg.value
    time_stamp = message.get('time_stamp')
    fligth_num = message.get('flight').get('number')
    fligth_iata = message.get('flight').get('iata')
    fligth_icao = message.get('flight').get('icao')
    flight_date = message.get('flight_date')
    flight_status = message.get('flight_status')
    
    departure = message.get('departure').get('airport')
    dep_delay = message.get('departure').get('delay')
    if dep_delay == None:
        dep_delay = '0'
    arrival = message.get('arrival').get('airport')
    arr_delay = message.get('arrival').get('delay')
    if arr_delay == None:
        arr_delay = '0'
    airline = message.get('airline').get('name')
    
    query = 'INSERT INTO flights (time_stamp, fligth_num, fligth_iata, fligth_icao, flight_date, flight_status, departure, dep_delay, arrival, arr_delay, airline)'
    query += f" VALUES ({time_stamp}, {fligth_num}, '{fligth_iata}', '{fligth_icao}', '{flight_date}', '{flight_status}', '{departure}', {dep_delay}, '{arrival}', {arr_delay}, '{airline}');"
    
    try:
        session.execute(query)
        print(query)
    except:
        print('WARNING: Invalid Input Value, query omited.')