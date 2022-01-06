# raspberry-temperature-logger
A simple project to measure and log temperature and humidity using the DHT22 sensor and a Raspberry Pi

# Requirements
## Hardware
- A Raspberry PI
- A DHT sensor. I've used [this one](https://www.banggood.com/DHT22-Single-bus-Digital-Temperature-and-Humidity-Sensor-Module-Electronic-Building-Blocks-AM2302-3_3V-5V-DC-p-1457358.html?rmmds=myorder&cur_warehouse=CN) (Not an affiliate link)

## Python dependencies
https://learn.adafruit.com/dht-humidity-sensing-on-raspberry-pi-with-gdocs-logging/python-setup

# Running

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
