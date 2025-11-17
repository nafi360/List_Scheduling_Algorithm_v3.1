#!/bin/bash
set -euo pipefail

BUCKET=$1  # misal: s3://my-mito-bucket
RESULT_PREFIX=${2:-results}

SCRATCH_ROOT=/scratch
aws s3 sync "${SCRATCH_ROOT}/results" "${BUCKET}/${RESULT_PREFIX}"