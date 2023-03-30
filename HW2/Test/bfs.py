import csv
edgeFile = 'edges.csv'

def bfs(start, end):
    # Begin your code (Part 1)
    # raise NotImplementedError("To be implemented")
    
    # the data format: start, end, distance, speed limit
    # Load data and store in with { start { end : ( distance, speed limit ) } }
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

            graph[ data[0]][ data[1]] = ( float(data[2]), float(data[3]) )
            graph[ data[1]][ data[0]] = ( float(data[2]), float(data[3]) )

    # Init
    queue = []
    queue.append(str(start))

    visited = set()
    visited.add(str(start))

    nodes = dict()

    parent = {str(start):None}

    path = []
    dist = 0.0
    num_visited = 0

    # BFS
    while len(queue) > 0 :
        vertex = queue.pop(0) # Take out the first element in the queue
        num_visited += 1
        nodes = graph[vertex]
        for node in nodes: 
            if node not in visited:
                visited.add(node)
                parent[node] = vertex
                queue.append(node)
        
    
    # Trace back from end to start 
    point = str(end)
    while point != start:
        path.append(int(point))
        if parent[point] == None:
            break
        dist = dist + float( graph[ point ] [ parent[point] ] [0] )
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