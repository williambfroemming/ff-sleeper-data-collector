variable "project" {
  type = string
}

variable "aws_region" {
  type    = string
  default = "us-west-2" # QuickSight-compatible region
}

variable "lake_bucket" {
  type    = string
  default = null # if null, name is derived from project + region
}

variable "lambda_schedule_cron" {
  type    = string
  default = "cron(0 14 ? * MON-FRI *)" # 7am PT weekdays
}

variable "quicksight_user" {
  type        = string
  description = "QuickSight username (usually your email or IAM username)"
  default     = "william"
  # Example: "admin/your-email@example.com" or "your-iam-username"
  # To find: Login to QuickSight → Click profile icon → Copy username
}