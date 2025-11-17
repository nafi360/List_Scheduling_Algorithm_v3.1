#!/bin/bash
#SBATCH --job-name=raxml
#SBATCH --output=logs/raxml_%j.out
#SBATCH --error=logs/raxml_%j.err
#SBATCH --cpus-per-task=4
#SBATCH --mem=16G
#SBATCH --time=12:00:00

source $(dirname "$0")/job_common_env.sh

RAXML=/opt/bio/raxml/raxmlHPC-PTHREADS-SSE3
IN=${RESULT_ROOT}/phylo_alignment/alignment_trimmed.fasta
OUT=${RESULT_ROOT}/phylo_raxml

mkdir -p $OUT

$RAXML -T 4 \
  -s $IN \
  -n mito_tree \
  -m GTRGAMMA \
  -p 12345 \
  -x 12345 \
  -# 1000 \
  -w $OUT