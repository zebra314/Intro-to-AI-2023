#!/usr/bin/env python
# coding: utf-8

# Don't change this part.
# For load graph information and show map
import folium
import pickle
def load_path_graph(path):
    with open('graph.pkl', 'rb') as f:
        graph = pickle.load(f)

    node_pairs = list(zip(path[:-1], path[1:]))
    lines = []
    for edge in graph:
        if (edge['u'], edge['v']) in node_pairs or  (edge['v'], edge['u']) in node_pairs:
            lines.append(edge['geometry'])
    return lines

# Part 1~4 and 6
# You can wirte in new .py files and import it.
# ex: from astar import astar
from bfs import bfs
from dfs_stack import dfs
from ucs import ucs
from astar import astar
from astar_time import astar_time

# Part 5
# Change start ID and end ID.
start = 2270143902
end = 1079387396

# Don't change this part.
# Show the result of BFS
bfs_path, bfs_dist, bfs_visited = bfs(start, end)
print(f'The number of nodes in the path found by BFS: {len(bfs_path)}')
print(f'Total distance of path found by BFS: {bfs_dist} m')
print(f'The number of visited nodes in BFS: {bfs_visited}\n')

fmap = folium.Map(location=(24.806383132251874, 120.97685775516189), zoom_start=13)
for line in load_path_graph(bfs_path):
    fmap.add_child(folium.PolyLine(locations=line, tooltip='bfs', weight=4, color='blue'))
fmap

# Don't change this part.
# Show the result of DFS
dfs_path, dfs_dist, dfs_visited = dfs(start, end)
print(f'The number of nodes in the path found by DFS: {len(dfs_path)}')
print(f'Total distance of path found by DFS: {dfs_dist} m')
print(f'The number of visited nodes in DFS: {dfs_visited}\n')

fmap = folium.Map(location=(24.806383132251874, 120.97685775516189), zoom_start=13)
for line in load_path_graph(dfs_path):
    fmap.add_child(folium.PolyLine(locations=line, tooltip='dfs', weight=4, color='green'))
fmap

# Don't change this part.
# Show the result of UCS
ucs_path, ucs_dist, ucs_visited = ucs(start, end)
print(f'The number of nodes in the path found by UCS: {len(ucs_path)}')
print(f'Total distance of path found by UCS: {ucs_dist} m')
print(f'The number of visited nodes in UCS: {ucs_visited}\n')

fmap = folium.Map(location=(24.806383132251874, 120.97685775516189), zoom_start=13)
for line in load_path_graph(ucs_path):
    fmap.add_child(folium.PolyLine(locations=line, tooltip='ucs', weight=4, color='violet'))
fmap

# Don't change this part.
# Show the result of A* search
astar_path, astar_dist, astar_visited = astar(start, end)
print(f'The number of nodes in the path found by A* search: {len(astar_path)}')
print(f'Total distance of path found by A* search: {astar_dist} m')
print(f'The number of visited nodes in A* search: {astar_visited}\n')

fmap = folium.Map(location=(24.806383132251874, 120.97685775516189), zoom_start=13)
for line in load_path_graph(astar_path):
    fmap.add_child(folium.PolyLine(locations=line, tooltip='astar', weight=4, color='red'))
fmap

# Part 6 (Bonus)
# Don't change this part.
# Show the shortest time result of A* search
time_path, time, time_visited = astar_time(start, end)
print(f'The number of nodes in the path found by A* search: {len(time_path)}')
print(f'Total second of path found by A* search: {time} s')
print(f'The number of visited nodes in A* search: {time_visited}\n')

fmap = folium.Map(location=(24.806383132251874, 120.97685775516189), zoom_start=13)
for line in load_path_graph(time_path):
    fmap.add_child(folium.PolyLine(locations=line, tooltip='astar', weight=4, color='red'))
fmap