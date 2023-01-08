terraform {
  required_version = ">=1.0"
  backend "local" {}
  required_providers {
    google = {
        source = "hashicorp/google"
    }
  }
}

provider "google" {
    project = var.project
    region = var.region  
}

resource "google_storage_bucket" "data-lake-bucket" {
  name          = "${local.data_lake_bucket}_${var.project}" 
  location      = var.region

  storage_class = "STANDARD"
  uniform_bucket_level_access = true

  versioning {
    enabled     = true
  }

  lifecycle_rule {
    action {
      type = "Delete"
    }
    condition {
      age = 30  
    }
  }

  force_destroy = true
}

resource "google_bigquery_dataset" "default" {
  dataset_id = var.STOCK_DATASET
  project    = var.project
  location   = var.region
}

resource "google_bigquery_table" "stock_val" {
  dataset_id = google_bigquery_dataset.default.dataset_id
  table_id   = var.STOCK_VAL_TABLE
  project = var.project
  description = var.STOCK_VAL_TABLE
}

resource "google_bigquery_table" "stock_info" {
  dataset_id = google_bigquery_dataset.default.dataset_id
  table_id   = var.STOCK_INFO_TABLE
  project = var.project
  description = var.STOCK_INFO_TABLE
}

resource "google_bigquery_table" "btc_val" {
  dataset_id = google_bigquery_dataset.default.dataset_id
  table_id   = var.BTC_VAL_TABLE
  project = var.project
  description = var.BTC_VAL_TABLE
}
