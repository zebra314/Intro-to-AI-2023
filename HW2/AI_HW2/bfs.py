import csv
edgeFile = 'edges.csv'


def bfs(start, end):
    # Begin your code (Part 1)
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
    :queue: a list of string, storing the nodes while implementing BFS.
    :visited: a list of string, storing the nodes that have visited.
    :parent: a dictionary that records the parent node of each node in BFS,
            will use it to trace back the shortest path from the start to the end node.
    :nodes: a dictionary that stores the nodes that are connected to the current node.
    :found: a boolean value that indicates whether the end node is found.
    """
    queue = []
    queue.append(str(start))

    visited = set()
    visited.add(str(start))

    parent = {str(start): None}
    nodes = dict()
    found = False

    """
    Implement BFS.
    - End the loop if the end node is found or the queue is empty.
    - In the loop:
        - Take out the first element in the queue.
        - Add the current node to the visited list.
        - Add the current node to the parent dictionary.
        - Check if it is the end node.
        - If not, add its neighbors to the queue.
    """
    while len(queue) > 0 and found == False:
        vertex = queue.pop(0)
        num_visited += 1
        nodes = graph[vertex]
        for node in nodes:
            if node not in visited:
                visited.add(node)
                parent[node] = vertex
                if node == str(end):
                    found = True
                    break
                queue.append(node)

    """
    Trace back from end to start.
    - End the loop if the start node is found or the parent dictionary is empty.
    - In the loop:
        - Add the current node to the path list.
        - Add the distance between the current node and its parent to the dist value.
        - Update the current node to its parent.
    """
    point = str(end)
    while point != str(start):
        path.append(int(point))
        if parent[point] == None:
            break
        dist = dist + float(graph[parent[point]][point][0])
        point = parent[point]

    path.append(start)
    path.reverse()

    return path, dist, num_visited
    # End your code (Part 1)


if __name__ == '__main__':
    path, dist, num_visited = bfs(2270143902, 1079387396)
    print(f'The number of path nodes: {len(path)}')
    print(f'Total distance of path: {dist}')
    print(f'The number of visited nodes: {num_visited}')
