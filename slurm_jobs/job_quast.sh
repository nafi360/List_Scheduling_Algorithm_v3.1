#!/bin/bash
#SBATCH --job-name=quast
#SBATCH --output=logs/quast_%j.out
#SBATCH --error=logs/quast_%j.err
#SBATCH --cpus-per-task=2
#SBATCH --mem=8G
#SBATCH --time=03:00:00

source $(dirname "$0")/job_common_env.sh

QUAST=/opt/bio/quast/quast.py
IN=${RESULT_ROOT}/spades/contigs.fasta
OUT=${RESULT_ROOT}/quast

mkdir -p $OUT

python $QUAST $IN -o $OUT