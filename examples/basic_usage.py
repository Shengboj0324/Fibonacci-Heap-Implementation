

import sys
import os

# Add parent directory to path for imports
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from fibonacci_heap import FibonacciHeap, FibonacciHeapAnalyzer, FibonacciHeapVisualizer

def basic_operations_demo():

    print("=== Basic Fibonacci Heap Operations ===\n")

    # Create a new heap
    heap = FibonacciHeap()
    print("Created empty Fibonacci heap")
    print(f"Is empty: {heap.is_empty()}")
    print(f"Size: {len(heap)}")
    print()

    # Insert elements
    print("Inserting elements: 10, 5, 20, 3, 15, 8")
    nodes = {}
    for key in [10, 5, 20, 3, 15, 8]:
        node = heap.insert(key, f"data_{key}")
        nodes[key] = node
        print(f"Inserted {key}, current minimum: {heap.find_min().key}")

    print(f"\nHeap size: {len(heap)}")
    print(f"Number of trees: {heap.num_trees}")
    print(f"Potential function: {heap.potential()}")
    print()

    # Find minimum
    min_node = heap.find_min()
    print(f"Minimum element: {min_node.key} (data: {min_node.data})")
    print()

    # Delete minimum elements
    print("Deleting minimum elements:")
    while not heap.is_empty():
        min_node = heap.delete_min()
        print(f"Deleted: {min_node.key}, new size: {len(heap)}")
        if not heap.is_empty():
            print(f"  New minimum: {heap.find_min().key}")

    print("\nHeap is now empty")

def decrease_key_demo():

    print("\n=== Decrease Key Operation ===\n")

    heap = FibonacciHeap()

    # Insert elements
    print("Inserting elements: 20, 15, 10, 25, 30")
    nodes = {}
    for key in [20, 15, 10, 25, 30]:
        nodes[key] = heap.insert(key)

    print(f"Initial minimum: {heap.find_min().key}")

    # Decrease key of element 25 to 5
    print("\nDecreasing key of element 25 to 5")
    heap.decrease_key(nodes[25], 5)
    print(f"New minimum: {heap.find_min().key}")

    # Decrease key of element 30 to 1
    print("\nDecreasing key of element 30 to 1")
    heap.decrease_key(nodes[30], 1)
    print(f"New minimum: {heap.find_min().key}")

    # Extract all elements to see final order
    print("\nExtracting all elements:")
    while not heap.is_empty():
        min_node = heap.delete_min()
        print(f"Extracted: {min_node.key}")

def merge_demo():

    print("\n=== Heap Merging ===\n")

    # Create first heap
    heap1 = FibonacciHeap()
    print("Creating first heap with elements: 10, 20, 30")
    for key in [10, 20, 30]:
        heap1.insert(key)

    # Create second heap
    heap2 = FibonacciHeap()
    print("Creating second heap with elements: 5, 15, 25")
    for key in [5, 15, 25]:
        heap2.insert(key)

    print(f"Heap1 minimum: {heap1.find_min().key}, size: {len(heap1)}")
    print(f"Heap2 minimum: {heap2.find_min().key}, size: {len(heap2)}")

    # Merge heaps
    merged = heap1.merge(heap2)
    print(f"\nMerged heap minimum: {merged.find_min().key}, size: {len(merged)}")

    # Extract all elements
    print("\nExtracting all elements from merged heap:")
    while not merged.is_empty():
        min_node = merged.delete_min()
        print(f"Extracted: {min_node.key}")

def delete_operation_demo():

    print("\n=== Delete Operation ===\n")

    heap = FibonacciHeap()

    # Insert elements and keep references
    print("Inserting elements: 10, 5, 20, 3, 15, 8")
    nodes = {}
    for key in [10, 5, 20, 3, 15, 8]:
        nodes[key] = heap.insert(key)

    print(f"Initial heap size: {len(heap)}")
    print(f"Initial minimum: {heap.find_min().key}")

    # Delete element 20
    print("\nDeleting element 20")
    heap.delete(nodes[20])
    print(f"New heap size: {len(heap)}")
    print(f"Current minimum: {heap.find_min().key}")

    # Delete element 5
    print("\nDeleting element 5")
    heap.delete(nodes[5])
    print(f"New heap size: {len(heap)}")
    print(f"Current minimum: {heap.find_min().key}")

    # Extract remaining elements
    print("\nExtracting remaining elements:")
    while not heap.is_empty():
        min_node = heap.delete_min()
        print(f"Extracted: {min_node.key}")

def performance_demo():

    print("\n=== Performance Analysis ===\n")

    analyzer = FibonacciHeapAnalyzer()

    # Benchmark different heap sizes
    sizes = [100, 500, 1000]
    print("Benchmarking operations for different heap sizes:")

    for size in sizes:
        print(f"\nHeap size: {size}")
        results = analyzer.benchmark_operations(size)

        print(f"  Insert average time: {results['insert']['avg_time']:.6f}s")
        print(f"  Find min time: {results['find_min']['time']:.6f}s")
        print(f"  Delete min average time: {results['delete_min']['avg_time']:.6f}s")
        print(f"  Decrease key average time: {results['decrease_key']['avg_time']:.6f}s")

def visualization_demo():

    print("\n=== Heap Visualization ===\n")

    heap = FibonacciHeap()
    visualizer = FibonacciHeapVisualizer()

    # Build a small heap
    print("Building heap with elements: 10, 5, 20, 3, 15")
    for key in [10, 5, 20, 3, 15]:
        heap.insert(key)
        visualizer.log_operation("insert", heap, key=key)

    # Print heap structure
    print("\nHeap structure:")
    print(visualizer.print_heap_structure(heap))

    # Perform delete_min and show structure
    print("After delete_min:")
    heap.delete_min()
    visualizer.log_operation("delete_min", heap)
    print(visualizer.print_heap_structure(heap))

    # Show operation summary
    print("\nOperation summary:")
    print(visualizer.print_operation_summary())

def mathematical_analysis_demo():

    print("\n=== Mathematical Analysis ===\n")

    analyzer = FibonacciHeapAnalyzer()
    heap = FibonacciHeap()

    # Build heap
    print("Building heap with 20 elements")
    for i in range(20):
        heap.insert(i)

    # Perform some operations
    for _ in range(5):
        heap.delete_min()

    # Analyze properties
    analysis = analyzer.theoretical_vs_actual_analysis(heap)

    print(f"Heap size: {analysis['heap_size']}")
    print(f"Number of trees: {analysis['num_trees']}")
    print(f"Number of marked nodes: {analysis['num_marked']}")
    print(f"Potential function: {analysis['potential']}")
    print(f"Theoretical max degree: {analysis['theoretical_max_degree']}")
    print(f"Actual max degree: {analysis['actual_max_degree']}")
    print(f"Degree bound satisfied: {analysis['degree_bound_satisfied']}")
    print(f"Fibonacci property satisfied: {analysis['fibonacci_property_satisfied']}")

    # Test Fibonacci numbers
    print("\nFirst 10 Fibonacci numbers:")
    for i in range(10):
        fib = analyzer.fibonacci_number(i)
        print(f"F({i}) = {fib}")

    print(f"\nGolden ratio: {analyzer.golden_ratio():.10f}")

def main():

    print("Fibonacci Heap Implementation - Basic Usage Examples")
    print("=" * 60)

    try:
        basic_operations_demo()
        decrease_key_demo()
        merge_demo()
        delete_operation_demo()
        performance_demo()
        visualization_demo()
        mathematical_analysis_demo()

        print("\n" + "=" * 60)
        print("All demonstrations completed successfully!")

    except Exception as e:
        print(f"\nError during demonstration: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()
