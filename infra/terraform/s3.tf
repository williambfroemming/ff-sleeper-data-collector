locals {
  lake_bucket_name = coalesce(var.lake_bucket, "${var.project}-lake-${var.aws_region}")
}

resource "aws_s3_bucket" "lake" {
  bucket = local.lake_bucket_name
}

resource "aws_s3_bucket_versioning" "lake" {
  bucket = aws_s3_bucket.lake.id
  versioning_configuration { status = "Enabled" }
}

resource "aws_s3_bucket_server_side_encryption_configuration" "lake" {
  bucket = aws_s3_bucket.lake.id
  rule {
    apply_server_side_encryption_by_default {
      kms_master_key_id = aws_kms_key.lake.arn
      sse_algorithm     = "aws:kms"
    }
  }
}

resource "aws_s3_bucket_public_access_block" "lake" {
  bucket                  = aws_s3_bucket.lake.id
  block_public_acls       = true
  block_public_policy     = true
  ignore_public_acls      = true
  restrict_public_buckets = true
}

# Create useful prefixes (optional but nice to have)
resource "aws_s3_object" "folders" {
  for_each = toset([
    "raw/", "silver/", "gold/", "athena/", "staging/legacy_excel/", "exports/"
  ])
  bucket       = aws_s3_bucket.lake.id
  key          = each.value
  content      = ""
  content_type = "application/x-directory"
  depends_on   = [aws_s3_bucket_public_access_block.lake]
}
