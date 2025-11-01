# EventBridge schedules for Lambda data collection

# Weekly collection - runs every Wednesday during season
# Collects current year: regular season, matchups, player details
resource "aws_cloudwatch_event_rule" "weekly_collection" {
  name                = "${var.project}-weekly-collection"
  description         = "Weekly data collection every Wednesday"
  schedule_expression = "cron(0 12 ? * WED *)"  # Every Wednesday at 12pm UTC (4am PST)
  
  state = var.enable_weekly_collection ? "ENABLED" : "DISABLED"
}

resource "aws_cloudwatch_event_target" "weekly_lambda" {
  rule      = aws_cloudwatch_event_rule.weekly_collection.name
  target_id = "lambda"
  arn       = aws_lambda_function.ingest.arn
  
  # Collect current year only
  input = jsonencode({
    year                   = var.current_year
    collect_playoffs       = false
    collect_player_totals  = false
  })
}

resource "aws_lambda_permission" "allow_weekly_eventbridge" {
  statement_id  = "AllowWeeklyExecutionFromEventBridge"
  action        = "lambda:InvokeFunction"
  function_name = aws_lambda_function.ingest.function_name
  principal     = "events.amazonaws.com"
  source_arn    = aws_cloudwatch_event_rule.weekly_collection.arn
}

# Season finale collection - runs January 15th
# Collects playoffs and player totals for completed season
resource "aws_cloudwatch_event_rule" "season_finale" {
  name                = "${var.project}-season-finale"
  description         = "Playoff and player totals collection after season"
  schedule_expression = "cron(0 12 15 1 ? *)"  # January 15th at 12pm UTC
  
  state = var.enable_season_finale_collection ? "ENABLED" : "DISABLED"
}

resource "aws_cloudwatch_event_target" "season_finale_lambda" {
  rule      = aws_cloudwatch_event_rule.season_finale.name
  target_id = "lambda"
  arn       = aws_lambda_function.ingest.arn
  
  # Collect previous year's complete data
  input = jsonencode({
    year                   = var.current_year - 1
    week                   = 17
    collect_playoffs       = true
    collect_player_totals  = true
  })
}

resource "aws_lambda_permission" "allow_season_finale_eventbridge" {
  statement_id  = "AllowSeasonFinaleExecutionFromEventBridge"
  action        = "lambda:InvokeFunction"
  function_name = aws_lambda_function.ingest.function_name
  principal     = "events.amazonaws.com"
  source_arn    = aws_cloudwatch_event_rule.season_finale.arn
}
