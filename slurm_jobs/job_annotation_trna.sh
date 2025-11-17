#!/bin/bash
#SBATCH --job-name=annot_trna
#SBATCH --output=logs/annot_trna_%j.out
#SBATCH --error=logs/annot_trna_%j.err
#SBATCH --cpus-per-task=1
#SBATCH --mem=4G
#SBATCH --time=01:00:00

source $(dirname "$0")/job_common_env.sh

TRNAS=/opt/bio/tRNAscan-SE/tRNAscan-SE
IN=${RESULT_ROOT}/spades/contigs.fasta
OUT=${RESULT_ROOT}/annotation_trna

mkdir -p $OUT

$TRNAS -o ${OUT}/trna.txt $IN