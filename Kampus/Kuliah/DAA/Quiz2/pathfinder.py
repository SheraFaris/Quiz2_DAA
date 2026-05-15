import random
import itertools
from heapq import heappop, heappush

grid = [[round(random.random(), 2) for _ in range(6)] for _ in range(6)]

class graph:
    def __init__(self, adjacency_list=None):
        self.adjacency_list = adjacency_list or {}


class vertex:
    def __init__(self):
        self.value = None


class edge:
    def __init__(self, distance=None, vertex=None):
        self.distance = distance
        self.vertex = vertex


def build_adjacency_list(grid):
    adjacency_list = {}
    height = len(grid)
    width = len(grid[0]) if height else 0

    for y in range(height):
        for x in range(width):
            node = (x, y)
            adjacency_list[node] = []

            for dx, dy in ((1, 0), (-1, 0), (0, 1), (0, -1)):
                nx, ny = x + dx, y + dy
                if 0 <= nx < width and 0 <= ny < height:
                    adjacency_list[node].append(edge(grid[ny][nx], (nx, ny)))

    return adjacency_list


graph_map = graph(build_adjacency_list(grid))

def djakstra(graph, start):
    previous = {v: None for v in graph.adjacency_list.keys()}
    visited = {v: False for v in graph.adjacency_list.keys()}
    distances = {v: float("inf") for v in graph.adjacency_list.keys()}
    distances[start] = 0
    queue = PriorityQueue()
    queue.add_task(0, start)
    while len(queue) > 0:
        removed_distance, removed = queue.pop_task()
        if visited[removed]:
            continue
        visited[removed] = True
        for edge in graph.adjacency_list[removed]:
            if visited[edge.vertex]:
                continue
            new_distance = removed_distance + edge.distance
            if new_distance < distances[edge.vertex]:
                distances[edge.vertex] = new_distance
                previous[edge.vertex] = removed
                queue.add_task(new_distance, edge.vertex)
    return previous, distances


def reconstruct_path(previous, start, end):
    path = []
    current = end

    while current is not None:
        path.append(current)
        if current == start:
            break
        current = previous[current]

    path.reverse()
    return path if path and path[0] == start else []

class PriorityQueue:
    def __init__(self):
        self.pq = []
        self.entry_finder = {}
        self.counter = itertools.count()

    def __len__(self):
        return len(self.entry_finder)
    
    def add_task(self, priority, task):
        'Add new task or update task priority'
        if task in self.entry_finder:
            self.update_priority(priority, task)
            return
        count = next(self.counter)
        entry = [priority, count, task]
        self.entry_finder[task] = entry
        heappush(self.pq, entry)
    
    def update_priority(self, priority, task):
        'update task priority, KeyError if unfound'
        entry = self.entry_finder[task]
        entry[2] = None
        count = next(self.counter)
        new_entry = [priority, count, task]
        self.entry_finder[task] = new_entry
        heappush(self.pq, new_entry)

    def pop_task(self):
        'remove return lowest priority task, KeyError if unfound'
        while self.pq:
            priority, count, task = heappop(self.pq)
            if task is None:
                continue
            del self.entry_finder[task]
            return priority, task
        raise KeyError('Pop from an empty Priority Queue')

for y in range(len(grid)):
    for x in range(len(grid[y])):
        print(grid[y][x], end=" ")
    print()

print("adjacency_list_size:", len(graph_map.adjacency_list))

start = (0, 0)
end = (5, 5)
previous, distances = djakstra(graph_map, start)
path = reconstruct_path(previous, start, end)

print("start:", start)
print("end:", end)
print("shortest_distance:", distances[end])
print("shortest_path:", path)



