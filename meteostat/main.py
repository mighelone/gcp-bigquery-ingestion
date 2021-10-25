from meteostat import Hourly, Stations
import logging
from google.cloud import bigquery
import json
import datetime as dt
import os

import pandas as pd

logging.basicConfig(level=logging.INFO)
log = logging.getLogger(__name__)

class BigQueryError(Exception):
    '''Exception raised whenever a BigQuery error happened''' 

    def __init__(self, errors):
        super().__init__(self._format(errors))
        self.errors = errors

    def _format(self, errors):
        err = []
        for error in errors:
            err.extend(error['errors'])
        return json.dumps(err)

def format_errors(errors):
    err = [
        error['errors']
        for error in errors
    ]
    return json.dumps(err)

def handler(event, context):
    table_name = os.environ.get("TABLE", "meteostat")
    dataset = os.environ.get("DATASET", "mobkoi")
    # get the previous day
    timestamp = dt.datetime.strptime(context.timestamp, "%Y-%m-%dT%H:%M:%S.%fZ") - dt.timedelta(days=1)
    start_time = timestamp.replace(hour=0, minute=0, second=0, microsecond=0)
    end_time = timestamp.replace(hour=23, minute=59, second=59, microsecond=999999)
    log.info(f"Getting meteo data for {timestamp}")

    # get the stations arounf London
    stations = Stations().bounds((52,-0.5),(50,0.5)).fetch()
    # get the hourly data for the given stations and time range
    data = Hourly(stations, start=start_time, end=end_time).fetch().reset_index()
    data["time"] = data["time"].dt.strftime("%Y-%m-%dT%H:%M:%S.%fZ")
    records = data.to_dict(orient="records")
    log.info(f"Fetched {len(records)} records for {stations.shape[0]} stations")
    
    bq = bigquery.Client()

    table = bq.dataset(dataset).table(table_name)

    error_chuncks = bq.insert_rows_from_dataframe(bq.get_table(table), data)

    message = "\n".join(
        [format_errors(errors) for errors in error_chuncks]
    )
    if message:
        raise RuntimeError(message)

if __name__ == "__main__":
    from dataclasses import dataclass, field
    import datetime as dt

    @dataclass
    class Context:
        # timestamp: dt.datetime = field(default_factory=lambda: dt.datetime.utcnow())
        timestamp: str = "2021-10-18T18:08:22.264Z"

    handler(event={}, context=Context())