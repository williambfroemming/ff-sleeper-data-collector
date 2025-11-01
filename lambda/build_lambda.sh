#!/bin/bash
set -e

echo "======================================"
echo "Building Lambda Deployment Package"
echo "======================================"

FUNCTION_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
BUILD_DIR="${FUNCTION_DIR}/build"
PACKAGE_DIR="${BUILD_DIR}/package"
DEPLOYMENT_PACKAGE="${FUNCTION_DIR}/lambda_deployment.zip"

echo "Cleaning previous builds..."
rm -rf "${BUILD_DIR}"
rm -f "${DEPLOYMENT_PACKAGE}"
mkdir -p "${PACKAGE_DIR}"

echo "Installing Python dependencies..."
pip install -r requirements.txt -t "${PACKAGE_DIR}" --platform manylinux2014_x86_64 --only-binary=:all:

echo "Copying source code..."
cp lambda_function.py "${PACKAGE_DIR}/"
cp -r collectors "${PACKAGE_DIR}/"
cp -r utils "${PACKAGE_DIR}/"

echo "Creating deployment package..."
cd "${PACKAGE_DIR}"
zip -r "${DEPLOYMENT_PACKAGE}" . -q

PACKAGE_SIZE=$(du -h "${DEPLOYMENT_PACKAGE}" | cut -f1)
echo "SUCCESS: Package created - ${DEPLOYMENT_PACKAGE} (${PACKAGE_SIZE})"

PACKAGE_SIZE_MB=$(du -m "${DEPLOYMENT_PACKAGE}" | cut -f1)
if [ ${PACKAGE_SIZE_MB} -gt 50 ]; then
    echo "WARNING: Package exceeds 50MB - upload to S3 first"
fi

echo ""
echo "Next steps:"
echo "1. mv lambda_deployment.zip ../infra/terraform/"
echo "2. Update terraform.tfvars with current_league_id = \"1257436698095136768\""
echo "3. cd ../infra/terraform && terraform apply"
echo "4. Run historical backfill:"
echo "   aws lambda invoke --function-name ff-data-project-ingest \\"
echo "     --payload '{\"backfill_historical\": true}' response.json"
