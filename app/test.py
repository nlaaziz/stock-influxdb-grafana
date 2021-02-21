import time
from datetime import datetime

from influxdb_client import InfluxDBClient, Point, WritePrecision
from influxdb_client.client.write_api import SYNCHRONOUS

# You can generate a Token from the "Tokens Tab" in the UI
token = "Qja94aR19EopLmK5RAr-u5m3v59EKe_T4Ft6rLa7SiDNqRPbQDi74ytaSY4S3-NXovXk8vJxRaewPZCcCelbEA=="
org = "test"
bucket = "stock"

client = InfluxDBClient(url="http://influxdb:8086", token=token)

write_api = client.write_api(write_options=SYNCHRONOUS)

data = "test1 val=23.43234543"
write_api.write(bucket, org, data)

while True:
    time.sleep(5)
