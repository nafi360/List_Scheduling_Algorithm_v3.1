#!/bin/bash
#SBATCH --job-name=misa
#SBATCH --output=logs/misa_%j.out
#SBATCH --error=logs/misa_%j.err
#SBATCH --cpus-per-task=1
#SBATCH --mem=4G
#SBATCH --time=01:00:00

source $(dirname "$0")/job_common_env.sh

MISA=/opt/bio/MISA/misa.pl
IN=${RESULT_ROOT}/spades/contigs.fasta
OUT=${RESULT_ROOT}/repeats_misa

mkdir -p $OUT

cp $IN ${OUT}/input.fasta
perl $MISA ${OUT}/input.fasta