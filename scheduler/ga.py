from typing import Dict, Tuple, List
import random
import numpy as np
from .dag_utils import predecessors

def _schedule_from_order(g, task_profile, order: List[str], P: int):
    avail_time_proc = np.zeros(P, dtype=float)
    start = {}
    finish = {}
    assign = {}

    # enforce dependensi: hanya boleh dijadwalkan kalau semua pred sudah dijadwalkan
    unscheduled = set(order)
    ready = [t for t in order if len(predecessors(g, t)) == 0]

    while ready:
        t = ready.pop(0)  # ambil depan
        comp_time = float(task_profile[t]["base_runtime_s"])
        best_p = None
        best_finish = None

        for p in range(P):
            ready_time = 0.0
            for pred in predecessors(g, t):
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

        unscheduled.remove(t)
        # cek task lain yang sekarang semua pred-nya sudah selesai
        for u in list(unscheduled):
            if all(pred in finish for pred in predecessors(g, u)) and u not in ready:
                ready.append(u)

    makespan = max(finish.values())
    return makespan, assign, start, finish

def ga_schedule(g, task_profile, P: int,
                pop_size: int = 20,
                n_gen: int = 30,
                cx_rate: float = 0.8,
                mut_rate: float = 0.2,
                seed: int | None = None) -> Tuple[Dict[str, int], Dict[str, float], Dict[str, float]]:
    if seed is not None:
        random.seed(seed)

    tasks = list(g.nodes())

    def random_individual():
        ind = tasks[:]
        random.shuffle(ind)
        return ind

    def crossover(p1, p2):
        a, b = sorted(random.sample(range(len(tasks)), 2))
        hole = p1[a:b]
        rest = [t for t in p2 if t not in hole]
        return rest[:a] + hole + rest[a:]

    def mutate(ind):
        i, j = random.sample(range(len(tasks)), 2)
        ind[i], ind[j] = ind[j], ind[i]

    # init population
    population = [random_individual() for _ in range(pop_size)]

    def fitness(ind):
        makespan, *_ = _schedule_from_order(g, task_profile, ind, P)
        return makespan

    for _ in range(n_gen):
        # evaluate
        scored = [(fitness(ind), ind) for ind in population]
        scored.sort(key=lambda x: x[0])
        population = [ind for _, ind in scored]

        new_pop = population[:2]  # elitism

        while len(new_pop) < pop_size:
            p1, p2 = random.sample(population[:10], 2)
            child = p1[:]
            if random.random() < cx_rate:
                child = crossover(p1, p2)
            if random.random() < mut_rate:
                mutate(child)
            new_pop.append(child)

        population = new_pop

    best_ind = min(population, key=fitness)
    _, assign, start, finish = _schedule_from_order(g, task_profile, best_ind, P)
    return assign, start, finish