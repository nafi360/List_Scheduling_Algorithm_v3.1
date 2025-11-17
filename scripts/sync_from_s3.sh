#!/bin/bash
set -euo pipefail

BUCKET=$1  # misal: s3://my-mito-bucket

RAW_PREFIX=${2:-raw}
REF_PREFIX=${3:-ref}

SCRATCH_ROOT=/scratch
mkdir -p ${SCRATCH_ROOT}/raw ${SCRATCH_ROOT}/ref

aws s3 sync "${BUCKET}/${RAW_PREFIX}" "${SCRATCH_ROOT}/raw"
aws s3 sync "${BUCKET}/${REF_PREFIX}" "${SCRATCH_ROOT}/ref"