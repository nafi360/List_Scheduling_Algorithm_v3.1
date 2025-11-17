import argparse
import json
import subprocess
from pathlib import Path
import yaml

ROOT = Path(__file__).resolve().parents[1]

TASK_TO_JOB = {
    "trimmomatic": "job_trimmomatic.sh",
    "spades": "job_spades.sh",
    "quast": "job_quast.sh",
    "annotation_trna": "job_annotation_trna.sh",
    "annotation_rrna": "job_annotation_rrna.sh",
    "annotation_orf": "job_annotation_orf.sh",
    "annotation_prepmt": "job_annotation_prepmt.sh",
    "repeats_misa": "job_repeats_misa.sh",
    "repeats_trf": "job_repeats_trf.sh",
    "repeats_reputer": "job_repeats_reputer.sh",
    "plastid_mito_blast": "job_plastid_mito_blast.sh",
    "plastid_mito_circos": "job_plastid_mito_circos.sh",
    "phylo_alignment": "job_phylo_alignment.sh",
    "phylo_raxml": "job_phylo_raxml.sh",
}

def sbatch(job_script, partition, constraint, dependency_jobid=None):
    cmd = ["sbatch", "-p", partition, "--constraint", constraint, job_script]
    if dependency_jobid:
        cmd = ["sbatch", f"--dependency=afterok:{dependency_jobid}"] + cmd[1:]
    print(" ".join(cmd))
    out = subprocess.check_output(cmd).decode().strip()
    # format: Submitted batch job 12345
    jobid = out.split()[-1]
    return jobid

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--algo", required=True, choices=["heft", "ga"])
    parser.add_argument("--env", required=True, choices=["E1", "E2", "E3"])
    args = parser.parse_args()

    sched_path = ROOT / f"schedule_{args.algo}_{args.env}.json"
    env_map_path = ROOT / "config" / "env_mapping.yaml"
    dag_path = ROOT / "dag" / "workflow_dag.json"

    schedule = json.loads(sched_path.read_text())
    dag = json.loads(dag_path.read_text())
    env_map = yaml.safe_load(env_map_path.read_text())
    env_cfg = env_map["environments"][args.env]

    partition = env_cfg["slurm_partition"]
    constraint = env_cfg["slurm_constraint"]

    # build adjacency & indegree for dependency sbatch
    preds = {n: [] for n in dag["nodes"]}
    succs = {n: [] for n in dag["nodes"]}
    for e in dag["edges"]:
        preds[e["dst"]].append(e["src"])
        succs[e["src"]].append(e["dst"])

    jobids = {}

    # simple topological scheduling based on schedule["start"]
    tasks_ordered = sorted(schedule["start"].keys(),
                           key=lambda t: schedule["start"][t])

    for t in tasks_ordered:
        job_script = ROOT / "slurm_jobs" / TASK_TO_JOB[t]
        deps = [jobids[p] for p in preds[t] if p in jobids]
        dep_id = deps[-1] if deps else None
        jid = sbatch(str(job_script), partition, constraint, dep_id)
        jobids[t] = jid

    out_path = ROOT / f"jobs_{args.algo}_{args.env}.json"
    out_path.write_text(json.dumps(jobids, indent=2))
    print(f"Job IDs disimpan ke {out_path}")

if __name__ == "__main__":
    main()