#!/bin/bash
#SBATCH --job-name=plastid_blast
#SBATCH --output=logs/plastid_blast_%j.out
#SBATCH --error=logs/plastid_blast_%j.err
#SBATCH --cpus-per-task=2
#SBATCH --mem=8G
#SBATCH --time=04:00:00

source $(dirname "$0")/job_common_env.sh

BLAST=/opt/bio/ncbi-blast+/bin/blastn
REF=${REF_ROOT}/chloroplast.fasta
IN=${RESULT_ROOT}/spades/contigs.fasta
OUT=${RESULT_ROOT}/plastid_blast

mkdir -p $OUT

$BLAST -query $REF -subject $IN -outfmt 6 \
  -out ${OUT}/blast_cp_vs_mt.txt -num_threads 2