from pathlib import Path
import csv
import networkx as nx
import matplotlib.pyplot as plt

ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data" / "source-use.csv"
OUTPUT = ROOT / "figures" / "citation-network.svg"


def load_edges(path):
    edges = []

    with path.open(encoding="utf-8-sig", newline="") as f:
        for row in csv.DictReader(f):
            if not row["source_id"]:
                continue

            edges.append({
                "source_id": row["source_id"],
                "source_name": row["source_name"],
                "source_date": row["source_date"],
                "user_id": row["user_id"],
                "user_name": row["user_name"],
                "user_date": row["user_date"],
                "relationship": row["relationship"],
                "source_kind": row["source_kind"],
                "strength": row["strength"],
            })

    return edges


def build_graph(edges):
    graph = nx.DiGraph()

    for edge in edges:

        # Earlier source / evidence
        graph.add_node(
            edge["source_id"],
            label=edge["source_name"],
            date=edge["source_date"],
            role="source"
        )

        # Later interpreter / author
        graph.add_node(
            edge["user_id"],
            label=edge["user_name"],
            date=edge["user_date"],
            role="user"
        )

        # Arrow direction = source -> later user/interpreter
        graph.add_edge(
            edge["source_id"],
            edge["user_id"],
            relationship=edge["relationship"],
            strength=edge["strength"]
        )

    return graph


def draw_graph(graph, output_path):
    output_path.parent.mkdir(parents=True, exist_ok=True)

    plt.figure(figsize=(16, 11))

    # Deterministic layout so successive renders are comparable.
    pos = nx.spring_layout(
        graph,
        seed=42,
        k=1.5
    )

    labels = {}

    for node, data in graph.nodes(data=True):
        name = data.get("label", node)
        date = data.get("date", "")

        if date:
            labels[node] = f"{name}\n({date})"
        else:
            labels[node] = name

    nx.draw_networkx_nodes(
        graph,
        pos,
        node_size=3000,
        alpha=0.9
    )

    nx.draw_networkx_edges(
        graph,
        pos,
        arrows=True,
        arrowsize=18,
        width=1.3,
        alpha=0.65,
        connectionstyle="arc3,rad=0.06"
    )

    nx.draw_networkx_labels(
        graph,
        pos,
        labels=labels,
        font_size=8
    )

    plt.title(
        "Hölderlin Psychiatric Interpretation: Source-Use Genealogy\n"
        "Arrows run from earlier source/evidence to later interpreter"
    )

    plt.axis("off")
    plt.tight_layout()

    plt.savefig(
        output_path,
        format="svg",
        bbox_inches="tight"
    )

    plt.close()


def main():
    edges = load_edges(DATA)
    graph = build_graph(edges)
    draw_graph(graph, OUTPUT)

    print(f"Loaded {len(edges)} linked source-use relationships.")
    print(
        f"Graph contains {graph.number_of_nodes()} nodes "
        f"and {graph.number_of_edges()} edges."
    )
    print(f"Wrote: {OUTPUT}")


if __name__ == "__main__":
    main()