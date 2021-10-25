resource "google_bigquery_dataset" "dataset" {
  dataset_id                  = var.dataset
  location = "europe-west2"
}

resource "google_bigquery_table" "entries" {
  dataset_id = google_bigquery_dataset.dataset.dataset_id
  table_id   = var.table

  time_partitioning {
    type = "DAY"
  }

  schema = file("../meteostat/schema.json")

}
