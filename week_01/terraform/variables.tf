terraform {
  required_version = ">= 1.0"
  backend "local" {}
  required_providers {
    google = {
      source = "hashicorp/google"
    }
  }
}

locals {
  data_lake_bucket = "dtc_data_lake"
}

variable "project" {
  description = "explorer-363509"  #project ID
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
  default = "/home/tomasoak/dataeng_zoomcamp/explorer-363509-9bf8f121680a.json"
}