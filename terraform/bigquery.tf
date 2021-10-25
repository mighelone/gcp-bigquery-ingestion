resource "google_bigquery_dataset" "dataset" {
  dataset_id                  = var.dataset
  location = "europe-west2"
}

resource "google_bigquery_table" "entries" {
  dataset_id = google_bigquery_dataset.dataset.dataset_id
  table_id   = "entries"

  time_partitioning {
    type = "DAY"
  }

  schema = file("../schema.json")

}
