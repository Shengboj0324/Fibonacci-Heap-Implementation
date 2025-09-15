

import unittest
import sys
import os

# Add parent directory to path for imports
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from fibonacci_heap.fibonacci_heap import FibonacciHeap
from fibonacci_heap.analysis import FibonacciHeapAnalyzer

class TestFibonacciHeapAnalyzer(unittest.TestCase):

    def setUp(self):

        self.analyzer = FibonacciHeapAnalyzer()
        self.heap = FibonacciHeap()

    def test_fibonacci_number_calculation(self):

        # Test first few Fibonacci numbers
        expected = [0, 1, 1, 2, 3, 5, 8, 13, 21, 34, 55]

        for i, expected_val in enumerate(expected):
            self.assertEqual(self.analyzer.fibonacci_number(i), expected_val)

    def test_golden_ratio(self):

        phi = self.analyzer.golden_ratio()
        expected_phi = (1 + 5**0.5) / 2

        self.assertAlmostEqual(phi, expected_phi, places=10)
        self.assertAlmostEqual(phi, 1.618033988749, places=10)

    def test_max_degree_bound(self):

        # Test for various heap sizes
        test_cases = [
            (1, 0),
            (2, 1),
            (3, 2),
            (5, 2),
            (8, 3),
            (13, 3),
            (21, 4),
            (100, 6),
            (1000, 9)
        ]

        for n, expected_bound in test_cases:
            bound = self.analyzer.max_degree_bound(n)
            self.assertEqual(bound, expected_bound)

    def test_verify_fibonacci_property_empty(self):

        result = self.analyzer.verify_fibonacci_property(self.heap)
        self.assertTrue(result)

    def test_verify_fibonacci_property_simple(self):

        # Insert a few elements
        self.heap.insert(10)
        self.heap.insert(20)
        self.heap.insert(5)

        result = self.analyzer.verify_fibonacci_property(self.heap)
        self.assertTrue(result)

    def test_verify_fibonacci_property_complex(self):

        # Build a more complex heap
        for i in range(20):
            self.heap.insert(i)

        # Perform some operations to create tree structure
        for _ in range(5):
            self.heap.delete_min()

        result = self.analyzer.verify_fibonacci_property(self.heap)
        self.assertTrue(result)

    def test_verify_degree_bound_empty(self):

        result = self.analyzer.verify_degree_bound(self.heap)
        self.assertTrue(result)

    def test_verify_degree_bound_simple(self):

        # Insert elements and perform operations
        for i in range(10):
            self.heap.insert(i)

        # Delete some to trigger consolidation
        for _ in range(3):
            self.heap.delete_min()

        result = self.analyzer.verify_degree_bound(self.heap)
        self.assertTrue(result)

    def test_analyze_potential_change(self):

        # Initial state
        initial_potential = self.heap.potential()

        # Perform insert operation
        node = self.heap.insert(10)
        analysis = self.analyzer.analyze_potential_change(self.heap, "insert", 0.001)

        self.assertEqual(analysis['operation'], "insert")
        self.assertEqual(analysis['potential_before'], initial_potential)
        self.assertEqual(analysis['potential_after'], self.heap.potential())
        self.assertEqual(analysis['potential_change'], 1)  # One new tree
        self.assertGreater(analysis['amortized_cost'], 0)

    def test_time_operation(self):

        def dummy_operation(x, y):
            return x + y

        result, time_taken = self.analyzer.time_operation(dummy_operation, 5, 3)

        self.assertEqual(result, 8)
        self.assertGreater(time_taken, 0)
        self.assertLess(time_taken, 1)  # Should be very fast

    def test_benchmark_operations_small(self):

        results = self.analyzer.benchmark_operations(10)

        # Check that all expected operations are benchmarked
        self.assertIn('insert', results)
        self.assertIn('find_min', results)
        self.assertIn('decrease_key', results)
        self.assertIn('delete_min', results)

        # Check insert results
        insert_results = results['insert']
        self.assertIn('avg_time', insert_results)
        self.assertIn('max_time', insert_results)
        self.assertIn('min_time', insert_results)
        self.assertIn('total_time', insert_results)

        # Times should be positive
        self.assertGreater(insert_results['avg_time'], 0)
        self.assertGreaterEqual(insert_results['max_time'], insert_results['avg_time'])
        self.assertLessEqual(insert_results['min_time'], insert_results['avg_time'])

    def test_complexity_analysis(self):

        sizes = [10, 20, 50]
        results = self.analyzer.complexity_analysis(sizes)

        self.assertEqual(results['sizes'], sizes)
        self.assertEqual(len(results['insert_times']), len(sizes))
        self.assertEqual(len(results['delete_min_times']), len(sizes))
        self.assertEqual(len(results['decrease_key_times']), len(sizes))

        # All times should be positive
        for times in results['insert_times']:
            self.assertGreater(times, 0)

    def test_theoretical_vs_actual_analysis_empty(self):

        analysis = self.analyzer.theoretical_vs_actual_analysis(self.heap)

        self.assertTrue(analysis['empty_heap'])

    def test_theoretical_vs_actual_analysis_non_empty(self):

        # Build heap
        for i in range(20):
            self.heap.insert(i)

        # Perform some operations
        for _ in range(5):
            self.heap.delete_min()

        analysis = self.analyzer.theoretical_vs_actual_analysis(self.heap)

        self.assertIn('heap_size', analysis)
        self.assertIn('num_trees', analysis)
        self.assertIn('num_marked', analysis)
        self.assertIn('potential', analysis)
        self.assertIn('theoretical_max_degree', analysis)
        self.assertIn('actual_max_degree', analysis)
        self.assertIn('degree_bound_satisfied', analysis)
        self.assertIn('fibonacci_property_satisfied', analysis)

        # Verify properties
        self.assertEqual(analysis['heap_size'], len(self.heap))
        self.assertEqual(analysis['num_trees'], self.heap.num_trees)
        self.assertEqual(analysis['num_marked'], self.heap.num_marked)
        self.assertEqual(analysis['potential'], self.heap.potential())
        self.assertTrue(analysis['degree_bound_satisfied'])
        self.assertTrue(analysis['fibonacci_property_satisfied'])

    def test_operation_counting(self):

        # Initially all counts should be zero
        for count in self.analyzer.operation_counts.values():
            self.assertEqual(count, 0)

        # Operation times should be empty
        for times in self.analyzer.operation_times.values():
            self.assertEqual(len(times), 0)

    def test_potential_history_tracking(self):

        # Initially empty
        self.assertEqual(len(self.analyzer.potential_history), 0)

        # Add some analysis
        self.heap.insert(10)
        self.analyzer.analyze_potential_change(self.heap, "insert", 0.001)

        self.assertEqual(len(self.analyzer.potential_history), 1)
        self.assertEqual(self.analyzer.potential_history[0], 1)

        # Add another
        self.heap.insert(5)
        self.analyzer.analyze_potential_change(self.heap, "insert", 0.001)

        self.assertEqual(len(self.analyzer.potential_history), 2)
        self.assertEqual(self.analyzer.potential_history[1], 2)

    def test_large_fibonacci_numbers(self):

        # Test some larger Fibonacci numbers
        test_cases = [
            (20, 6765),
            (25, 75025),
            (30, 832040)
        ]

        for n, expected in test_cases:
            result = self.analyzer.fibonacci_number(n)
            self.assertEqual(result, expected)

    def test_degree_bound_edge_cases(self):

        # Zero and negative sizes
        self.assertEqual(self.analyzer.max_degree_bound(0), 0)
        self.assertEqual(self.analyzer.max_degree_bound(-1), 0)

        # Very large size
        large_bound = self.analyzer.max_degree_bound(1000000)
        self.assertGreater(large_bound, 0)
        self.assertLess(large_bound, 50)  # Should be reasonable

if __name__ == '__main__':
    unittest.main()
