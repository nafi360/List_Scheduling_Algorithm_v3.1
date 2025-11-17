# Desain Eksperimen HEFT vs GA + ParallelCluster + Pipeline Mitokondria

## Lingkungan Eksperimen

- **E1**: 2 vCPU (env2vcpu, instance c5.large)
- **E2**: 4 vCPU (env4vcpu, instance c5.xlarge)
- **E3**: 8 vCPU (env8vcpu, instance c5.2xlarge)

## Variabel yang Diukur

- Makespan (detik)
- Konsumsi energi (Joule)
- Biaya komputasi (USD)
- Reliabilitas eksekusi
- Load balancing (std dev active time per core)

## Alur Singkat

1. Generate DAG workflow mitokondria (`dag/build_dag.py`).
2. Generate profil tugas (`dag/task_profile.py`).
3. Jalankan scheduler HEFT & GA (`scheduler/run_scheduler.py`) untuk tiap environment.
4. Submit pipeline ke Slurm (`pipeline/submit_pipeline.py`).
5. Kumpulkan metrik (`pipeline/collect_metrics.py`).
6. Rekap hasil menjadi CSV (`pipeline/experiment_matrix.py`).