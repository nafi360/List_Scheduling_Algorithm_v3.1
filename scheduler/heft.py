from typing import Dict, List, Tuple
import numpy as np
from .dag_utils import predecessors

def compute_upward_rank(g, task_profile: Dict[str, Dict]) -> Dict[str, float]:
    avg_comp = {t: task_profile[t]["base_runtime_s"] for t in g.nodes()}
    rank_u: Dict[str, float] = {}

    def rec(v: str) -> float:
        if v in rank_u:
            return rank_u[v]
        succ = list(g.successors(v))
        if not succ:
            rank_u[v] = avg_comp[v]
        else:
            rank_u[v] = avg_comp[v] + max(rec(s) for s in succ)
        return rank_u[v]

    for v in g.nodes():
        rec(v)
    return rank_u

def heft_schedule(g, task_profile: Dict[str, Dict], P: int) -> Tuple[Dict[str, int], Dict[str, float], Dict[str, float]]:
    rank_u = compute_upward_rank(g, task_profile)
    order = sorted(g.nodes(), key=lambda t: rank_u[t], reverse=True)

    avail_time_proc = np.zeros(P, dtype=float)
    start: Dict[str, float] = {}
    finish: Dict[str, float] = {}
    assign: Dict[str, int] = {}

    for t in order:
        best_p = None
        best_finish = None
        comp_time = float(task_profile[t]["base_runtime_s"])

        for p in range(P):
            ready_time = 0.0
            for pred in predecessors(g, t):
                # komunikasi diabaikan (lokal), pakai finish pred
                ready_time = max(ready_time, finish[pred])
            est_start = max(ready_time, avail_time_proc[p])
            est_finish = est_start + comp_time
            if best_finish is None or est_finish < best_finish:
                best_finish = est_finish
                best_p = p

        assign[t] = int(best_p)
        start[t] = float(best_finish - comp_time)
        finish[t] = float(best_finish)
        avail_time_proc[best_p] = best_finish

    return assign, start, finish