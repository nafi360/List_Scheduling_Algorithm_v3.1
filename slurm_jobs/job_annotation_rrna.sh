#!/bin/bash
#SBATCH --job-name=annot_rrna
#SBATCH --output=logs/annot_rrna_%j.out
#SBATCH --error=logs/annot_rrna_%j.err
#SBATCH --cpus-per-task=1
#SBATCH --mem=4G
#SBATCH --time=01:00:00

source $(dirname "$0")/job_common_env.sh

RRNAMMER=/opt/bio/RNAmmer/rnammer
IN=${RESULT_ROOT}/spades/contigs.fasta
OUT=${RESULT_ROOT}/annotation_rrna

mkdir -p $OUT

$RRNAMMER -S bac -m tsu,lsu -gff ${OUT}/rrna.gff < $IN