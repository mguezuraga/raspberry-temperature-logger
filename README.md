# raspberry-temperature-logger
A simple project to measure and log temperature and humidity using the DHT22 sensor and a Raspberry Pi

# Requirements
## Hardware
- A Raspberry PI (I've used a Raspberry Pi 3 Model B Rev 1.2)
- A DHT sensor. I've used [this one](https://www.banggood.com/DHT22-Single-bus-Digital-Temperature-and-Humidity-Sensor-Module-Electronic-Building-Blocks-AM2302-3_3V-5V-DC-p-1457358.html?rmmds=myorder&cur_warehouse=CN) (Not an affiliate link)

## Setting up dependencies for the sensor
https://learn.adafruit.com/dht-humidity-sensing-on-raspberry-pi-with-gdocs-logging/python-setup

# Running

There are 2 ways to run this: Standalone (SQLite) and with a dedicated database server (PostgreSQL):

## SQLite
1. Create a `history.db` SQLite database
```
$ sqlite3 history.db
SQLite version 3.34.1 2021-01-20 14:10:07
Enter ".help" for usage hints.
sqlite> CREATE TABLE readings(
    temperature FLOAT,
    humidity FLOAT,
    Timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
);
sqlite>
```
2. Execution
```
$ python3 measure.py --log debug
2022-01-06 20:43:20,100 DEBUG:Temp: 21.1C Humidity: 66.7%
-snip-
[etc]
```

3. Verifying
```
$ sqlite3 history.db
SQLite version 3.34.1 2021-01-20 14:10:07
Enter ".help" for usage hints.
sqlite> select * from readings;
21.2|66.0|2022-01-05 20:42:27
21.1|67.4|2022-01-05 21:12:30
21.0|67.3|2022-01-05 21:42:30
-snip-
[etc]
```

## PostgreSQL
1. Install and set up PostgreSQL
```
sudo apt install postgresql
sudo su postgres
createuser pi -P --interactive # Choose a password here, and if you want this user to be administrative user
```

2. Create the database and table
```
pi@raspberrypi3:~ $ sudo su postgres
postgres@raspberrypi3:/home/pi$ psql
psql (13.5 (Raspbian 13.5-0+deb11u1))
Type "help" for help.

postgres=# CREATE TABLE readings(
    temperature double presicion not null,
    humidity double presicion not null,
    datetime timestamp with time zone default now()
);
```

3. Execution
```
$ python3 measure-pgsql.py --log debug
2022-01-12 19:24:00,206 DEBUG:Temp: 22.6C Humidity: 57.2%
2022-01-12 19:54:00,508 DEBUG:Temp: 22.6C Humidity: 57.1%
-snip-
[etc]
```

3. Verifying
```
pi@raspberrypi3:~ $ psql history
psql (13.5 (Raspbian 13.5-0+deb11u1))
Type "help" for help.

history=# select * from readings;
 temperature | humidity |           datetime
-------------+----------+-------------------------------
        22.7 |       58 | 2022-01-11 19:45:52.564362+00
        22.6 |     57.9 | 2022-01-11 19:47:23.655042+00
-snip-
[etc]
```
