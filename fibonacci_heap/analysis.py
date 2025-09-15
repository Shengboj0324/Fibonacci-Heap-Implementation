

from typing import List, Dict, Tuple, Optional, Any
import math
import time
from .fibonacci_heap import FibonacciHeap
from .fibonacci_node import FibonacciNode

class FibonacciHeapAnalyzer:
    # Mathematical analysis and performance benchmarking tools
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
        # Calculate nth Fibonacci number efficiently
        if n <= 1:
            return n

        a, b = 0, 1
        for _ in range(2, n + 1):
            a, b = b, a + b

        return b

    @staticmethod
    def golden_ratio() -> float:
        # φ = (1 + √5) / 2 ≈ 1.618
        return (1 + math.sqrt(5)) / 2

    @staticmethod
    def max_degree_bound(n: int) -> int:
        # Maximum degree bound: ⌊log_φ(n)⌋

        if n <= 0:
            return 0

        phi = FibonacciHeapAnalyzer.golden_ratio()
        return int(math.log(n) / math.log(phi))

    def verify_fibonacci_property(self, heap: FibonacciHeap) -> bool:
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

        if heap.is_empty():
            return True

        max_degree = 0
        for root in heap.get_roots():
            max_degree = max(max_degree, root.max_degree_in_subtree())

        theoretical_bound = self.max_degree_bound(len(heap))
        return max_degree <= theoretical_bound

    def analyze_potential_change(self, heap: FibonacciHeap, operation: str,
                               actual_time: float) -> Dict[str, float]:

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

        start_time = time.perf_counter()
        result = operation_func(*args, **kwargs)
        end_time = time.perf_counter()

        return result, end_time - start_time

    def benchmark_operations(self, n: int) -> Dict[str, Dict[str, float]]:

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
