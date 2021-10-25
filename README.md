# GCP task

## Meteostat ingestion

Hourly data from [Meteostat APIs](https://dev.meteostat.net/) are ingested for stations around London.
Python `meteostat` API library are used for ingesting the data.

## Architecture

A cloud function is used for ingesting the data. The task is executed daily using a Cloud Function written in 
Python 3.9.
The cloud function is activated by receiving a message in a topic defined in the Pub/Sub service.
In order to trigger the job daily, a scheduler task is executed daily, publishing a message into the Pub/Sub topic.

The cloud function will ingest the horly weather data from the meteostat API.
First, the stations around London (top left (52, -0.5), bottom right (50, 0.5)) are fetched, and then used to get the hourly weather data.
The data are finally inserted into a BigQuery table, using the Python BigQuery APIs.