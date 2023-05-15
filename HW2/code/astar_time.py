import csv
import queue
edgeFile = 'edges.csv'
heuristicFile = 'heuristic.csv'


def astar_time(start, end):
    # Begin your code (Part 6)
    # raise NotImplementedError("To be implemented")
    """
    Load the csv data and store in a nested map.
    :edgeFile: The csv data in the format of "start, end, distance, speed limit".
    :graph: A nested map, storing the data of edgeFile in the format of
            { start { end : ( distance, speed limit ) } }.
    """
    graph = dict()
    max_speed = 0
    with open(edgeFile, 'r') as f:
        for line in f:

            data = line.split(',')
            if data[0] == 'start':
                continue
            if data[0] not in graph:
                graph[data[0]] = dict()
            if data[1] not in graph:
                graph[data[1]] = dict()

            data[3] = data[3].split('\n')[0]
            data[3] = str(float(data[3])*1000/3600)  # convert km/hr to m/s

            max_speed = max(max_speed, float(data[3]))
            graph[data[0]][data[1]] = (float(data[2]), float(data[3]))

    """
    Load the heuristic data and store in a map.
    :heuristicFile: The csv data in the format of "node, distance to ID1, ..., distance to ID3".
    :straight_dist: A map, storing the data of heuristicFile in the format of
                    { node : h }.
    """
    straight_dist = dict()
    with open(heuristicFile, 'r') as f:
        for line in f:
            data = line.split(',')
            data[3] = data[3].split('\n')[0]
            if data[0] == 'node':
                for i, element in enumerate(data):
                    if element == str(end):
                        case = i
                        break
                continue
            straight_dist[data[0]] = float(data[case])

    """
    Init the return values.
    :path: a list of string, storing the shortest path from the start to the end node.
    :time: a float value that stores the total time of the shortest path.
    :num_visited: an integer that stores the number of nodes that have been visited.
    """
    path = []
    time = 0.0
    num_visited = 0

    """
    Init the containers.
    :que: a priority queue, storing the nodes to be visited.
    :visited: a set, storing the nodes that have been visited.
    :parent: a map, storing the parent of each node.
    :nodes: a map, storing the neighbors of each node.
    :found: a boolean, indicating whether the end node has been found.
    """
    que = queue.PriorityQueue()
    que.put((0 + straight_dist[str(start)] / max_speed, str(start)))

    visited = set()
    visited.add(str(start))

    parent = {str(start): (None, 0.0)}
    nodes = dict()
    found = False

    """
    Implement the A* algorithm.
    :weight: g() + h()
        - g() = the time cost from start to current node
        - h() = the time cost of the straight line distance from current node to end node
    - The steps is the same as the A* algorithm.
    """
    while que.empty() == 0 and found == False:
        vertex = que.get()
        num_visited += 1
        if vertex[1] == str(end):
            found = True
            break
        nodes = graph[vertex[1]]
        for node in nodes:
            weight = vertex[0] + graph[vertex[1]][node][0] / graph[vertex[1]][node][1] + \
                straight_dist[node] / max_speed - \
                straight_dist[vertex[1]] / max_speed
            if node not in visited or weight < parent[node][1]:
                visited.add(node)
                parent[node] = (vertex[1], weight)  # (point, time)
                que.put((weight, node))

    """
    Trace back from end to start.
    - End the loop when the start node is reached.
    - Append the node to the path.
    - Update the time.
    """
    point = str(end)
    while point != str(start):
        path.append(int(point))
        if parent[point][0] == None:
            break
        time = time + graph[parent[point][0]][point][0] / \
            graph[parent[point][0]][point][1]
        point = parent[point][0]

    path.append(start)
    path.reverse()

    return path, time, num_visited
    # End your code (Part 6)


if __name__ == '__main__':
    path, time, num_visited = astar_time(2270143902, 1079387396)
    print(f'The number of path nodes: {len(path)}')
    print(f'Total second of path: {time}')
    print(f'The number of visited nodes: {num_visited}')
