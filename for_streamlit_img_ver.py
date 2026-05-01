import random
import time
import heapq
from collections import deque

import pandas as pd
import streamlit as st

import base64
import streamlit.components.v1 as components

st.set_page_config(layout="wide")


def create_grid(size):
    grid = [["." for _ in range(size)] for _ in range(size)]

    grid[0][0] = "S"
    grid[size - 1][size - 1] = "G"

    for i in range(size):
        for j in range(size):
            if grid[i][j] == ".":
                r = random.random()

                if r < 0.1:
                    grid[i][j] = "#"
                elif r < 0.15:
                    grid[i][j] = "~"
                elif r < 0.2:
                    grid[i][j] = "X"

    return grid


# def color_grid(val):
#     if val == "S":
#         return "background-color: lightgreen"
#     elif val == "G":
#         return "background-color: lightcoral"
#     elif val == "#":
#         return "background-color: black; color: white"
#     elif val == "~":
#         return "background-color: lightblue"
#     elif val == "X":
#         return "background-color: orange"
#     elif val == "o":
#         return "background-color: lightgray"
#     elif val == "*":
#         return "background-color: yellow"
#     return ""


# def show_grid(grid, placeholder=None):
#     df = pd.DataFrame(grid)
#     styled = df.style.map(color_grid)

#     if placeholder:
#         placeholder.dataframe(styled, hide_index=True)
#     else:
#         st.dataframe(styled, hide_index=True)

def get_base64_image(path):
    with open(path, "rb") as f:
        return base64.b64encode(f.read()).decode()


def render_grid_with_images(grid):
    img_map = {
        "S": "start.png",
        "G": "goal.png",
        "#": "wall.png",
        "~": "water.png",
        "X": "danger.png"
    }

    color_map = {
        ".": "white",
        "o": "lightgray",
        "*": "yellow"
    }

    html = "<div style='display:inline-block;'>"

    for row in grid:
        html += "<div style='display:flex;'>"

        for cell in row:
            if cell in img_map:
                img_base64 = get_base64_image(img_map[cell])

                html += f"""
                <div style="width:40px; height:40px; border:1px solid #ddd;
                            display:flex; align-items:center; justify-content:center;">
                    <img src="data:image/png;base64,{img_base64}" width="28">
                </div>
                """
            else:
                color = color_map.get(cell, "white")

                html += f"""
                <div style="width:40px; height:40px; border:1px solid #ddd;
                            background-color:{color};">
                </div>
                """

        html += "</div>"

    html += "</div>"
    return html


def show_grid(grid, placeholder=None):
    html = render_grid_with_images(grid)
    height = len(grid) * 45 + 20

    if placeholder:
        with placeholder.container():
            components.html(html, height=height, scrolling=False)
    else:
        components.html(html, height=height, scrolling=False)


def animate_search(grid, visited_order, path):
    placeholder = st.empty()
    temp_grid = [row[:] for row in grid]

    for r, c in visited_order:
        if temp_grid[r][c] not in ["S", "G"]:
            temp_grid[r][c] = "o"

        show_grid(temp_grid, placeholder)
        time.sleep(0.15)

    if path:
        for r, c in path:
            if temp_grid[r][c] not in ["S", "G"]:
                temp_grid[r][c] = "*"

            show_grid(temp_grid, placeholder)
            time.sleep(0.15)


def show_result(success, steps, path, runtime, cost=None):
    st.subheader("Result")

    st.write(f"Success: {success}")
    st.write(f"Steps: {steps}")
    st.write(f"Path Length: {len(path) - 1 if path else 0}")
    st.write(f"Unique Cells Visited: {len(set(path)) if path else 0}")
    st.write(f"Runtime: {round(runtime, 4)} seconds")

    if cost is not None:
        st.write(f"Total Cost: {cost}")


def lets_moves(grid, pos, block_all=True):
    row, col = pos
    moves = []

    directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]

    for dr, dc in directions:
        nr = row + dr
        nc = col + dc

        if 0 <= nr < len(grid) and 0 <= nc < len(grid[0]):
            cell = grid[nr][nc]

            if block_all:
                if cell not in ["#", "~", "X"]:
                    moves.append((nr, nc))
            else:
                if cell != "#":
                    moves.append((nr, nc))

    return moves


def random_agent(grid):
    start = (0, 0)
    goal = (len(grid) - 1, len(grid[0]) - 1)

    pos = start
    path = [pos]
    steps = 0

    while pos != goal and steps < 5000:
        moves = lets_moves(grid, pos)

        if not moves:
            break

        pos = random.choice(moves)
        path.append(pos)
        steps += 1

    return path, path, steps, pos == goal


def bfs(grid):
    start = (0, 0)
    goal = (len(grid) - 1, len(grid[0]) - 1)

    queue = deque([start])
    visited = {start}
    visited_order = [start]
    parent = {}

    while queue:
        current = queue.popleft()

        if current == goal:
            break

        for nxt in lets_moves(grid, current):
            if nxt not in visited:
                visited.add(nxt)
                visited_order.append(nxt)
                parent[nxt] = current
                queue.append(nxt)

    if goal not in visited:
        return None, visited_order

    path = []
    cur = goal

    while cur != start:
        path.append(cur)
        cur = parent[cur]

    path.append(start)
    path.reverse()

    return path, visited_order


def dfs(grid):
    start = (0, 0)
    goal = (len(grid) - 1, len(grid[0]) - 1)

    stack = [start]
    visited = {start}
    visited_order = [start]
    parent = {}

    while stack:
        current = stack.pop()

        if current == goal:
            break

        for nxt in lets_moves(grid, current):
            if nxt not in visited:
                visited.add(nxt)
                visited_order.append(nxt)
                parent[nxt] = current
                stack.append(nxt)

    if goal not in visited:
        return None, visited_order

    path = []
    cur = goal

    while cur != start:
        path.append(cur)
        cur = parent[cur]

    path.append(start)
    path.reverse()

    return path, visited_order


def dijkstra(grid):
    start = (0, 0)
    goal = (len(grid) - 1, len(grid[0]) - 1)

    cost_map = {
        ".": 1, "S": 1, "G": 1,
        "~": 3, "X": 5,
        "#": float("inf")
    }

    pq = [(0, start)]
    dist = {start: 0}
    parent = {}
    visited = set()
    visited_order = []

    while pq:
        cost, current = heapq.heappop(pq)

        if current in visited:
            continue

        visited.add(current)
        visited_order.append(current)

        if current == goal:
            break

        for nxt in lets_moves(grid, current, block_all=False):
            r, c = nxt
            new_cost = cost + cost_map[grid[r][c]]

            if nxt not in dist or new_cost < dist[nxt]:
                dist[nxt] = new_cost
                parent[nxt] = current
                heapq.heappush(pq, (new_cost, nxt))

    if goal not in dist:
        return None, visited_order, None

    path = []
    cur = goal

    while cur != start:
        path.append(cur)
        cur = parent[cur]

    path.append(start)
    path.reverse()

    return path, visited_order, dist[goal]


def heuristic(pos, goal):
    return abs(pos[0] - goal[0]) + abs(pos[1] - goal[1])


def astar(grid):
    start = (0, 0)
    goal = (len(grid) - 1, len(grid[0]) - 1)

    cost_map = {
        ".": 1, "S": 1, "G": 1,
        "~": 3, "X": 5,
        "#": float("inf")
    }

    pq = [(0, start)]
    g_score = {start: 0}
    parent = {}
    visited = set()
    visited_order = []

    while pq:
        _, current = heapq.heappop(pq)

        if current in visited:
            continue

        visited.add(current)
        visited_order.append(current)

        if current == goal:
            break

        for nxt in lets_moves(grid, current, block_all=False):
            r, c = nxt
            new_g = g_score[current] + cost_map[grid[r][c]]

            if nxt not in g_score or new_g < g_score[nxt]:
                g_score[nxt] = new_g
                parent[nxt] = current
                f_score = new_g + heuristic(nxt, goal)
                heapq.heappush(pq, (f_score, nxt))

    if goal not in g_score:
        return None, visited_order, None

    path = []
    cur = goal

    while cur != start:
        path.append(cur)
        cur = parent[cur]

    path.append(start)
    path.reverse()

    return path, visited_order, g_score[goal]


# UI
st.title("Adaptive Delivery AI Simulator")

size = st.slider("Map Size", 4, 15, 8)
algo = st.selectbox("Algorithm", ["Random", "DFS", "BFS", "Dijkstra", "A*"])

if st.button("Run"):
    grid = create_grid(size)

    if algo == "Random":
        t = time.time()
        path, visited, steps, success = random_agent(grid)
        runtime = time.time() - t

        animate_search(grid, visited, path)
        show_result(success, steps, path, runtime)

    elif algo == "DFS":
        t = time.time()
        path, visited = dfs(grid)
        runtime = time.time() - t

        animate_search(grid, visited, path)
        show_result(path is not None, len(path)-1 if path else 0, path, runtime)

    elif algo == "BFS":
        t = time.time()
        path, visited = bfs(grid)
        runtime = time.time() - t

        animate_search(grid, visited, path)
        show_result(path is not None, len(path)-1 if path else 0, path, runtime)

        elif algo == "Dijkstra":
        t = time.time()
        path, visited, cost = dijkstra(grid)
        runtime = time.time() - t

        animate_search(grid, visited, path)
        show_result(path is not None, len(path)-1 if path else 0, path, runtime, cost)

    elif algo == "A*":
        t = time.time()
        path, visited, cost = astar(grid)
        runtime = time.time() - t

        animate_search(grid, visited, path)
        show_result(path is not None, len(path)-1 if path else 0, path, runtime, cost)