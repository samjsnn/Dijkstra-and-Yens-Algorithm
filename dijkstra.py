import heapq
from collections import defaultdict

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


def dijkstra(graph, source, target, k):
    paths = []  # List to store the k shortest paths
    queue = [(0, [source])]  # Priority queue to store paths
    cumulative_weights = defaultdict(
        lambda: float("inf")
    )  # Precomputed cumulative weights

    cumulative_weights[source] = 0

    while queue and len(paths) < k:
        _, path = heapq.heappop(queue)
        node = path[-1]

        if node == target:
            paths.append((path, cumulative_weights[node]))

        if len(paths) == k:
            break

        for neighbor, weight in graph[node].items():
            new_weight = cumulative_weights[node] + weight
            if new_weight < cumulative_weights[neighbor]:
                cumulative_weights[neighbor] = new_weight
                new_path = path + [neighbor]
                heapq.heappush(queue, (new_weight, new_path))

    return paths


if __name__ == "__main__":
    # input data
    graph = read_graph(DATA)

    with open(DATA, "r") as f:
        lines = f.readlines()
        last_line = lines[-1].strip().split()
        start_vertex, end_vertex, k = last_line[0], last_line[1], int(last_line[2])

    print(start_vertex, end_vertex, k)
    # find the k-shortest loopless paths using Dijkstra's Algorithm with binary heap
    shortest_paths = dijkstra(graph, start_vertex, end_vertex, k)

    # print the costs of the k-shortest loopless paths
    print(f"The {k} shortest paths from {start_vertex} to {end_vertex} are:")
    for i, (path, total_weight) in enumerate(shortest_paths[:k]):
        print(f"P{i + 1}: Cost = {total_weight}")
