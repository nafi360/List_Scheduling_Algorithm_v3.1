#!/bin/bash
#SBATCH --job-name=spades
#SBATCH --output=logs/spades_%j.out
#SBATCH --error=logs/spades_%j.err
#SBATCH --cpus-per-task=4
#SBATCH --mem=32G
#SBATCH --time=12:00:00

source $(dirname "$0")/job_common_env.sh

SPADES=/opt/bio/SPAdes/bin/spades.py
IN=${RESULT_ROOT}/trimmomatic
OUT=${RESULT_ROOT}/spades

mkdir -p $OUT

python "$SPADES" \
  -1 ${IN}/reads_1_paired.fq.gz \
  -2 ${IN}/reads_2_paired.fq.gz \
  -o $OUT