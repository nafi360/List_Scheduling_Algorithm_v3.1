#!/bin/bash
#SBATCH --job-name=prepmt
#SBATCH --output=logs/prepmt_%j.out
#SBATCH --error=logs/prepmt_%j.err
#SBATCH --cpus-per-task=1
#SBATCH --mem=4G
#SBATCH --time=01:00:00

source $(dirname "$0")/job_common_env.sh

PREPMT=/opt/bio/PREP-Mt/prep_mt
IN=${RESULT_ROOT}/spades/contigs.fasta
OUT=${RESULT_ROOT}/annotation_prepmt

mkdir -p $OUT

$PREPMT -i $IN -o ${OUT}/prepmt_results.txt