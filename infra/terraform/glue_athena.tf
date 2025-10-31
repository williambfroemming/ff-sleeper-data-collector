resource "aws_glue_catalog_database" "raw" { name = "${var.project}_raw" }
resource "aws_glue_catalog_database" "silver" { name = "${var.project}_silver" }
resource "aws_glue_catalog_database" "gold" { name = "${var.project}_gold" }

resource "aws_athena_workgroup" "wg" {
  name = "${var.project}_wg"
  configuration {
    enforce_workgroup_configuration = true
    result_configuration {
      output_location = "s3://${aws_s3_bucket.lake.bucket}/athena/"
      encryption_configuration {
        encryption_option = "SSE_KMS"
        kms_key_arn       = aws_kms_key.lake.arn
      }
    }
  }
}
