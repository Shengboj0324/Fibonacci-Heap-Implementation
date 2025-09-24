"""
Fibonacci Heap Analysis and Visualization

This module provides comprehensive analysis, benchmarking, and visualization tools
for Fibonacci heaps. Combines mathematical analysis, performance measurement,
and visual representation capabilities.

Consolidates the analysis and visualization functionality while maintaining
all existing features and behavior.
"""

from typing import List, Dict, Tuple, Optional, Any
import math
import time
from .core import FibonacciHeap, FibonacciNode


class FibonacciHeapAnalyzer:
    """Mathematical analysis and performance benchmarking tools for Fibonacci heaps."""
    
    def __init__(self):
        # Track operation counts and timing
        self.operation_counts: Dict[str, int] = {
            'insert': 0,
            'delete_min': 0,
            'decrease_key': 0,
            'delete': 0,
            'merge': 0,
            'find_min': 0
        }
        self.operation_times: Dict[str, List[float]] = {
            'insert': [],
            'delete_min': [],
            'decrease_key': [],
            'delete': [],
            'merge': [],
            'find_min': []
        }
        self.potential_history: List[int] = []  # Track potential function over time

    @staticmethod
    def fibonacci_number(n: int) -> int:
        """Calculate nth Fibonacci number efficiently."""
        if n <= 1:
            return n

        a, b = 0, 1
        for _ in range(2, n + 1):
            a, b = b, a + b

        return b

    @staticmethod
    def golden_ratio() -> float:
        """Calculate the golden ratio: φ = (1 + √5) / 2 ≈ 1.618."""
        return (1 + math.sqrt(5)) / 2

    @staticmethod
    def max_degree_bound(n: int) -> int:
        """Calculate maximum degree bound: ⌊log_φ(n)⌋."""
        if n <= 0:
            return 0

        phi = FibonacciHeapAnalyzer.golden_ratio()
        return int(math.log(n) / math.log(phi))

    def verify_fibonacci_property(self, heap: FibonacciHeap) -> bool:
        """Verify that all nodes in the heap satisfy the Fibonacci property."""
        if heap.is_empty():
            return True

        def check_node_iterative(root: FibonacciNode) -> bool:
            # Use iterative approach to avoid recursion depth issues
            stack = [root]
            while stack:
                node = stack.pop()
                if not node.verify_fibonacci_property():
                    return False
                # Add children to stack for processing
                stack.extend(node.get_children())
            return True

        # Check all root nodes
        return all(check_node_iterative(root) for root in heap.get_roots())

    def verify_degree_bound(self, heap: FibonacciHeap) -> bool:
        """Verify that the maximum degree satisfies the theoretical bound."""
        if heap.is_empty():
            return True

        max_degree = 0
        for root in heap.get_roots():
            max_degree = max(max_degree, root.max_degree_in_subtree())

        theoretical_bound = self.max_degree_bound(len(heap))
        return max_degree <= theoretical_bound

    def analyze_potential_change(self, heap: FibonacciHeap, operation: str,
                               actual_time: float) -> Dict[str, float]:
        """Analyze the change in potential function for amortized analysis."""
        current_potential = heap.potential()

        if self.potential_history:
            potential_change = current_potential - self.potential_history[-1]
        else:
            potential_change = current_potential

        self.potential_history.append(current_potential)

        # Theoretical amortized cost = actual cost + c * potential change
        # where c is a constant (typically 1)
        c = 1
        amortized_cost = actual_time + c * potential_change

        return {
            'actual_time': actual_time,
            'potential_before': self.potential_history[-2] if len(self.potential_history) > 1 else 0,
            'potential_after': current_potential,
            'potential_change': potential_change,
            'amortized_cost': amortized_cost,
            'operation': operation
        }

    def time_operation(self, operation_func, *args, **kwargs) -> Tuple[Any, float]:
        """Time the execution of an operation and return result and duration."""
        start_time = time.perf_counter()
        result = operation_func(*args, **kwargs)
        end_time = time.perf_counter()

        return result, end_time - start_time

    def benchmark_operations(self, n: int) -> Dict[str, Dict[str, float]]:
        """Benchmark all heap operations with n elements."""
        heap = FibonacciHeap()
        nodes = []

        # Insert n elements
        insert_times = []
        for i in range(n):
            node, time_taken = self.time_operation(heap.insert, i)
            nodes.append(node)
            insert_times.append(time_taken)

        # Benchmark find_min
        _, find_min_time = self.time_operation(heap.find_min)

        # Benchmark decrease_key on random nodes
        decrease_key_times = []
        for i in range(min(10, n)):
            node = nodes[i * n // 10] if n > 10 else nodes[i]
            _, time_taken = self.time_operation(heap.decrease_key, node, node.key - 1)
            decrease_key_times.append(time_taken)

        # Benchmark delete_min
        delete_min_times = []
        for _ in range(min(5, n)):
            if not heap.is_empty():
                _, time_taken = self.time_operation(heap.delete_min)
                delete_min_times.append(time_taken)

        return {
            'insert': {
                'avg_time': sum(insert_times) / len(insert_times),
                'max_time': max(insert_times),
                'min_time': min(insert_times),
                'total_time': sum(insert_times)
            },
            'find_min': {
                'time': find_min_time
            },
            'decrease_key': {
                'avg_time': sum(decrease_key_times) / len(decrease_key_times) if decrease_key_times else 0,
                'max_time': max(decrease_key_times) if decrease_key_times else 0,
                'min_time': min(decrease_key_times) if decrease_key_times else 0
            },
            'delete_min': {
                'avg_time': sum(delete_min_times) / len(delete_min_times) if delete_min_times else 0,
                'max_time': max(delete_min_times) if delete_min_times else 0,
                'min_time': min(delete_min_times) if delete_min_times else 0
            }
        }

    def complexity_analysis(self, heap_sizes: List[int]) -> Dict[str, List[float]]:
        """Analyze time complexity across different heap sizes."""
        results = {
            'sizes': heap_sizes,
            'insert_times': [],
            'delete_min_times': [],
            'decrease_key_times': []
        }

        for size in heap_sizes:
            benchmark = self.benchmark_operations(size)
            results['insert_times'].append(benchmark['insert']['avg_time'])
            results['delete_min_times'].append(benchmark['delete_min']['avg_time'])
            results['decrease_key_times'].append(benchmark['decrease_key']['avg_time'])

        return results

    def theoretical_vs_actual_analysis(self, heap: FibonacciHeap) -> Dict[str, Any]:
        """Compare theoretical properties with actual heap state."""
        if heap.is_empty():
            return {'empty_heap': True}

        n = len(heap)
        theoretical_max_degree = self.max_degree_bound(n)

        actual_max_degree = 0
        for root in heap.get_roots():
            actual_max_degree = max(actual_max_degree, root.max_degree_in_subtree())

        return {
            'heap_size': n,
            'num_trees': heap.num_trees,
            'num_marked': heap.num_marked,
            'potential': heap.potential(),
            'theoretical_max_degree': theoretical_max_degree,
            'actual_max_degree': actual_max_degree,
            'degree_bound_satisfied': actual_max_degree <= theoretical_max_degree,
            'fibonacci_property_satisfied': self.verify_fibonacci_property(heap),
            'theoretical_min_trees': 1,
            'theoretical_max_trees': n,
            'trees_efficiency': 1 - (heap.num_trees - 1) / (n - 1) if n > 1 else 1
        }


class FibonacciHeapVisualizer:
    """Visualization and operation logging for Fibonacci heaps."""
    
    def __init__(self):
        self.operation_log: List[Dict] = []  # Track operations for analysis

    def log_operation(self, operation: str, heap: FibonacciHeap, **kwargs) -> None:
        """Record operation with heap state for analysis."""
        self.operation_log.append({
            'operation': operation,
            'heap_size': len(heap),
            'num_trees': heap.num_trees,
            'num_marked': heap.num_marked,
            'potential': heap.potential(),
            'min_key': heap.min_node.key if heap.min_node else None,
            'timestamp': len(self.operation_log),
            **kwargs
        })

    def print_heap_structure(self, heap: FibonacciHeap, show_details: bool = True) -> str:
        """Generate a string representation of the heap structure."""
        if heap.is_empty():
            return "Empty Fibonacci Heap"

        output = []
        output.append(f"Fibonacci Heap (size={len(heap)}, trees={heap.num_trees}, marked={heap.num_marked})")
        output.append(f"Potential: Φ(H) = {heap.num_trees} + 2×{heap.num_marked} = {heap.potential()}")
        output.append(f"Minimum: {heap.min_node.key}")
        output.append("")

        # Print each tree in root list
        roots = heap.get_roots()
        for i, root in enumerate(roots):
            output.append(f"Tree {i + 1}:")
            tree_repr = self._print_tree(root, "", True, show_details)
            output.extend(tree_repr)
            output.append("")

        return "\n".join(output)

    def _print_tree(self, node: FibonacciNode, prefix: str, is_last: bool,
                   show_details: bool) -> List[str]:
        """Generate tree representation for a node and its subtree."""
        output = []

        # Node representation
        mark_str = "*" if node.marked else ""
        if show_details:
            node_str = f"{node.key}{mark_str} (deg={node.degree})"
        else:
            node_str = f"{node.key}{mark_str}"

        connector = "└── " if is_last else "├── "
        output.append(f"{prefix}{connector}{node_str}")

        # Children
        if node.child is not None:
            children = node.get_children()
            new_prefix = prefix + ("    " if is_last else "│   ")

            for i, child in enumerate(children):
                is_last_child = (i == len(children) - 1)
                child_repr = self._print_tree(child, new_prefix, is_last_child, show_details)
                output.extend(child_repr)

        return output

    def print_operation_summary(self) -> str:
        """Generate a summary of all logged operations."""
        if not self.operation_log:
            return "No operations logged"

        output = []
        output.append("Operation Summary:")
        output.append("=" * 50)

        operation_counts = {}
        for log_entry in self.operation_log:
            op = log_entry['operation']
            operation_counts[op] = operation_counts.get(op, 0) + 1

        for operation, count in operation_counts.items():
            output.append(f"{operation}: {count} times")

        output.append("")
        output.append("Detailed Log:")
        output.append("-" * 30)

        for i, log_entry in enumerate(self.operation_log):
            output.append(f"{i+1:3d}. {log_entry['operation']:<12} "
                         f"size={log_entry['heap_size']:3d} "
                         f"trees={log_entry['num_trees']:2d} "
                         f"marked={log_entry['num_marked']:2d} "
                         f"Φ={log_entry['potential']:3d}")

        return "\n".join(output)

    def generate_dot_graph(self, heap: FibonacciHeap, filename: str = "fibonacci_heap.dot") -> str:
        """Generate a Graphviz DOT representation of the heap."""
        if heap.is_empty():
            return "digraph FibonacciHeap { empty [label=\"Empty Heap\"]; }"

        dot_lines = []
        dot_lines.append("digraph FibonacciHeap {")
        dot_lines.append("  rankdir=TB;")
        dot_lines.append("  node [shape=circle, style=filled];")
        dot_lines.append("")

        # Node definitions
        node_id = 0
        node_map = {}

        def add_node_to_dot(node: FibonacciNode) -> int:
            nonlocal node_id
            current_id = node_id
            node_map[id(node)] = current_id
            node_id += 1

            # Node styling
            color = "lightblue"
            if node == heap.min_node:
                color = "lightgreen"
            elif node.marked:
                color = "lightcoral"

            dot_lines.append(f"  {current_id} [label=\"{node.key}\", fillcolor=\"{color}\"];")

            # Add children
            if node.child is not None:
                children = node.get_children()
                for child in children:
                    child_id = add_node_to_dot(child)
                    dot_lines.append(f"  {current_id} -> {child_id};")

            return current_id

        # Add all trees
        for root in heap.get_roots():
            add_node_to_dot(root)

        # Add root list connections (dashed)
        roots = heap.get_roots()
        if len(roots) > 1:
            dot_lines.append("")
            dot_lines.append("  // Root list connections")
            for i in range(len(roots)):
                current_id = node_map[id(roots[i])]
                next_id = node_map[id(roots[(i + 1) % len(roots)])]
                dot_lines.append(f"  {current_id} -> {next_id} [style=dashed, color=gray];")

        dot_lines.append("")
        dot_lines.append("  // Legend")
        dot_lines.append("  subgraph cluster_legend {")
        dot_lines.append("    label=\"Legend\";")
        dot_lines.append("    style=filled;")
        dot_lines.append("    fillcolor=white;")
        dot_lines.append("    min_node [label=\"Min\", fillcolor=\"lightgreen\"];")
        dot_lines.append("    marked_node [label=\"Marked\", fillcolor=\"lightcoral\"];")
        dot_lines.append("    normal_node [label=\"Normal\", fillcolor=\"lightblue\"];")
        dot_lines.append("  }")

        dot_lines.append("}")

        dot_content = "\n".join(dot_lines)

        # Write to file if filename provided
        if filename:
            with open(filename, 'w') as f:
                f.write(dot_content)

        return dot_content

    def animate_operations(self, operations: List[Tuple[str, List]],
                          delay: float = 1.0) -> None:
        """Animate a sequence of operations on a heap."""
        import time
        import os

        heap = FibonacciHeap()

        for i, (operation, args) in enumerate(operations):
            # Clear screen (works on most terminals)
            os.system('clear' if os.name == 'posix' else 'cls')

            print(f"Step {i + 1}: {operation}({', '.join(map(str, args))})")
            print("=" * 60)

            # Perform operation
            if operation == "insert":
                heap.insert(*args)
            elif operation == "delete_min":
                heap.delete_min()
            elif operation == "decrease_key":
                # For animation, we'll need to track nodes
                pass  # Implementation would need node tracking

            # Show current state
            print(self.print_heap_structure(heap))

            if i < len(operations) - 1:
                print(f"\nNext: {operations[i + 1][0]}({', '.join(map(str, operations[i + 1][1]))})")
                time.sleep(delay)

        print("\nAnimation complete!")

    def complexity_visualization(self, sizes: List[int], times: Dict[str, List[float]]) -> str:
        """Generate a text-based visualization of time complexity analysis."""
        output = []
        output.append("Time Complexity Analysis")
        output.append("=" * 50)

        for operation, time_list in times.items():
            if operation == 'sizes':
                continue

            output.append(f"\n{operation.upper()}:")
            output.append("-" * 20)

            for i, (size, time_val) in enumerate(zip(sizes, time_list)):
                # Simple bar chart using asterisks
                bar_length = int(time_val * 1000000)  # Scale for visibility
                bar = "*" * min(bar_length, 50)
                output.append(f"n={size:4d}: {time_val:.6f}s {bar}")

        return "\n".join(output)
