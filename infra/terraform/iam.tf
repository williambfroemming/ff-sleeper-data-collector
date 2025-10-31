resource "aws_iam_role" "lambda_ingest" {
  name = "${var.project}-lambda-ingest-role"
  assume_role_policy = jsonencode({
    Version = "2012-10-17",
    Statement = [{
      Effect    = "Allow",
      Principal = { Service = "lambda.amazonaws.com" },
      Action    = "sts:AssumeRole"
    }]
  })
}

resource "aws_iam_policy" "lambda_ingest_policy" {
  name = "${var.project}-lambda-ingest-policy"
  policy = jsonencode({
    Version = "2012-10-17",
    Statement = [
      {
        Sid    = "S3LakePut",
        Effect = "Allow",
        Action = ["s3:PutObject", "s3:AbortMultipartUpload", "s3:ListBucket"],
        Resource = [
          "arn:aws:s3:::${aws_s3_bucket.lake.bucket}",
          "arn:aws:s3:::${aws_s3_bucket.lake.bucket}/*"
        ]
      },
      {
        Sid      = "KMSUse",
        Effect   = "Allow",
        Action   = ["kms:Encrypt", "kms:Decrypt", "kms:GenerateDataKey*", "kms:DescribeKey"],
        Resource = [aws_kms_key.lake.arn]
      },
      {
        Sid      = "CWLogs",
        Effect   = "Allow",
        Action   = ["logs:CreateLogGroup", "logs:CreateLogStream", "logs:PutLogEvents"],
        Resource = "*"
      },
      {
        Sid      = "Network",
        Effect   = "Allow",
        Action   = ["ec2:CreateNetworkInterface", "ec2:DescribeNetworkInterfaces", "ec2:DeleteNetworkInterface"],
        Resource = "*"
      }
    ]
  })
}

resource "aws_iam_role_policy_attachment" "lambda_ingest_attach" {
  role       = aws_iam_role.lambda_ingest.name
  policy_arn = aws_iam_policy.lambda_ingest_policy.arn
}

# ========================================
# QuickSight IAM Resources
# ========================================

# Data source for AWS account info
data "aws_caller_identity" "current" {}

resource "aws_iam_role" "quicksight" {
  name = "${var.project}-quicksight-role"

  assume_role_policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        Effect = "Allow"
        Principal = {
          Service = "quicksight.amazonaws.com"
        }
        Action = "sts:AssumeRole"
      }
    ]
  })
}

resource "aws_iam_policy" "quicksight_access" {
  name        = "${var.project}-quicksight-access-policy"
  description = "Allow QuickSight to access Athena, Glue, and S3"

  policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        Sid    = "AthenaAccess"
        Effect = "Allow"
        Action = [
          "athena:BatchGetQueryExecution",
          "athena:GetQueryExecution",
          "athena:GetQueryResults",
          "athena:GetWorkGroup",
          "athena:ListWorkGroups",
          "athena:StartQueryExecution",
          "athena:StopQueryExecution",
          "athena:GetQueryResultsStream",
          "athena:ListQueryExecutions"
        ]
        Resource = [
          aws_athena_workgroup.wg.arn,
          "arn:aws:athena:${var.aws_region}:${data.aws_caller_identity.current.account_id}:workgroup/*"
        ]
      },
      {
        Sid    = "GlueCatalogAccess"
        Effect = "Allow"
        Action = [
          "glue:GetDatabase",
          "glue:GetDatabases",
          "glue:GetTable",
          "glue:GetTables",
          "glue:GetPartition",
          "glue:GetPartitions",
          "glue:BatchGetPartition"
        ]
        Resource = [
          "arn:aws:glue:${var.aws_region}:${data.aws_caller_identity.current.account_id}:catalog",
          "arn:aws:glue:${var.aws_region}:${data.aws_caller_identity.current.account_id}:database/${aws_glue_catalog_database.raw.name}",
          "arn:aws:glue:${var.aws_region}:${data.aws_caller_identity.current.account_id}:database/${aws_glue_catalog_database.silver.name}",
          "arn:aws:glue:${var.aws_region}:${data.aws_caller_identity.current.account_id}:database/${aws_glue_catalog_database.gold.name}",
          "arn:aws:glue:${var.aws_region}:${data.aws_caller_identity.current.account_id}:table/${aws_glue_catalog_database.raw.name}/*",
          "arn:aws:glue:${var.aws_region}:${data.aws_caller_identity.current.account_id}:table/${aws_glue_catalog_database.silver.name}/*",
          "arn:aws:glue:${var.aws_region}:${data.aws_caller_identity.current.account_id}:table/${aws_glue_catalog_database.gold.name}/*"
        ]
      },
      {
        Sid    = "S3DataLakeRead"
        Effect = "Allow"
        Action = [
          "s3:GetObject",
          "s3:GetObjectVersion",
          "s3:ListBucket",
          "s3:GetBucketLocation"
        ]
        Resource = [
          "arn:aws:s3:::${aws_s3_bucket.lake.bucket}",
          "arn:aws:s3:::${aws_s3_bucket.lake.bucket}/*"
        ]
      },
      {
        Sid    = "S3AthenaResults"
        Effect = "Allow"
        Action = [
          "s3:GetObject",
          "s3:GetObjectVersion",
          "s3:PutObject",
          "s3:DeleteObject",
          "s3:ListBucket"
        ]
        Resource = [
          "arn:aws:s3:::${aws_s3_bucket.lake.bucket}/athena/*"
        ]
      },
      {
        Sid    = "KMSDecrypt"
        Effect = "Allow"
        Action = [
          "kms:Decrypt",
          "kms:DescribeKey",
          "kms:GenerateDataKey"
        ]
        Resource = [aws_kms_key.lake.arn]
      }
    ]
  })
}

resource "aws_iam_role_policy_attachment" "quicksight_attach" {
  role       = aws_iam_role.quicksight.name
  policy_arn = aws_iam_policy.quicksight_access.arn
}