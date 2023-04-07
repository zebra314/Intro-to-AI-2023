import csv
edgeFile = 'edges.csv'


def dfs(start, end):
    # Begin your code (Part 2)
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
    :stack: a list of string, storing the nodes while implementing DFS.
    :visited: a list of string, storing the nodes that have visited.
    :parent: a dictionary that records the parent node of each node in DFS,
            will use it to trace back the shortest path from the start to the end node.
    :nodes: a dictionary that stores the nodes that are connected to the current node.
    :found: a boolean value that indicates whether the end node is found.
    """
    stack = []
    stack.append(str(start))

    visited = set()
    visited.add(str(start))

    parent = {str(start): None}
    nodes = dict()
    found = False

    """
    Implement DFS.
    - End the loop if the stack is empty or the end node is found.
    - In the loop:
        - Take out the last element in the stack.
        - Add the current node to the visited list.
        - Add the current node to the parent list.
        - If the end node is found, break the loop.
        - If the current node has not been visited, add it to the stack.
    """
    while len(stack) > 0 and found == False:
        vertex = stack.pop()
        num_visited += 1
        nodes = graph[vertex]
        for node in nodes:
            if node not in visited:
                visited.add(node)
                parent[node] = vertex
                if node == str(end):
                    found = True
                    break
                stack.append(node)

    """
    Trace back from end to start.
    - End the loop if the start node is found.
    - In the loop:
        - Add the current node to the path list.
        - If the current node is the start node, break the loop.
        - Add the distance between the current node and its parent node to the dist value.
        - Update the current node to its parent node.
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
    # End your code (Part 2)


if __name__ == '__main__':
    path, dist, num_visited = dfs(2270143902, 1079387396)
    print(f'The number of path nodes: {len(path)}')
    print(f'Total distance of path: {dist}')
    print(f'The number of visited nodes: {num_visited}')
