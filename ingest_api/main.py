import requests
import json
import logging
import os
import datetime as dt
from google.cloud import bigquery

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



def insert_bigquery(event, context):
    url = os.environ.get("URL", "https://api.publicapis.org/entries")
    table_name = os.environ.get("TABLE", "entries")
    dataset = os.environ.get("DATASET", "mobkoi")

    log.info(event)
    response = requests.get(url)

    response.raise_for_status()

    data = response.json()

    log.info(f"N. entries {data['count']} @ {context.timestamp}")

    ts = dt.datetime.strptime(context.timestamp, "%Y-%m-%dT%H:%M:%S.%fZ")
    log.info(f"Timestamp {ts}")
    records = [
        dict(date=ts.strftime("%Y-%m-%d"), timestamp=ts.isoformat(), **entry)
        for entry in data["entries"]
    ]

    bq = bigquery.Client()

    table = bq.dataset(dataset).table(table_name)

    errors = bq.insert_rows_json(
        table=table,
        json_rows=records,
    )

    if errors:
        log.error("Error loading data into bigquery")
        raise BigQueryError(errors)
    log.info(f"Data succesfully loaded to bigquery {dataset}.{table_name}")




if __name__ == "__main__":
    from dataclasses import dataclass, field
    import datetime as dt

    @dataclass
    class Context:
        # timestamp: dt.datetime = field(default_factory=lambda: dt.datetime.utcnow())
        timestamp: str = "2021-10-22T18:08:22.264Z"

    insert_bigquery(event={}, context=Context())