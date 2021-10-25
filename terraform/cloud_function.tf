data "archive_file" "function_zip" {
  type        = "zip"
  output_path = "../mobkoi_function.zip"
#   excludes    = [ "${path.module}/unwanted.zip" ]

  source {
    content  = file("../ingest_api/main.py")
    filename = "main.py"
  }

  source {
    content  = file("../ingest_api/requirements.txt")
    filename = "requirements.txt"
  }
}

resource "google_storage_bucket" "bucket" {
  name = "mobkoi_functions"
}

resource "google_storage_bucket_object" "function_zipfile" {
  name   = "index.zip"
  bucket = google_storage_bucket.bucket.name
  source = data.archive_file.function_zip.output_path
}


resource "google_cloudfunctions_function" "scrape_api" {
  name        = "scrape-api"
  description = "Scrape API and copy to BigQuery"
  runtime     = "python39"

  available_memory_mb   = 256
  source_archive_bucket = google_storage_bucket.bucket.name
  source_archive_object = google_storage_bucket_object.function_zipfile.name
  event_trigger {
      event_type = "google.pubsub.topic.publish"
      resource = google_pubsub_topic.trigger.id
  }
  entry_point = "insert_bigquery"

  timeout = 540

  environment_variables = {
    URL = var.api_url
    TABLE = var.table
    DATASET = var.dataset
  }
#   trigger_http          = true
#   entry_point           = "helloGET"
}

# IAM entry for all users to invoke the function
resource "google_cloudfunctions_function_iam_member" "invoker" {
  project        = google_cloudfunctions_function.scrape_api.project
  region         = google_cloudfunctions_function.scrape_api.region
  cloud_function = google_cloudfunctions_function.scrape_api.name

  role   = "roles/cloudfunctions.invoker"
  member = "allUsers"
}