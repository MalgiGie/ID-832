import os
import json
import networkx as nx
import matplotlib.pyplot as plt

from utils import *
from config import *

RELATIONS_FILE = os.path.join(ROOT_DIRECTORY, "npcs", "relations.json")
GRAPH_OUTPUT_FILE = os.path.join(ROOT_DIRECTORY, "npc_relations_graph.png")

RELATION_COLORS = {
    "Przyjaźń": "green",
    "Sojusz": "blue",
    "Rywalizacja": "orange",
    "Konflikt": "red",
    "Wrogość": "black",
    "Nienawiść": "darkred",
    "Zemsta": "purple",
    "Współpraca": "cyan",
    "Odmienne cele": "gray",
    "neutral": "gray"
}

RELATION_TRANSLATIONS = {
    "Friendship": "Przyjaźń",
    "Alliance": "Sojusz",
    "Rivalry": "Rywalizacja",
    "Conflict": "Konflikt",
    "Hostility": "Wrogość",
    "Hatred": "Nienawiść",
    "Revenge": "Zemsta",
    "Cooperation": "Współpraca",
    "Different goals": "Odmienne cele",
    "Neutral": "neutral",
    "neutral": "neutral"
}


def load_relations():
    if not os.path.exists(RELATIONS_FILE):
        print(f"File not found: {RELATIONS_FILE}")
        return []
    with open(RELATIONS_FILE, "r", encoding="utf-8") as f:
        return json.load(f)


def normalize_relation_type(rel_type: str) -> str:
    if not rel_type:
        return "neutral"
    rel_type = rel_type.strip()
    return RELATION_TRANSLATIONS.get(rel_type, rel_type)


def visualize(relations):
    if not relations:
        print("Relations not loaded")
        return

    G = nx.DiGraph()

    for rel in relations:
        npc_from = rel.get("from")
        npc_to = rel.get("to")
        relation_type = normalize_relation_type(rel.get("type", "neutral"))

        G.add_node(npc_from)
        G.add_node(npc_to)
        G.add_edge(npc_from, npc_to, type=relation_type)

    plt.figure(figsize=(18, 12))
    pos = nx.spring_layout(G, k=2.5, iterations=100, seed=42)
    nx.draw_networkx_nodes(G, pos, node_color="lightblue", node_size=2000)

    for rel_type, color in RELATION_COLORS.items():
        edges = [(u, v) for u, v, d in G.edges(data=True) if d["type"] == rel_type]
        if edges:
            nx.draw_networkx_edges(G, pos, edgelist=edges, edge_color=color, width=3, arrowsize=25)

    nx.draw_networkx_labels(
        G, pos, font_size=12, font_family="sans-serif",
        bbox=dict(facecolor="white", edgecolor="black", boxstyle="round,pad=0.3")
    )

    for rel_type, color in RELATION_COLORS.items():
        plt.plot([], [], color=color, label=rel_type, linewidth=3)
    plt.legend(title="Relation type", loc="upper left", fontsize=12)

    plt.title("NPC relations graph", fontsize=16)
    plt.axis("off")
    plt.tight_layout()

    plt.savefig(GRAPH_OUTPUT_FILE, dpi=300)
    print(f"Graph saved inside {GRAPH_OUTPUT_FILE}")
    plt.show(block=True)


def main():
    relations = load_relations()
    if not relations:
        print(f"No data found inside {RELATIONS_FILE}")
        return
    print(f"Loaded {len(relations)} relations. Creating graph...")
    visualize(relations)


if __name__ == "__main__":
    main()
