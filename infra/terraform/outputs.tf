output "lake_bucket" {
  value = aws_s3_bucket.lake.bucket
}

output "kms_key_arn" {
  value = aws_kms_key.lake.arn
}

output "glue_databases" {
  value = [
    aws_glue_catalog_database.raw.name,
    aws_glue_catalog_database.silver.name,
    aws_glue_catalog_database.gold.name
  ]
}

output "athena_workgroup" {
  value = aws_athena_workgroup.wg.name
}

output "lambda_name" {
  value = aws_lambda_function.ingest.function_name
}

output "quicksight_role_arn" {
  value       = aws_iam_role.quicksight.arn
  description = "IAM role ARN for QuickSight to assume"
}