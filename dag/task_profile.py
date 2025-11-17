import json
from pathlib import Path

PROFILE_PATH = Path(__file__).parent / "task_profile.json"

# Estimasi kasar runtime (detik) dan kebutuhan core per task.
# Nanti bisa diupdate pakai hasil real runtime dari Slurm.
PROFILE = {
    "trimmomatic":       {"base_runtime_s": 600,  "cores": 2},
    "spades":            {"base_runtime_s": 3600, "cores": 4},
    "quast":             {"base_runtime_s": 900,  "cores": 2},
    "annotation_trna":   {"base_runtime_s": 600,  "cores": 1},
    "annotation_rrna":   {"base_runtime_s": 600,  "cores": 1},
    "annotation_orf":    {"base_runtime_s": 900,  "cores": 2},
    "annotation_prepmt": {"base_runtime_s": 600,  "cores": 1},
    "repeats_misa":      {"base_runtime_s": 600,  "cores": 1},
    "repeats_trf":       {"base_runtime_s": 600,  "cores": 1},
    "repeats_reputer":   {"base_runtime_s": 600,  "cores": 1},
    "plastid_mito_blast":{"base_runtime_s": 1200, "cores": 2},
    "plastid_mito_circos":{"base_runtime_s": 900, "cores": 1},
    "phylo_alignment":   {"base_runtime_s": 1800, "cores": 4},
    "phylo_raxml":       {"base_runtime_s": 3600, "cores": 4},
}

if __name__ == "__main__":
    PROFILE_PATH.write_text(json.dumps(PROFILE, indent=2))
    print(f"Task profile disimpan ke {PROFILE_PATH}")