variable "credentials" {
  description = "My credentials"
  default     = "./keys/my-creds.json"
}

variable "project_name" {
  description = "My Project Name"
  default     = "terraform-demo-412115"
}

variable "location" {
  description = "Project Location"
  default     = "US"
}

variable "bq_dataset_name" {
  description = "My BigQuery Dataset Name"
  default     = "demo_dataset"
}

variable "gcs_bucket_name" {
  description = "My Storage Bucket Name"
  default     = "terraform-demo-412115-terra-bucket"
}

variable "gcs_storage_class" {
  description = "Bucket Storage Class"
  default     = "STANDARD"
}

variable "region_name" {
  description = "Project region"
  default     = "us-central1"
}
