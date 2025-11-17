#!/bin/bash
#SBATCH --job-name=phylo_align
#SBATCH --output=logs/phylo_align_%j.out
#SBATCH --error=logs/phylo_align_%j.err
#SBATCH --cpus-per-task=4
#SBATCH --mem=8G
#SBATCH --time=03:00:00

source $(dirname "$0")/job_common_env.sh

MAFFT=/opt/bio/mafft/mafft
TRIMAL=/opt/bio/trimal/trimal
IN=${RESULT_ROOT}/spades/contigs.fasta
OUT=${RESULT_ROOT}/phylo_alignment

mkdir -p $OUT

$MAFFT --thread 4 $IN > ${OUT}/alignment.fasta
$TRIMAL -in ${OUT}/alignment.fasta -out ${OUT}/alignment_trimmed.fasta -automated1