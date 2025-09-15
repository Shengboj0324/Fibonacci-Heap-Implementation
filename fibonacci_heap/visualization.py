

from typing import List, Dict, Optional, Tuple
import math
from .fibonacci_heap import FibonacciHeap
from .fibonacci_node import FibonacciNode

class FibonacciHeapVisualizer:
    # Visualization and operation logging for Fibonacci heaps
    def __init__(self):
        self.operation_log: List[Dict] = []  # Track operations for analysis

    def log_operation(self, operation: str, heap: FibonacciHeap, **kwargs) -> None:
        # Record operation with heap state for analysis
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
