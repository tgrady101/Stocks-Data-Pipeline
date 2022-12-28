locals {
  data_lake_bucket = "data_lake"
}

variable "project" {
  description = "stocks-data-pipeline"
  default = "stocks-data-pipeline"
}

variable "region" {
  description = "Region for GCP resources."
  default = "us-east5"
  type = string
}


variable "STOCK_DATASET" {
  description = "BigQuery Dataset to hold information about various S&P 500 stocks"
  type = string
  default = "Stock_Info_Dataset"
}

variable "STOCK_VAL_TABLE"{

  description = "End of day values for S&P 500 stocks"
  type = string
  default = "stock_values"
}

variable "BTC_VAL_TABLE"{

  description = "End of day values for Bitcoin"
  type = string
  default = "BTC_values"
}

variable "STOCK_INFO_TABLE"{

  description = "Information about S&P 500 companies"
  type = string
  default = "stock_info"
}

