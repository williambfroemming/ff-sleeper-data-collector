data "archive_file" "stub_zip" {
  type        = "zip"
  output_path = "${path.module}/lambda_stub.zip"

  # Each "source" block becomes a file inside the zip
  source {
    filename = "lambda_function.py"
    content  = <<-PY
      import json, datetime

      def handler(event, context):
          return {
              "status": "ok",
              "ts": datetime.datetime.utcnow().isoformat(),
              "note": "replace with Sleeper ingest later"
          }
    PY
  }
}

resource "aws_lambda_function" "ingest" {
  function_name = "${var.project}-ingest"
  role          = aws_iam_role.lambda_ingest.arn
  handler       = "lambda_function.handler"
  runtime       = "python3.12"

  # Zip produced by the archive_file data source
  filename         = data.archive_file.stub_zip.output_path
  source_code_hash = data.archive_file.stub_zip.output_base64sha256

  timeout = 30

  environment {
    variables = {
      LAKE_BUCKET = aws_s3_bucket.lake.bucket
      KMS_KEY_ARN = aws_kms_key.lake.arn
    }
  }

  depends_on = [aws_iam_role_policy_attachment.lambda_ingest_attach]
}
