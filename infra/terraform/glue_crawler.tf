# IAM role for the crawler
resource "aws_iam_role" "glue_crawler" {
  name = "${var.project}-glue-crawler-role"
  assume_role_policy = jsonencode({
    Version = "2012-10-17",
    Statement = [{
      Effect    = "Allow",
      Principal = { Service = "glue.amazonaws.com" },
      Action    = "sts:AssumeRole"
    }]
  })
}

# Attach AWS managed baseline for Glue service roles
resource "aws_iam_role_policy_attachment" "glue_crawler_managed" {
  role       = aws_iam_role.glue_crawler.name
  policy_arn = "arn:aws:iam::aws:policy/service-role/AWSGlueServiceRole"
}

# Extra S3 + Glue Catalog + KMS permissions for our lake
resource "aws_iam_policy" "glue_crawler_extras" {
  name = "${var.project}-glue-crawler-extras"
  policy = jsonencode({
    Version = "2012-10-17",
    Statement = [
      {
        Sid : "LakeList",
        Effect : "Allow",
        Action : ["s3:ListBucket"],
        Resource : ["arn:aws:s3:::${aws_s3_bucket.lake.bucket}"]
      },
      {
        Sid : "LakeRead",
        Effect : "Allow",
        Action : ["s3:GetObject", "s3:ListBucket"],
        Resource : ["arn:aws:s3:::${aws_s3_bucket.lake.bucket}/staging/*"]
      },
      {
        Sid : "GlueCatalog",
        Effect : "Allow",
        Action : [
          "glue:CreateTable", "glue:UpdateTable", "glue:DeleteTable",
          "glue:GetTable", "glue:GetTables", "glue:CreateDatabase",
          "glue:GetDatabase", "glue:GetDatabases",
          "glue:BatchCreatePartition", "glue:BatchGetPartition", "glue:BatchDeletePartition",
          "glue:UpdateDatabase"
        ],
        Resource : ["*"]
      },
      {
        Sid : "UseLakeKMS",
        Effect : "Allow",
        Action : [
          "kms:Decrypt",
          "kms:DescribeKey",
          "kms:GenerateDataKey",
          "kms:GenerateDataKeyWithoutPlaintext"
        ],
        Resource : ["${aws_kms_key.lake.arn}"]
      },
      {
        Sid : "Logs",
        Effect : "Allow",
        Action : ["logs:CreateLogGroup", "logs:CreateLogStream", "logs:PutLogEvents"],
        Resource : ["*"]
      }
    ]
  })
}

resource "aws_iam_role_policy_attachment" "glue_crawler_extras_attach" {
  role       = aws_iam_role.glue_crawler.name
  policy_arn = aws_iam_policy.glue_crawler_extras.arn
}

resource "aws_glue_crawler" "staging_legacy_excel" {
  name          = "${var.project}-staging-legacy-excel"
  role          = aws_iam_role.glue_crawler.arn
  database_name = aws_glue_catalog_database.raw.name
  table_prefix  = "stg_"

  s3_target {
    path = "s3://${aws_s3_bucket.lake.bucket}/staging/legacy_excel/"
  }

  configuration = jsonencode({
    Version       = 1.0,
    CrawlerOutput = { Partitions = { AddOrUpdateBehavior = "InheritFromTable" } },
    Grouping      = { TableLevelConfiguration = 3 }
  })

  schema_change_policy {
    delete_behavior = "LOG"
    update_behavior = "UPDATE_IN_DATABASE"
  }

  recrawl_policy {
    recrawl_behavior = "CRAWL_EVERYTHING"
  }
}
