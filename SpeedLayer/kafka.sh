screen  zoookeeper -server -start.sh  kafka/config/zookeeper.properties
screen  kafka -server -start.sh  kafka/config/server.properties

kafka -topics.sh --create  --topic flights_json  --bootstrap -serverlocalhost :9092