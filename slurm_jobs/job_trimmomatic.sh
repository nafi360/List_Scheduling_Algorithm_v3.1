#!/bin/bash
#SBATCH --job-name=trimmomatic
#SBATCH --output=logs/trimmomatic_%j.out
#SBATCH --error=logs/trimmomatic_%j.err
#SBATCH --cpus-per-task=2
#SBATCH --mem=8G
#SBATCH --time=02:00:00

source $(dirname "$0")/job_common_env.sh

TRIM_JAR=/opt/bio/trimmomatic/trimmomatic.jar

mkdir -p ${RESULT_ROOT}/trimmomatic

java -jar "$TRIM_JAR" PE -threads 2 \
  ${RAW_ROOT}/reads_1.fq.gz \
  ${RAW_ROOT}/reads_2.fq.gz \
  ${RESULT_ROOT}/trimmomatic/reads_1_paired.fq.gz \
  ${RESULT_ROOT}/trimmomatic/reads_1_unpaired.fq.gz \
  ${RESULT_ROOT}/trimmomatic/reads_2_paired.fq.gz \
  ${RESULT_ROOT}/trimmomatic/reads_2_unpaired.fq.gz \
  SLIDINGWINDOW:4:20 MINLEN:50