#!/usr/bin/env python3
import sys
from collections import deque


# Function
def getMaze():
    maze = []
    while True:
        s = sys.stdin.readline().strip("\n")
        if s.startswith("#"):
            maze.append(list(s))
            # with open("output.txt", "a") as file:
            #     file.write(str(len(maze)))
            #     file.write(s)
        else:
            break
    return maze


def getPosition(maze, obj1, obj2=None):
    row_size = len(maze)
    col_size = len(maze[0])
    pos_list = []
    for x in range(row_size):
        for y in range(col_size):
            if maze[x][y] == obj1 or maze[x][y] == obj2:
                pos_list.append([x, y])
    return pos_list


def getMove(direction):
    if direction == "S":
        return "MOVE DOWN\n\n"
    elif direction == "N":
        return "MOVE UP\n\n"
    elif direction == "E":
        return "MOVE RIGHT\n\n"
    elif direction == "W":
        return "MOVE LEFT\n\n"


def maze2graph(maze):
    height = len(maze)
    width = len(maze[0]) if height else 0
    graph = {(i, j): [] for j in range(width)
             for i in range(height) if maze[i][j] != '#'}
    for row, col in graph.keys():
        if row < height - 1 and maze[row + 1][col] != '#':
            graph[(row, col)].append(("S", (row + 1, col)))
            graph[(row + 1, col)].append(("N", (row, col)))
        if col < width - 1 and maze[row][col + 1] != '#':
            graph[(row, col)].append(("E", (row, col + 1)))
            graph[(row, col + 1)].append(("W", (row, col)))
    return graph


def find_path_bfs(maze, start, goal, other_agent):
    start, goal = start, goal
    queue = deque([("", start)])
    visited = set()
    graph = maze2graph(maze)
    while queue:
        path, current = queue.popleft()
        if current == goal:
            return path
        if current in visited:
            continue
        x, y = current[0], current[1]
        if maze[x][y] in other_agent:
            continue
        visited.add(current)
        for direction, neighbour in graph[current]:
            queue.append((path + direction, neighbour))
    return "NO WAY!"


# Main loop
while True:
    s = sys.stdin.readline()
    if s == '':
        break
    if s.startswith("HELLO"):
        sys.stdout.write("I AM An\n\n")
    elif s.startswith("YOU ARE"):
        sys.stdout.write("OK\n\n")
        agent_name = s[8:9]
        all_agent = list("QWERTYUIOPASDFGHJKLZXCVBNM")
        all_agent.remove(agent_name)
        other_agent = all_agent
    elif s.startswith("MAZE"):
        maze = getMaze()
        des = getPosition(maze, "o", "!")
        agent_pos = getPosition(maze, agent_name)
        start = tuple(agent_pos[0])
        all_path = {}
        for pos in des:
            goal = tuple(pos)
            path = find_path_bfs(maze, start, goal, other_agent)
            all_path[len(path)] = path
        shortest_len = min(all_path.keys())
        shortest_path = all_path[shortest_len]
        next_pos = shortest_path[0:1]
        next_move = getMove(next_pos)
        # with open("output.txt", "a") as file:
        #     file.write(next_pos)
        sys.stdout.write(next_move)
