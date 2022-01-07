import requests

from kafka import KafkaProducer
from json import loads, dumps
from time import sleep
from datetime import datetime


producer = KafkaProducer(bootstrap_servers=['localhost:9092'],
                        value_serializer= lambda x: dumps(x).encode('utf-8'))

with open('access_key.txt', 'r') as f:
    access_key = f.read()

access_key = access_key[:-1]

while True:
    response = loads(requests.get(f'http://api.aviationstack.com/v1/flights?access_key={access_key}').text)

    data = response['data']

    for dat in data:
        now = datetime.now()
        time_stamp = int(datetime.timestamp(now))
        dat['time_stamp'] = time_stamp
        print(dat)
        producer.send('flights_json', value=dat)
        sleep(4)
