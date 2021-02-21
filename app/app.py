import time
import requests
import json
import os

from datetime import datetime
from influxdb_client import InfluxDBClient, Point, WritePrecision
from influxdb_client.client.write_api import SYNCHRONOUS

# You can generate a Token from the "Tokens Tab" in the UI
influx_url= os.environ['INFLUX-URL']
token = os.environ['INFLUX-TOKEN']
org = os.environ['INFLUX-ORG']
bucket = os.environ['INFLUX-BUCKET']
alpha_api_key = os.environ['ALPHA-API-KEY']
alpha_url = os.environ['ALPHA-URL']
symbols = os.environ['SYMBOLS'].split(",")
last_data = os.environ['LAST-DATA']

def get_alpha_data(symbol):
    alpha_query_url = alpha_url.format(symbol=symbol, alpha_api_key=alpha_api_key)
    print("symbol %s = > url alpha %s " % (symbol, alpha_query_url))
    response_alpha_data = requests.get(alpha_query_url).json()
    print(response_alpha_data)
    return response_alpha_data

def write_data_influxdb(stock_day, stock_day_data):
    stock_day_reformat = stock_day.split("-")
    stock_datetime = datetime(int(stock_day_reformat[0]), int(stock_day_reformat[1]), int(stock_day_reformat[2]), 0, 0, 0, 0)
    print(stock_datetime)
    stock_timestamp = int(datetime.timestamp(stock_datetime))
    print(stock_timestamp)
    influx_data = "{symbol} val={symbol_val} {stock_timestamp}000000000".format(symbol=symbol,
                                                                                symbol_val=stock_day_data["4. close"],
                                                                                stock_timestamp=stock_timestamp)
    print(influx_data)

    client = InfluxDBClient(url=influx_url, token=token)
    write_api = client.write_api(write_options=SYNCHRONOUS)
    write_api.write(bucket, org, influx_data)

def fill_influxdb(daily_alpha_data):
    for stock_day, stock_day_data in daily_alpha_data.items():
        write_data_influxdb(stock_day, stock_day_data)

for symbol in symbols:
    response_alpha_data = get_alpha_data(symbol)
    stock_day = datetime.today().strftime("%y-%m-%d")
    daily_alpha_data = response_alpha_data["Time Series (Daily)"]
    if last_data and stock_day in daily_alpha_data:
        stock_day_data = daily_alpha_data[stock_day]
        write_last_data_influxdb(stock_day, stock_day_data)
    elif not last_data:
        fill_influxdb(daily_alpha_data)
    else:
        print("Nothing To Do")
        time.sleep(10)
