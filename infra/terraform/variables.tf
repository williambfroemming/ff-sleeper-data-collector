variable "project" {
  type = string
}

variable "aws_region" {
  type    = string
  default = "us-west-2"
}

variable "lake_bucket" {
  type    = string
  default = null # if null, name is derived from project + region
}

variable "lambda_schedule_cron" {
  type    = string
  default = "cron(0 14 ? * MON-FRI *)" # 7am PT weekdays
}
