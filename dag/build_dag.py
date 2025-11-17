import json
import networkx as nx
from pathlib import Path

DAG_PATH = Path(__file__).parent / "workflow_dag.json"

# List task sesuai pipeline mitokondria
TASKS = [
    "trimmomatic",
    "spades",
    "quast",
    "annotation_trna",
    "annotation_rrna",
    "annotation_orf",
    "annotation_prepmt",
    "repeats_misa",
    "repeats_trf",
    "repeats_reputer",
    "plastid_mito_blast",
    "plastid_mito_circos",
    "phylo_alignment",
    "phylo_raxml",
]

def build_workflow_dag() -> nx.DiGraph:
    g = nx.DiGraph()

    for t in TASKS:
        g.add_node(t)

    # Edges kira-kira:
    g.add_edge("trimmomatic", "spades")
    g.add_edge("spades", "quast")

    for ann in ["annotation_trna", "annotation_rrna",
                "annotation_orf", "annotation_prepmt"]:
        g.add_edge("spades", ann)

    for rep in ["repeats_misa", "repeats_trf", "repeats_reputer"]:
        g.add_edge("spades", rep)

    g.add_edge("spades", "plastid_mito_blast")
    g.add_edge("plastid_mito_blast", "plastid_mito_circos")

    g.add_edge("spades", "phylo_alignment")
    g.add_edge("phylo_alignment", "phylo_raxml")

    return g

def save_dag_json(g: nx.DiGraph, path: Path) -> None:
    data = {
        "nodes": list(g.nodes()),
        "edges": [{"src": u, "dst": v} for u, v in g.edges()],
    }
    path.write_text(json.dumps(data, indent=2))

if __name__ == "__main__":
    dag = build_workflow_dag()
    save_dag_json(dag, DAG_PATH)
    print(f"DAG disimpan ke {DAG_PATH}")