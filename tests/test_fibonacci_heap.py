

import unittest
import sys
import os

# Add parent directory to path for imports
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from fibonacci_heap.fibonacci_heap import FibonacciHeap
from fibonacci_heap.fibonacci_node import FibonacciNode

class TestFibonacciHeap(unittest.TestCase):

    def setUp(self):

        self.heap = FibonacciHeap()

    def test_empty_heap(self):

        self.assertTrue(self.heap.is_empty())
        self.assertEqual(len(self.heap), 0)
        self.assertFalse(bool(self.heap))
        self.assertIsNone(self.heap.find_min())
        self.assertEqual(self.heap.potential(), 0)
        self.assertEqual(self.heap.num_trees, 0)
        self.assertEqual(self.heap.num_marked, 0)

    def test_single_insert(self):

        node = self.heap.insert(10, "data10")

        self.assertFalse(self.heap.is_empty())
        self.assertEqual(len(self.heap), 1)
        self.assertTrue(bool(self.heap))
        self.assertEqual(self.heap.find_min(), node)
        self.assertEqual(self.heap.find_min().key, 10)
        self.assertEqual(self.heap.num_trees, 1)
        self.assertEqual(self.heap.potential(), 1)

    def test_multiple_inserts(self):

        nodes = []
        keys = [10, 5, 20, 3, 15, 8]

        for key in keys:
            node = self.heap.insert(key, f"data{key}")
            nodes.append(node)

        self.assertEqual(len(self.heap), 6)
        self.assertEqual(self.heap.find_min().key, 3)
        self.assertEqual(self.heap.num_trees, 6)

    def test_find_min_updates(self):

        # Insert in descending order
        self.heap.insert(20)
        self.assertEqual(self.heap.find_min().key, 20)

        self.heap.insert(15)
        self.assertEqual(self.heap.find_min().key, 15)

        self.heap.insert(10)
        self.assertEqual(self.heap.find_min().key, 10)

        self.heap.insert(5)
        self.assertEqual(self.heap.find_min().key, 5)

    def test_delete_min_empty(self):

        result = self.heap.delete_min()
        self.assertIsNone(result)

    def test_delete_min_single_element(self):

        node = self.heap.insert(10)

        result = self.heap.delete_min()

        self.assertEqual(result, node)
        self.assertEqual(result.key, 10)
        self.assertTrue(self.heap.is_empty())
        self.assertEqual(len(self.heap), 0)

    def test_delete_min_multiple_elements(self):

        keys = [10, 5, 20, 3, 15, 8]
        for key in keys:
            self.heap.insert(key)

        # Delete minimum elements in order
        expected_order = [3, 5, 8, 10, 15, 20]
        for expected_key in expected_order:
            min_node = self.heap.delete_min()
            self.assertEqual(min_node.key, expected_key)

        self.assertTrue(self.heap.is_empty())

    def test_delete_min_with_children(self):

        # Create a structure where min node has children
        nodes = []
        for key in [10, 20, 30, 5, 15, 25]:
            nodes.append(self.heap.insert(key))

        # Force some consolidation by deleting min
        min_node = self.heap.delete_min()
        self.assertEqual(min_node.key, 5)

        # Verify heap is still valid
        self.assertEqual(self.heap.find_min().key, 10)

    def test_decrease_key_basic(self):

        node1 = self.heap.insert(10)
        node2 = self.heap.insert(20)
        node3 = self.heap.insert(5)

        # Decrease key of node2
        self.heap.decrease_key(node2, 3)

        self.assertEqual(node2.key, 3)
        self.assertEqual(self.heap.find_min(), node2)

    def test_decrease_key_invalid(self):

        node = self.heap.insert(10)

        with self.assertRaises(ValueError):
            self.heap.decrease_key(node, 15)

    def test_decrease_key_cascading_cut(self):

        # Build a tree structure that will trigger cascading cuts
        root = self.heap.insert(1)
        child1 = self.heap.insert(10)
        child2 = self.heap.insert(20)
        grandchild = self.heap.insert(30)

        # Force tree structure by deleting min and rebuilding
        self.heap.delete_min()  # Remove node with key 1

        # Insert new minimum to force consolidation
        new_min = self.heap.insert(0)

        # Now test decrease_key that should trigger cuts
        self.heap.decrease_key(grandchild, -1)
        self.assertEqual(self.heap.find_min().key, -1)

    def test_delete_operation(self):

        nodes = []
        for key in [10, 20, 5, 15, 8]:
            nodes.append(self.heap.insert(key))

        # Delete middle element
        self.heap.delete(nodes[1])  # Delete node with key 20

        self.assertEqual(len(self.heap), 4)

        # Verify remaining elements
        remaining_keys = []
        while not self.heap.is_empty():
            remaining_keys.append(self.heap.delete_min().key)

        self.assertEqual(remaining_keys, [5, 8, 10, 15])

    def test_merge_empty_heaps(self):

        heap2 = FibonacciHeap()

        merged = self.heap.merge(heap2)

        self.assertTrue(merged.is_empty())
        self.assertEqual(len(merged), 0)

    def test_merge_with_empty(self):

        self.heap.insert(10)
        self.heap.insert(5)

        heap2 = FibonacciHeap()

        merged = self.heap.merge(heap2)

        self.assertEqual(len(merged), 2)
        self.assertEqual(merged.find_min().key, 5)

    def test_merge_non_empty_heaps(self):

        # First heap
        self.heap.insert(10)
        self.heap.insert(20)

        # Second heap
        heap2 = FibonacciHeap()
        heap2.insert(5)
        heap2.insert(15)

        merged = self.heap.merge(heap2)

        self.assertEqual(len(merged), 4)
        self.assertEqual(merged.find_min().key, 5)

        # Verify all elements are present
        keys = []
        while not merged.is_empty():
            keys.append(merged.delete_min().key)

        self.assertEqual(sorted(keys), [5, 10, 15, 20])

    def test_potential_function(self):

        # Empty heap
        self.assertEqual(self.heap.potential(), 0)

        # Single element
        self.heap.insert(10)
        self.assertEqual(self.heap.potential(), 1)  # 1 tree, 0 marked

        # Multiple elements
        self.heap.insert(20)
        self.heap.insert(5)
        self.assertEqual(self.heap.potential(), 3)  # 3 trees, 0 marked

    def test_consolidation_reduces_trees(self):

        # Insert many elements
        for i in range(10):
            self.heap.insert(i)

        initial_trees = self.heap.num_trees

        # Delete min should trigger consolidation
        self.heap.delete_min()

        # Should have fewer trees after consolidation
        self.assertLess(self.heap.num_trees, initial_trees)

    def test_heap_property_maintained(self):

        import random

        # Insert random elements
        keys = list(range(20))
        random.shuffle(keys)

        nodes = []
        for key in keys:
            nodes.append(self.heap.insert(key))

        # Perform random operations
        for _ in range(10):
            if random.choice([True, False]) and not self.heap.is_empty():
                # Delete min
                min_node = self.heap.delete_min()
                self.assertIsNotNone(min_node)
            else:
                # Insert new element
                new_key = random.randint(100, 200)
                self.heap.insert(new_key)

        # Verify heap property by extracting all elements in order
        extracted_keys = []
        while not self.heap.is_empty():
            extracted_keys.append(self.heap.delete_min().key)

        # Should be in sorted order
        self.assertEqual(extracted_keys, sorted(extracted_keys))

    def test_stress_operations(self):

        import random

        nodes = []

        # Insert 100 elements
        for i in range(100):
            node = self.heap.insert(random.randint(1, 1000))
            nodes.append(node)

        # Perform decrease_key operations
        for _ in range(20):
            if nodes:
                node = random.choice(nodes)
                try:
                    new_key = node.key - random.randint(1, 10)
                    self.heap.decrease_key(node, new_key)
                except ValueError:
                    pass  # Invalid decrease, ignore

        # Delete some elements
        for _ in range(30):
            if not self.heap.is_empty():
                self.heap.delete_min()

        # Verify heap is still valid
        self.assertGreaterEqual(len(self.heap), 0)
        if not self.heap.is_empty():
            self.assertIsNotNone(self.heap.find_min())

if __name__ == '__main__':
    unittest.main()
