CREATE KEYSPACE flights_ks
WITH replication = {'class':'SimpleStrategy', 'replication_factor': 1};

CREATE TABLE flights(
    time_stamp bigint,
    fligth_num int,
    fligth_iata text,
    fligth_icao text,
    flight_date text,
    flight_status text,
    departure text,
    dep_delay int,
    arrival text,
    arr_delay int,
    airline text,
    PRIMARY KEY(time_stamp,fligth_iata,fligth_icao)
);
