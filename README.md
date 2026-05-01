# Adaptive Delivery AI Simulator

An interactive web application built with **Streamlit** that visualizes and compares classic pathfinding algorithms on a randomly generated grid map. The simulation is themed as a delivery robot navigating terrain with various obstacles and terrain types.

---

## Overview

The simulator generates a grid map where a delivery agent must find a path from the **Start** position (top-left) to the **Goal** position (bottom-right). You can select different search algorithms and watch them explore the map in real time, then see the final path highlighted.

---

## Features

- **Random map generation** with configurable grid size (4×4 to 15×15)
- **Animated step-by-step visualization** of cell exploration and final path
- **Five algorithms** to compare:
  - Random Agent
  - Depth-First Search (DFS)
  - Breadth-First Search (BFS)
  - Dijkstra's Algorithm
  - A* Search
- **Image-based grid rendering** using custom icons for each terrain type
- **Result metrics** displayed after each run: success, steps, path length, unique cells visited, runtime, and total cost

---

## Terrain Types

| Symbol | Icon | Description | Traversal Cost |
|--------|------|-------------|----------------|
| `S` | 🟢 start.png | Start position | 1 |
| `G` | 🔴 goal.png | Goal position | 1 |
| `.` | _(white)_ | Open path | 1 |
| `#` | 🧱 wall.png | Wall — impassable | ∞ |
| `~` | 💧 water.png | Water — high cost | 10 |
| `X` | ⚠️ danger.png | Danger zone — very high cost | 20 |
| `o` | _(gray)_ | Visited cell | — |
| `*` | _(yellow)_ | Final path cell | — |

> **Note:** Random Agent, DFS, and BFS treat water (`~`) and danger (`X`) cells as impassable. Dijkstra and A* can traverse them at a higher cost, allowing them to find cost-optimal routes.

---

## Algorithms

### Random Agent
Moves to a randomly chosen valid neighbor at each step (up to 5,000 steps). Only traverses open cells.

### Depth-First Search (DFS)
Explores as deep as possible before backtracking. Finds *a* path but not necessarily the shortest one. Only traverses open cells.

### Breadth-First Search (BFS)
Explores all neighbors level by level. Guarantees the shortest path in terms of number of steps. Only traverses open cells.

### Dijkstra's Algorithm
Finds the minimum-cost path by considering terrain traversal costs. Can navigate through water and danger zones when they are on a cheaper overall route.

### A* Search
Uses Manhattan distance as a heuristic to guide the search toward the goal. Combines path cost (g-score) and estimated remaining cost (h-score) for efficient optimal pathfinding. Uses the same cost map as Dijkstra.

---

## Project Structure

```
compare_Algorithms/
├── for_streamlit.py          # Base version (text-based grid, no images)
├── for_streamlit_img_ver.py  # Image grid version (intermediate)
├── for_streamlit_img_ver2.py # Latest version (two-column layout with images)
├── before_streamlit.ipynb    # Prototype / development notebook
├── start.png                 # Icon for Start cell
├── goal.png                  # Icon for Goal cell
├── wall.png                  # Icon for Wall cell
├── water.png                 # Icon for Water cell
├── danger.png                # Icon for Danger cell
└── ppt.pdf                   # Project presentation slides
```

---

## Requirements

- Python 3.8+
- [Streamlit](https://streamlit.io/)
- pandas

Install dependencies:

```bash
pip install streamlit pandas
```

---

## How to Run

```bash
streamlit run for_streamlit_img_ver2.py
```

Then open the URL shown in the terminal (usually `http://localhost:8501`) in your browser.

1. Use the **Map Size** slider to choose the grid dimensions.
2. Select an **Algorithm** from the dropdown.
3. Click **Run** to generate a new map and watch the algorithm search for a path.

---

## How It Works

1. A grid is randomly generated. Each non-start/goal cell has a probability of becoming a wall (10%), water (40%), or danger zone (5%).
2. The selected algorithm searches for a path from `(0, 0)` to `(size-1, size-1)`.
3. The grid is rendered as an HTML component using base64-encoded images.
4. Cells are highlighted gray (`o`) as they are visited, then yellow (`*`) along the final path.
5. After the animation, result metrics are displayed below the grid.
