import json
from pathlib import Path
import networkx as nx

def load_dag(path: Path) -> nx.DiGraph:
    data = json.loads(path.read_text())
    g = nx.DiGraph()
    for n in data["nodes"]:
        g.add_node(n)
    for e in data["edges"]:
        g.add_edge(e["src"], e["dst"])
    return g

def topo_order(g: nx.DiGraph):
    return list(nx.topological_sort(g))

def predecessors(g: nx.DiGraph, node):
    return list(g.predecessors(node))