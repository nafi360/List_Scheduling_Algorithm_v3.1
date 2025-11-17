# aws-mito-heft-ga

Eksperimen perbandingan algoritma penjadwalan **HEFT vs GA** pada pipeline analisis DNA mitokondria yang dijalankan di **AWS ParallelCluster (Slurm)**.

Fokus:
- Workflow biologis: trimming → assembly → evaluasi → anotasi → repeat → plastid-mito transfer → filogeni.
- Workflow komputasi: mapping DAG → penjadwalan HEFT/GA → submit ke Slurm → ambil metrik (makespan, energi, biaya, reliabilitas, load balancing).
- Lingkungan eksperimen: E1 (2 vCPU), E2 (4 vCPU), E3 (8 vCPU).

## Struktur Repo (ringkas)

Lihat komentar di tiap file dalam repo:
- `config/`    → config ParallelCluster, tools bioinfo, parameter metrik, mapping environment.
- `dag/`       → generate DAG workflow & profil tugas.
- `scheduler/` → implementasi HEFT & GA, plus helper DAG.
- `pipeline/`  → glue antara scheduler ↔ Slurm ↔ metrik eksperimen.
- `slurm_jobs/`→ script sbatch per tahap pipeline mitokondria.
- `scripts/`   → sync S3 dan setup head node.
- `docs/`      → diagram & desain eksperimen (buat skripsi).

## Quick start (di head node ParallelCluster)

```bash
# 1. clone repo
git clone https://github.com/USERNAME/aws-mito-heft-ga.git
cd aws-mito-heft-ga

# 2. setup environment
bash scripts/setup_headnode.sh

# 3. generate DAG & task profile
python dag/build_dag.py
python dag/task_profile.py

# 4. jalankan scheduler (HEFT/GA) untuk environment tertentu
python scheduler/run_scheduler.py --algo heft --env E1
python scheduler/run_scheduler.py --algo ga --env E1

# 5. submit pipeline ke Slurm
python pipeline/submit_pipeline.py --algo heft --env E1
python pipeline/submit_pipeline.py --algo ga --env E1

# 6. collect metrik & simpan ke CSV
python pipeline/experiment_matrix.py
