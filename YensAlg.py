import heapq
from collections import defaultdict
import sys

DATA = "finalinput.txt"


def read_graph(filename):
    graph = defaultdict(dict)
    with open(filename, "r") as f:
        lines = f.readlines()[1:]
        total_lines = len(lines)
        for line_number, line in enumerate(lines):
            if line_number == total_lines - 1:
                break  # Skip the last line of the file

            parts = line.strip().split()
            if len(parts) < 3:
                continue  # Skip lines that don't have enough elements

            vertex1, vertex2, weight = parts[0], parts[1], float(parts[2])
            graph[vertex1][vertex2] = weight
            graph[vertex2][vertex1] = weight

    return graph


def dijkstra(graph, source, target):
    distances = defaultdict(lambda: sys.maxsize)
    distances[source] = 0
    visited = set()

    queue = [(0, source)]
    while queue:
        current_distance, current_vertex = heapq.heappop(queue)
        if current_vertex == target:
            break

        if current_distance > distances[current_vertex]:
            continue

        visited.add(current_vertex)
        for neighbor, weight in graph[current_vertex].items():
            distance = current_distance + weight
            if distance < distances[neighbor]:
                distances[neighbor] = distance
                heapq.heappush(queue, (distance, neighbor))

    return visited, distances


def yen_algorithm(graph, source, target, k):
    paths = []  # List to store the k shortest paths
    potential_paths = []  # List to store potential candidate paths

    # Find the shortest path using Dijkstra's algorithm
    visited, distances = dijkstra(graph, source, target)
    if distances[target] == sys.maxsize:
        return paths

    shortest_path = [target]
    node = target

    while node != source:
        min_distance = sys.maxsize
        min_node = None

        for neighbor, weight in graph[node].items():
            distance = distances[neighbor]
            if distance < min_distance and neighbor not in shortest_path:
                min_distance = distance
                min_node = neighbor

        if min_node is None:
            break

        shortest_path.append(min_node)
        node = min_node

    paths.append((shortest_path[::-1], distances[target]))

    for _ in range(1, k):
        for i in range(len(paths[-1][0]) - 1):
            spur_node = paths[-1][0][i]
            root_path = paths[-1][0][: i + 1]

            graph_copy = defaultdict(dict)
            for u, neighbors in graph.items():
                if u not in root_path:
                    continue
                for v, weight in neighbors.items():
                    if v not in root_path:
                        continue
                    graph_copy[u][v] = weight

            for path in paths:
                if path[0][: i + 1] == root_path:
                    graph_copy[path[0][i]][path[0][i + 1]] = sys.maxsize

            visited, distances = dijkstra(graph_copy, spur_node, target)
            if distances[target] != sys.maxsize:
                spur_path = [spur_node]
                node = spur_node

                while node != target:
                    min_distance = sys.maxsize
                    min_node = None

                    for neighbor, weight in graph[node].items():
                        distance = distances[neighbor]
                        if distance < min_distance and neighbor not in spur_path:
                            min_distance = distance
                            min_node = neighbor

                    if min_node is None:
                        break

                    spur_path.append(min_node)
                    node = min_node

                potential_path = root_path + spur_path
                potential_paths.append((potential_path, sum(distances.values())))

        if not potential_paths:
            break

        potential_paths.sort(key=lambda x: x[1])

        paths.append(potential_paths.pop(0))

    print(paths)
    return paths


if __name__ == "__main__":
    # input data
    graph = read_graph(DATA)

    with open(DATA, "r") as f:
        lines = f.readlines()
        last_line = lines[-1].strip().split()
        start_vertex, end_vertex, k = last_line[0], last_line[1], int(last_line[2])

    print(start_vertex, end_vertex, k)
    # find the k-shortest loopless paths using Yen's Algorithm
    shortest_paths = yen_algorithm(graph, start_vertex, end_vertex, k)

    # print the costs of the k-shortest loopless paths
    print(f"The {k} shortest paths from {start_vertex} to {end_vertex} are:")
    for i, (path, total_weight) in enumerate(shortest_paths):
        print(f"Path {i + 1}: Cost = {total_weight}")
