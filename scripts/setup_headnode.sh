#!/bin/bash
set -euo pipefail

# masuk ke root repo
cd "$(dirname "$0")/.."

python3 -m venv venv
source venv/bin/activate

pip install --upgrade pip
pip install -r requirements.txt

mkdir -p slurm_jobs/logs /scratch/raw /scratch/ref /scratch/results
echo "Head node setup selesai (venv + folder basic)."