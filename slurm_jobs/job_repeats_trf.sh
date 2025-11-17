#!/bin/bash
#SBATCH --job-name=trf
#SBATCH --output=logs/trf_%j.out
#SBATCH --error=logs/trf_%j.err
#SBATCH --cpus-per-task=1
#SBATCH --mem=4G
#SBATCH --time=01:00:00

source $(dirname "$0")/job_common_env.sh

TRF=/opt/bio/TRF/trf
IN=${RESULT_ROOT}/spades/contigs.fasta
OUT=${RESULT_ROOT}/repeats_trf

mkdir -p $OUT

$TRF $IN 2 7 7 80 10 50 500 -d -h
mv ${IN}.2.7.7.80.10.50.500.dat $OUT/