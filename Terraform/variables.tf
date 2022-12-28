locals {
  data_lake_bucket = "data_lake"
}

variable "project" {
  description = "ebay-data-pipeline"
  default = "ebay-data-pipeline"
}

variable "region" {
  description = "Region for GCP resources."
  default = "us-east5"
  type = string
}


variable "BQ_DATASET" {
  description = "BigQuery Dataset that raw data (from GCS) will be written to"
  type = string
  default = "Ebay_MTG_Dual_Land_Saleszz"
}
