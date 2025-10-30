variable "project" {
  type = string
}

variable "aws_region" {
  type    = string
  default = "us-west-2"
}

variable "lake_bucket" {
  type    = string
  default = null
}

variable "quicksight_spice" {
  type    = bool
  default = false
}

variable "lambda_schedule_cron" {
  type    = string
  # 7am PT weekdays; adjust later
  default = "cron(0 14 ? * MON-FRI *)"
}
