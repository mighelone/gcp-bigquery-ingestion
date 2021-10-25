resource "google_pubsub_topic" "trigger" {
  name = "trigger-ingestion"

  labels = {
    project = "mobkoi"
  }
}

resource "google_cloud_scheduler_job" "trigger" {
  name        = "trigger-ingestion"
  description = "Trigger ingestion daily"
  schedule    = "30 1 * * *"
  time_zone        = "Europe/London"

  pubsub_target {
    # topic.id is the topic's full resource name.
    topic_name = google_pubsub_topic.trigger.id
    data       = base64encode("trigger")
  }

}