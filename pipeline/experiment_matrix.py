from pathlib import Path
import json
import subprocess
import pandas as pd

ROOT = Path(__file__).resolve().parents[1]

ALGOS = ["heft", "ga"]
ENVS = ["E1", "E2", "E3"]

def run_cmd(cmd):
    print(" ".join(cmd))
    subprocess.check_call(cmd)

def main():
    rows = []

    for env in ENVS:
        for algo in ALGOS:
            # 1. run scheduler
            run_cmd(["python", str(ROOT / "scheduler" / "run_scheduler.py"),
                     "--algo", algo, "--env", env])

            # 2. submit pipeline
            run_cmd(["python", str(ROOT / "pipeline" / "submit_pipeline.py"),
                     "--algo", algo, "--env", env])

            # 3. collect metrics (simulasi / real tergantung implementasi)
            run_cmd(["python", str(ROOT / "pipeline" / "collect_metrics.py"),
                     "--algo", algo, "--env", env])

            metrics_path = ROOT / f"metrics_{algo}_{env}.json"
            metrics = json.loads(metrics_path.read_text())
            rows.append(metrics)

    df = pd.DataFrame(rows)
    out_csv = ROOT / "experiment_results.csv"
    df.to_csv(out_csv, index=False)
    print(f"Matrix eksperimen disimpan ke {out_csv}")

if __name__ == "__main__":
    main()