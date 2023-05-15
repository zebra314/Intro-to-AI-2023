import csv
import queue
edgeFile = 'edges.csv'
heuristicFile = 'heuristic.csv'


def astar(start, end):
    # Begin your code (Part 4)
    # raise NotImplementedError("To be implemented")
    """
    Load the csv data and store in a nested map.
    :edgeFile: The csv data in the format of "start, end, distance, speed limit".
    :graph: A nested map, storing the data of edgeFile in the format of
            { start { end : ( distance, speed limit ) } }.
    """
    graph = dict()
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
    :dist: a float value that stores the total distance of the shortest path.
    :num_visited: an integer value that stores the number of visited nodes.
    """
    path = []
    dist = 0.0
    num_visited = 0

    """
    Init the containers.
    :que: a priority queue of string, storing the nodes while implementing UCS.
    :visited: a list of string, storing the nodes that have visited.
    :parent: a dictionary that records the parent node of each node in UCS,
                in the format of { node : ( parent, distance ) }.
    :nodes: a dictionary that stores the neighbors of the current node.
    :found: a boolean value that indicates whether the end node is found.
    """
    que = queue.PriorityQueue()
    que.put((0 + straight_dist[str(start)], str(start)))

    visited = set()
    visited.add(str(start))

    parent = {str(start): (None, 0.0)}
    nodes = dict()
    found = False

    """
    Implement A* algorithm.
    :weight: g() + h()
        - g(): the distance which have walked
        - h(): straight line distance between that node and end node
    
    - End the loop when the queue is empty or the end node is found.
    - In the loop:
        - Get the node with the smallest distance from the queue.
        - If the node is the end node, end the loop.
        - Get the neighbors of the node.
        - For each neighbor, Calculate the weight from the start node to the neighbor.
        - If the neighbor is not visited or the weight is smaller than the previous one,
        - Add the neighbor to the visited set.
        - Record the parent node and the distance in the parent dictionary.
        - Add the neighbor to the queue.
    """
    while que.empty() == 0 and found == False:
        vertex = que.get()
        num_visited += 1
        if vertex[1] == str(end):
            found = True
            break
        nodes = graph[vertex[1]]
        for node in nodes:
            weight = vertex[0] + graph[vertex[1]][node][0] + \
                straight_dist[node] - straight_dist[vertex[1]]
            if node not in visited or weight < parent[node][1]:
                visited.add(node)
                parent[node] = (vertex[1], weight)  # (point, distance)
                que.put((weight, node))

    """
    Trace back from end to start.
    - End the loop when the start node is found.
    - In the loop:
        - Get the parent node of the current node.
        - If the parent node is not found, end the loop.
        - Calculate the distance from the parent node to the current node.
        - Add the current node to the path.
    """
    point = str(end)
    while point != str(start):
        path.append(int(point))
        if parent[point][0] == None:
            break
        dist = dist + float(graph[parent[point][0]][point][0])
        point = parent[point][0]

    path.append(start)
    path.reverse()

    return path, dist, num_visited
    # End your code (Part 4)


if __name__ == '__main__':
    path, dist, num_visited = astar(2270143902, 1079387396)
    print(f'The number of path nodes: {len(path)}')
    print(f'Total distance of path: {dist}')
    print(f'The number of visited nodes: {num_visited}')
