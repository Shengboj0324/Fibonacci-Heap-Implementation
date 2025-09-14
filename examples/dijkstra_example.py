

import sys
import os
from typing import Dict, List, Tuple, Optional
import math

# Add parent directory to path for imports
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from fibonacci_heap import FibonacciHeap

class Graph:

    def __init__(self):

        self.vertices = set()
        self.edges = {}  # vertex -> [(neighbor, weight), ...]

    def add_vertex(self, vertex):

        self.vertices.add(vertex)
        if vertex not in self.edges:
            self.edges[vertex] = []

    def add_edge(self, from_vertex, to_vertex, weight):

        self.add_vertex(from_vertex)
        self.add_vertex(to_vertex)
        self.edges[from_vertex].append((to_vertex, weight))

    def get_neighbors(self, vertex):

        return self.edges.get(vertex, [])

    def get_vertices(self):

        return list(self.vertices)

def dijkstra_fibonacci_heap(graph: Graph, start_vertex) -> Tuple[Dict, Dict]:

    # Initialize distances and predecessors
    distances = {vertex: math.inf for vertex in graph.get_vertices()}
    predecessors = {vertex: None for vertex in graph.get_vertices()}
    distances[start_vertex] = 0

    # Create Fibonacci heap and insert all vertices
    heap = FibonacciHeap()
    vertex_nodes = {}

    for vertex in graph.get_vertices():
        node = heap.insert(distances[vertex], vertex)
        vertex_nodes[vertex] = node

    visited = set()

    print(f"Starting Dijkstra's algorithm from vertex {start_vertex}")
    print(f"Initial heap size: {len(heap)}")

    while not heap.is_empty():
        # Extract minimum distance vertex
        min_node = heap.delete_min()
        current_vertex = min_node.data
        current_distance = min_node.key

        if current_vertex in visited:
            continue

        visited.add(current_vertex)

        print(f"Processing vertex {current_vertex} with distance {current_distance}")

        # Skip if distance is infinite (unreachable)
        if current_distance == math.inf:
            break

        # Update distances to neighbors
        for neighbor, edge_weight in graph.get_neighbors(current_vertex):
            if neighbor in visited:
                continue

            new_distance = current_distance + edge_weight

            if new_distance < distances[neighbor]:
                print(f"  Updating distance to {neighbor}: {distances[neighbor]} -> {new_distance}")

                # Decrease key in heap
                old_distance = distances[neighbor]
                distances[neighbor] = new_distance
                predecessors[neighbor] = current_vertex

                # Use decrease_key operation (O(1) amortized)
                heap.decrease_key(vertex_nodes[neighbor], new_distance)

    return distances, predecessors

def reconstruct_path(predecessors: Dict, start_vertex, end_vertex) -> List:

    if predecessors[end_vertex] is None and end_vertex != start_vertex:
        return []  # No path exists

    path = []
    current = end_vertex

    while current is not None:
        path.append(current)
        current = predecessors[current]

    path.reverse()
    return path

def create_example_graph() -> Graph:

    graph = Graph()

    # Add edges (from, to, weight)
    edges = [
        ('A', 'B', 4),
        ('A', 'C', 2),
        ('B', 'C', 1),
        ('B', 'D', 5),
        ('C', 'D', 8),
        ('C', 'E', 10),
        ('D', 'E', 2),
        ('D', 'F', 6),
        ('E', 'F', 3)
    ]

    for from_v, to_v, weight in edges:
        graph.add_edge(from_v, to_v, weight)
        graph.add_edge(to_v, from_v, weight)  # Make undirected

    return graph

def print_graph(graph: Graph):

    print("Graph structure:")
    for vertex in sorted(graph.get_vertices()):
        neighbors = graph.get_neighbors(vertex)
        neighbor_str = ", ".join(f"{n}({w})" for n, w in neighbors)
        print(f"  {vertex}: {neighbor_str}")

def print_results(distances: Dict, predecessors: Dict, start_vertex: str):

    print(f"\nShortest distances from {start_vertex}:")
    for vertex in sorted(distances.keys()):
        distance = distances[vertex]
        if distance == math.inf:
            print(f"  {vertex}: unreachable")
        else:
            path = reconstruct_path(predecessors, start_vertex, vertex)
            path_str = " -> ".join(path)
            print(f"  {vertex}: {distance} (path: {path_str})")

def compare_with_naive_dijkstra(graph: Graph, start_vertex) -> None:

    print("\n=== Performance Comparison ===")

    import time

    # Time Fibonacci heap version
    start_time = time.perf_counter()
    fib_distances, fib_predecessors = dijkstra_fibonacci_heap(graph, start_vertex)
    fib_time = time.perf_counter() - start_time

    # Time naive version (using simple list for priority queue)
    start_time = time.perf_counter()
    naive_distances, naive_predecessors = dijkstra_naive(graph, start_vertex)
    naive_time = time.perf_counter() - start_time

    print(f"Fibonacci heap time: {fib_time:.6f} seconds")
    print(f"Naive implementation time: {naive_time:.6f} seconds")

    # Verify results are the same
    if fib_distances == naive_distances:
        print("✓ Both implementations produce identical results")
    else:
        print("✗ Results differ between implementations")

def dijkstra_naive(graph: Graph, start_vertex) -> Tuple[Dict, Dict]:

    distances = {vertex: math.inf for vertex in graph.get_vertices()}
    predecessors = {vertex: None for vertex in graph.get_vertices()}
    distances[start_vertex] = 0

    unvisited = set(graph.get_vertices())

    while unvisited:
        # Find minimum distance vertex (O(V) operation)
        current_vertex = min(unvisited, key=lambda v: distances[v])

        if distances[current_vertex] == math.inf:
            break

        unvisited.remove(current_vertex)

        # Update distances to neighbors
        for neighbor, edge_weight in graph.get_neighbors(current_vertex):
            if neighbor in unvisited:
                new_distance = distances[current_vertex] + edge_weight
                if new_distance < distances[neighbor]:
                    distances[neighbor] = new_distance
                    predecessors[neighbor] = current_vertex

    return distances, predecessors

def create_large_graph(num_vertices: int) -> Graph:

    import random

    graph = Graph()

    # Create vertices
    vertices = [f"V{i}" for i in range(num_vertices)]

    # Add random edges
    for i in range(num_vertices):
        for j in range(i + 1, min(i + 5, num_vertices)):  # Connect to next few vertices
            weight = random.randint(1, 10)
            graph.add_edge(vertices[i], vertices[j], weight)
            graph.add_edge(vertices[j], vertices[i], weight)

    return graph

def performance_test():

    print("\n=== Performance Test on Larger Graph ===")

    sizes = [50, 100, 200]

    for size in sizes:
        print(f"\nTesting graph with {size} vertices:")
        graph = create_large_graph(size)
        start_vertex = f"V0"

        import time
        start_time = time.perf_counter()
        distances, predecessors = dijkstra_fibonacci_heap(graph, start_vertex)
        end_time = time.perf_counter()

        print(f"  Time: {end_time - start_time:.6f} seconds")
        print(f"  Reachable vertices: {sum(1 for d in distances.values() if d != math.inf)}")

def main():

    print("Dijkstra's Algorithm with Fibonacci Heap")
    print("=" * 50)

    # Create and display example graph
    graph = create_example_graph()
    print_graph(graph)

    # Run Dijkstra's algorithm
    start_vertex = 'A'
    print(f"\n=== Running Dijkstra's Algorithm ===")
    distances, predecessors = dijkstra_fibonacci_heap(graph, start_vertex)

    # Print results
    print_results(distances, predecessors, start_vertex)

    # Compare with naive implementation
    compare_with_naive_dijkstra(graph, start_vertex)

    # Performance test
    performance_test()

    print("\n" + "=" * 50)
    print("Dijkstra demonstration completed!")

if __name__ == "__main__":
    main()
