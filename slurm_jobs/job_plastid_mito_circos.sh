#!/bin/bash
#SBATCH --job-name=circos
#SBATCH --output=logs/circos_%j.out
#SBATCH --error=logs/circos_%j.err
#SBATCH --cpus-per-task=1
#SBATCH --mem=4G
#SBATCH --time=02:00:00

source $(dirname "$0")/job_common_env.sh

CIRCOS=/opt/bio/circos/bin/circos
IN=${RESULT_ROOT}/plastid_blast/blast_cp_vs_mt.txt
OUT=${RESULT_ROOT}/plastid_circos

mkdir -p $OUT

# butuh file konfigurasi Circos, ini placeholder
$CIRCOS -conf /opt/bio/circos/conf/circos.conf