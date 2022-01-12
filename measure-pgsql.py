# Inspired by https://learn.adafruit.com/dht-humidity-sensing-on-raspberry-pi-with-gdocs-logging/python-setup
# Requires python3-psycopg2

import argparse
import logging
import psycopg2
import sys
import time
import configparser

import adafruit_dht
import board

def get_db_connection_params() -> str:
    config = configparser.ConfigParser()
    config.read('db.cfg')
    
    db = dict(config.items('pgsql'))
    
    return ' '.join(x + '=' + y for x, y in db.items())

def measure() -> str:
    # Initial the dht device, with data pin connected to:
    dhtDevice = adafruit_dht.DHT22(board.D4)

    # you can pass DHT22 use_pulseio=False if you wouldn't like to use pulseio.
    # This may be necessary on a Linux single board computer like the Raspberry Pi,
    # but it will not work in CircuitPython.
    # dhtDevice = adafruit_dht.DHT22(board.D18, use_pulseio=False)

    connect_str = get_db_connection_params()
    
    try:
        conn = psycopg2.connect(connect_str)
        c = conn.cursor()
    except Exception as error:
        logging.critical('Something went wrong trying to write to the DB: {}'.format(error))
        sys.exit(1)

    while True:
        try:
            temperature = dhtDevice.temperature
            humidity = dhtDevice.humidity
            logging.debug("Temp: {:.1f}C Humidity: {}% ".format( temperature, humidity))
            c.execute("INSERT INTO readings (temperature, humidity) VALUES ({t}, {h})".format(t=temperature, h=humidity))
            conn.commit()

        except RuntimeError as error:
            # Errors happen fairly often, DHT's are hard to read, just keep going
            logging.warning(error.args[0])
            time.sleep(2.0)
            continue
        except psycopg2.DatabaseError as error:
            logging.critical('Something went wrong trying to write to the DB: {}'.format(error))
            sys.exit(1)
        except Exception as error:
            dhtDevice.exit()
            raise error

        # Log every 30 minutes
        time.sleep(60 * 30)

def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument('--log', default='warning', help='log level')
    args = parser.parse_args()

    levels = {
        "critical": logging.CRITICAL,
        "error": logging.ERROR,
        "warning": logging.WARNING,
        "info": logging.INFO,
        "debug": logging.DEBUG,
    }
    level = levels.get(args.log.lower())
    if level is None:
        raise ValueError(
            f"log level given: {args.log}"
            f" -- must be one of: {' | '.join(levels.keys())}"
        )
    logging.basicConfig(format='%(asctime)s %(levelname)s:%(message)s', level=level)

    measure()

if __name__ == '__main__':
    main()
