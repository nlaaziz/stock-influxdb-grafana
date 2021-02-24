import json

from datetime import datetime
from influxdb_client import InfluxDBClient, Point, WritePrecision
from influxdb_client.client.write_api import SYNCHRONOUS


class Config:
    def __init__(self, conf_file, influx_url, token, bucket, org):
        self.conf_file = conf_file
        self.influx_url = influx_url
        self.token = token
        self.bucket = bucket
        self.org = org
        with open(self.conf_file) as f:
            data = json.load(f)
        self.shares = data["shares"]
        print(self.shares)


    def push_shares_to_influxdb(self):
        for share in self.shares:
            share_date = share["time"].split("-")
            share_datetime = datetime(int(share_date[0]), int(share_date[1]), int(share_date[2]), 0, 0, 0, 0)
            print(share_datetime)
            share_timestamp = int(datetime.timestamp(share_datetime))
            print(share_timestamp)
            influx_data = "shares,symbol={symbol} val={number} {share_timestamp}000000000".format(symbol=share["symbol"],
                                                                                                  number=share["number"],
                                                                                                  share_timestamp=share_timestamp)
            print(influx_data)

            client = InfluxDBClient(url=self.influx_url, token=self.token)
            write_api = client.write_api(write_options=SYNCHRONOUS)
            write_api.write(self.bucket, self.org, influx_data)
