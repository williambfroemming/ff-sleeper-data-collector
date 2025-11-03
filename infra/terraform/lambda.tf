# Lambda function
resource "aws_lambda_function" "ingest" {
  function_name = "${var.project}-ingest"
  role          = aws_iam_role.lambda_ingest.arn
  handler       = "lambda_function.handler"
  runtime       = "python3.12"

  s3_bucket = "ff-data-project-lambda-artifacts-us-west-2"
  s3_key    = "lambda_deployment.zip"

  timeout     = 900
  memory_size = 2048

  # Use AWS public layer ARN directly for us-west-2
  layers = ["arn:aws:lambda:us-west-2:336392948345:layer:AWSSDKPandas-Python312:13"]

  environment {
    variables = {
      LAKE_BUCKET        = aws_s3_bucket.lake.bucket
      KMS_KEY_ARN        = aws_kms_key.lake.arn
      CURRENT_LEAGUE_ID  = var.current_league_id
      CURRENT_YEAR       = var.current_year
      HISTORICAL_LEAGUES = jsonencode(var.historical_leagues)
      NAME_MAP           = jsonencode(var.name_map)
      SCORING_SETTINGS   = jsonencode(var.scoring_settings)
    }
  }

  depends_on = [aws_iam_role_policy_attachment.lambda_ingest_attach]
}

# CloudWatch Log Group
resource "aws_cloudwatch_log_group" "lambda_ingest" {
  name              = "/aws/lambda/${aws_lambda_function.ingest.function_name}"
  retention_in_days = 14
}

# SNS topic for failure notifications
resource "aws_sns_topic" "lambda_failures" {
  name = "${var.project}-lambda-failures"
}

resource "aws_cloudwatch_metric_alarm" "lambda_errors" {
  alarm_name          = "${var.project}-lambda-errors"
  comparison_operator = "GreaterThanThreshold"
  evaluation_periods  = 1
  metric_name         = "Errors"
  namespace           = "AWS/Lambda"
  period              = 300
  statistic           = "Sum"
  threshold           = 0
  alarm_description   = "Alert when Lambda function fails"
  alarm_actions       = [aws_sns_topic.lambda_failures.arn]

  dimensions = {
    FunctionName = aws_lambda_function.ingest.function_name
  }
}
