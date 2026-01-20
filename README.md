Graph Visualizer (CLI)

A small Python command-line tool to visualize simple undirected graphs whose nodes are numbered 0..n-1.

Files
- [graph_vis.py](graph_vis.py): The CLI script.
- [requirements.txt](requirements.txt): Optional dependencies (`networkx`, `matplotlib`).

Install

Create a virtualenv and install dependencies (optional, needed for plotting):

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

Usage

Edges (simple JSON-style 2D list)

The tool now accepts a JSON-style 2D integer array for edges. Example:

```bash
python3 graph_vis.py --n 10 --edges '[[4,5],[1,6],[6,4],[5,3],[3,6],[0,2],[5,8],[0,6],[3,0],[6,8],[2,8],[1,2],[9,4]]'
```

To read the edge list from stdin, pass `-` for `--edges` and pipe the content in:

```bash
cat edges.json | python3 graph_vis.py --n 10 --edges - --out graph.png
```

If `matplotlib` or `networkx` are not available, the script prints an adjacency list fallback.

Notes
- Nodes are always created 0..n-1. Edges referencing out-of-range nodes are ignored with a warning.
- You can save the visualization to a file with `--out`.
 - If your edge list uses 1-based node indices (1..n) instead of 0-based (0..n-1), pass the `--offbyone` flag and the tool will shift indices automatically.
