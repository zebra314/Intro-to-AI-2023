import csv
from collections import deque
edgeFile = 'edges.csv'
edgeFile = '/home/alfonso/Git_workspace/ProgramLearn/intro_to_ai/HW2/AI_HW2/' + edgeFile

def bfs(start, end):
    #　Implement a bfs algorithm
    #　Input: start, end
    #　Output: path, dist, num_visited
    
    with open(edgeFile, 'r') as f:
        for line in f:
            data = line.split(',')
            if data[0] == 'start':
                print(line)
                break
            


    path = []
    dist = 0
    num_visited = 0

    return path, dist, num_visited
    # Begin your code (Part 1)
    # raise NotImplementedError("To be implemented")
    # End your code (Part 1)


if __name__ == '__main__':
    path, dist, num_visited = bfs(2270143902, 1079387396)
    print(f'The number of path nodes: {len(path)}')
    print(f'Total distance of path: {dist}')
    print(f'The number of visited nodes: {num_visited}')


