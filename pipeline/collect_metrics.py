import argparse
import json
import subprocess
from pathlib import Path
import yaml
import numpy as np

from .compute_metrics_from_timeline import compute_metrics_from_timeline

ROOT = Path(__file__).resolve().parents[1]

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--algo", required=True, choices=["heft", "ga"])
    parser.add_argument("--env", required=True, choices=["E1", "E2", "E3"])
    args = parser.parse_args()

    sched_path = ROOT / f"schedule_{args.algo}_{args.env}.json"
    jobs_path = ROOT / f"jobs_{args.algo}_{args.env}.json"
    sched = json.loads(sched_path.read_text())
    jobs = json.loads(jobs_path.read_text())

    cfg_sched = yaml.safe_load((ROOT / "config" / "scheduler_config.yaml").read_text())
    cfg_env = yaml.safe_load((ROOT / "config" / "env_mapping.yaml").read_text())

    P = int(cfg_env["environments"][args.env]["num_cores"])
    power_active = cfg_sched["power_active_watt"]
    power_idle = cfg_sched["power_idle_watt"]
    price_per_core_hour = cfg_sched["price_per_core_hour"][args.env]
    # lambda_fail per core: array panjang P, semua sama
    lam_val = cfg_sched["lambda_fail"][args.env]
    lambda_fail = np.full(P, lam_val)

    # untuk sekarang, pakai start/finish dari scheduler (simulasi),
    # nanti bisa diganti runtime real dari sacct.
    assign = sched["assign"]
    start = sched["start"]
    finish = sched["finish"]

    makespan, energy, cost, R, load_balance = compute_metrics_from_timeline(
        assign, start, finish, P,
        power_active, power_idle,
        price_per_core_hour, lambda_fail
    )

    out = {
        "algo": args.algo,
        "env": args.env,
        "makespan": makespan,
        "energy": energy,
        "cost": cost,
        "reliability": R,
        "load_balance": load_balance,
    }
    out_path = ROOT / f"metrics_{args.algo}_{args.env}.json"
    out_path.write_text(json.dumps(out, indent=2))
    print(f"Metrik disimpan ke {out_path}")

if __name__ == "__main__":
    main()