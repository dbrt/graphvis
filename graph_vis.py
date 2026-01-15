#!/usr/bin/env python3
"""Simple CLI graph visualizer.

Nodes are numbered 0..n-1. Edges are provided as a JSON-style 2D list: '[[0,1],[1,2]]'

Example:
    python3 graph_vis.py --n 4 --edges '[[0,1],[1,2],[2,3],[3,0]]'
    # or read edges from stdin:
    cat edges.json | python3 graph_vis.py --n 10 --edges - --out graph.png
"""
import argparse
import ast
import json
import sys


def parse_edges(text):
    """Parse edges from JSON or Python literal 2D list into a list of (u, v) integer tuples.

    Supported formats:
    - JSON array: [[0,1],[1,2]]
    - Python literal list: [[0,1],[1,2]]
    """
    text = (text or '').strip()
    if not text:
        return []

    # 1) Try JSON first
    try:
        data = json.loads(text)
        if isinstance(data, list):
            edges = []
            for item in data:
                if isinstance(item, (list, tuple)) and len(item) >= 2:
                    try:
                        edges.append((int(item[0]), int(item[1])))
                    except Exception:
                        continue
            return edges
    except Exception:
        pass

    # 2) Try Python literal
    try:
        data = ast.literal_eval(text)
        if isinstance(data, list):
            edges = []
            for item in data:
                if isinstance(item, (list, tuple)) and len(item) >= 2:
                    try:
                        edges.append((int(item[0]), int(item[1])))
                    except Exception:
                        continue
            return edges
    except Exception:
        pass

    # If not JSON or python literal, return empty list
    return []


def build_graph(n, edges):
    try:
        import networkx as nx
    except Exception:
        return None
    G = nx.Graph()
    G.add_nodes_from(range(n))
    # Only add edges that reference existing nodes to avoid creating extra nodes
    valid_edges = [(a, b) for (a, b) in edges if 0 <= a < n and 0 <= b < n]
    G.add_edges_from(valid_edges)
    return G


def draw_graph(G, out=None, layout='spring'):
    import matplotlib.pyplot as plt
    import networkx as nx

    if layout == 'circular':
        pos = nx.circular_layout(G)
    else:
        pos = nx.spring_layout(G)
    plt.figure(figsize=(6, 6))
    nx.draw(G, pos, with_labels=True, node_color='skyblue', edge_color='gray', node_size=600)
    if out:
        plt.savefig(out, bbox_inches='tight')
        print(f"Saved image to: {out}")
    else:
        plt.show()


def print_ascii(n, edges):
    adj = {i: [] for i in range(n)}
    for a, b in edges:
        if 0 <= a < n and 0 <= b < n:
            adj[a].append(b)
            adj[b].append(a)
    print("Adjacency list:")
    for i in range(n):
        print(f"{i}: {sorted(adj[i])}")


def main():
    p = argparse.ArgumentParser(description='Visualize small graphs (nodes 0..n-1).')
    p.add_argument('--n', type=int, required=True, help='Number of nodes (n)')
    p.add_argument('--edges', type=str, required=True, help="Edges as a JSON-style 2D list, e.g. '[[0,1],[1,2]]' (use '-' to read from stdin)")
    p.add_argument('--out', type=str, default=None, help='If provided, save visualization to this file (png, svg, etc.)')
    p.add_argument('--layout', choices=['spring', 'circular'], default='spring', help='Layout algorithm')
    args = p.parse_args()

    edges_text = args.edges
    if edges_text == '-':
        edges_text = sys.stdin.read()
    edges = parse_edges(edges_text)

    G = build_graph(args.n, edges)
    if G is None:
        print("Optional dependencies `networkx` and `matplotlib` not fully available.")
        print("Falling back to text adjacency output. To enable plotting, install: pip install -r requirements.txt")
        print_ascii(args.n, edges)
        return

    # Validate node ids and warn if some edges are out-of-range
    invalid = [e for e in edges if e[0] < 0 or e[1] < 0 or e[0] >= args.n or e[1] >= args.n]
    if invalid:
        print("Warning: some edges reference nodes outside 0..n-1 and will be ignored:", invalid, file=sys.stderr)

    draw_graph(G, out=args.out, layout=args.layout)


if __name__ == '__main__':
    main()
