#!/bin/bash
#SBATCH --job-name=annot_orf
#SBATCH --output=logs/annot_orf_%j.out
#SBATCH --error=logs/annot_orf_%j.err
#SBATCH --cpus-per-task=2
#SBATCH --mem=4G
#SBATCH --time=02:00:00

source $(dirname "$0")/job_common_env.sh

ORFFINDER=/opt/bio/ORFfinder/orffinder
BLAST=/opt/bio/ncbi-blast+/bin/blastn
IN=${RESULT_ROOT}/spades/contigs.fasta
OUT=${RESULT_ROOT}/annotation_orf

mkdir -p $OUT

$ORFFINDER -in $IN -out ${OUT}/orf.fasta
$BLAST -query ${OUT}/orf.fasta -db nt \
  -out ${OUT}/blast_orf.txt -outfmt 6 -max_hsps 1 -num_threads 2