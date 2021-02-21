import time
import requests
import json

from datetime import datetime

from influxdb_client import InfluxDBClient, Point, WritePrecision
from influxdb_client.client.write_api import SYNCHRONOUS

# You can generate a Token from the "Tokens Tab" in the UI
token = "Qja94aR19EopLmK5RAr-u5m3v59EKe_T4Ft6rLa7SiDNqRPbQDi74ytaSY4S3-NXovXk8vJxRaewPZCcCelbEA=="
org = "test"
bucket = "stock"
alpha_api_key = "2IX3H2UPE39MNJF6"
alpha_url = "https://www.alphavantage.co/query?function=TIME_SERIES_DAILY&symbol={symbol}&apikey={alpha_api_key}"
#alpha_url = "https://www.alphavantage.co/query?outputsize=full&function=TIME_SERIES_DAILY&symbol={symbol}&apikey={alpha_api_key}"
symbols = ["AAPL", "ABNB", "AMZN", "GOOGL", "MSFT", "NET", "NFLX", "PINS", "REGI", "NIO", "TSLA"]

time.sleep(10)
for symbol in symbols:
    alpha_query_url = alpha_url.format(symbol=symbol, alpha_api_key=alpha_api_key)
    response_alpha_data = requests.get(alpha_query_url).json()
    print(response_alpha_data)
    for stock_day, stock_day_data in response_alpha_data["Time Series (Daily)"].items():
        stock_day_reformat = stock_day.split("-")
        stock_datetime = datetime(int(stock_day_reformat[0]), int(stock_day_reformat[1]), int(stock_day_reformat[2]), 0, 0, 0, 0)
        print(stock_datetime)
        stock_timestamp = int(datetime.timestamp(stock_datetime))
        print(stock_timestamp)
        influx_data = "{symbol} val={symbol_val} {stock_timestamp}000000000".format(symbol=symbol,
                                                                                    symbol_val=stock_day_data["4. close"],
                                                                                    stock_timestamp=stock_timestamp)
        print(influx_data)

        client = InfluxDBClient(url="http://influxdb:8086", token=token)
        write_api = client.write_api(write_options=SYNCHRONOUS)
        write_api.write(bucket, org, influx_data)

        time.sleep(1)
