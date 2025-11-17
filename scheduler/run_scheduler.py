import argparse
import json
import yaml
from pathlib import Path

from .dag_utils import load_dag
from .heft import heft_schedule
from .ga import ga_schedule

ROOT = Path(__file__).resolve().parents[1]

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--algo", choices=["heft", "ga"], required=True)
    parser.add_argument("--env", choices=["E1", "E2", "E3"], required=True)
    parser.add_argument("--seed", type=int, default=42)
    args = parser.parse_args()

    dag_path = ROOT / "dag" / "workflow_dag.json"
    profile_path = ROOT / "dag" / "task_profile.json"
    env_map_path = ROOT / "config" / "env_mapping.yaml"

    dag = load_dag(dag_path)
    task_profile = json.loads(profile_path.read_text())
    env_map = yaml.safe_load(env_map_path.read_text())
    env_cfg = env_map["environments"][args.env]
    P = int(env_cfg["num_cores"])

    if args.algo == "heft":
        assign, start, finish = heft_schedule(dag, task_profile, P)
    else:
        assign, start, finish = ga_schedule(dag, task_profile, P, seed=args.seed)

    out_path = ROOT / f"schedule_{args.algo}_{args.env}.json"
    out = {
        "algo": args.algo,
        "env": args.env,
        "num_cores": P,
        "assign": assign,
        "start": start,
        "finish": finish,
    }
    out_path.write_text(json.dumps(out, indent=2))
    print(f"Schedule disimpan ke {out_path}")

if __name__ == "__main__":
    main()