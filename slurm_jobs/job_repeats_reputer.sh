#!/bin/bash
#SBATCH --job-name=reputer
#SBATCH --output=logs/reputer_%j.out
#SBATCH --error=logs/reputer_%j.err
#SBATCH --cpus-per-task=1
#SBATCH --mem=4G
#SBATCH --time=02:00:00

source $(dirname "$0")/job_common_env.sh

REPUTER=/opt/bio/REPuter/reputer
IN=${RESULT_ROOT}/spades/contigs.fasta
OUT=${RESULT_ROOT}/repeats_reputer

mkdir -p $OUT

$REPUTER -o $OUT -f $IN -c forward