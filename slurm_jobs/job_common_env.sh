#!/bin/bash

module load python
module load gcc
module load java

export SCRATCH_ROOT=/scratch
export RAW_ROOT=${SCRATCH_ROOT}/raw
export REF_ROOT=${SCRATCH_ROOT}/ref
export RESULT_ROOT=${SCRATCH_ROOT}/results

mkdir -p "$RESULT_ROOT"
mkdir -p "$(dirname "$0")/logs"