locals {
  data_lake_bucket = "dtc_data_lake"
}

variable "project" {
  description = "canvas-provider-376717"  #project ID
  type = string
}

variable "region" {
  description = "Region for GCP resources. Choose as per your location: https://cloud.google.com/about/locations"
  default = "europe-north1"
  type = string
}

variable "storage_class" {
  description = "Storage class type for bucket."
  default = "STANDARD"
}

variable "BQ_DATASET" {
  description = "BigQuery Dataset that raw data (from GCS) will be written to"
  type = string
  default = "trips_data_all"
}

variable "credentials" {
  type = string
  default = "~/dataeng_zoomcamp/canvas-provider-376717-e57799392c50.json"
}