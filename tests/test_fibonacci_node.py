

import unittest
import sys
import os

# Add parent directory to path for imports
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from fibonacci_heap.core import FibonacciNode

class TestFibonacciNode(unittest.TestCase):

    def setUp(self):

        self.node1 = FibonacciNode(10, "data1")
        self.node2 = FibonacciNode(20, "data2")
        self.node3 = FibonacciNode(5, "data3")
        self.node4 = FibonacciNode(15, "data4")

    def test_node_creation(self):

        node = FibonacciNode(42, "test_data")

        self.assertEqual(node.key, 42)
        self.assertEqual(node.data, "test_data")
        self.assertEqual(node.degree, 0)
        self.assertIsNone(node.parent)
        self.assertIsNone(node.child)
        self.assertEqual(node.left, node)
        self.assertEqual(node.right, node)
        self.assertFalse(node.marked)

    def test_node_comparison(self):

        node1 = FibonacciNode(10)
        node2 = FibonacciNode(20)
        node3 = FibonacciNode(10)

        self.assertTrue(node1 < node2)
        self.assertTrue(node1 <= node2)
        self.assertTrue(node2 > node1)
        self.assertTrue(node2 >= node1)
        self.assertTrue(node1 == node3)
        self.assertFalse(node1 == node2)

    def test_add_single_child(self):

        self.node1.add_child(self.node2)

        self.assertEqual(self.node1.degree, 1)
        self.assertEqual(self.node1.child, self.node2)
        self.assertEqual(self.node2.parent, self.node1)
        self.assertEqual(self.node2.left, self.node2)
        self.assertEqual(self.node2.right, self.node2)
        self.assertFalse(self.node2.marked)

    def test_add_multiple_children(self):

        self.node1.add_child(self.node2)
        self.node1.add_child(self.node3)
        self.node1.add_child(self.node4)

        self.assertEqual(self.node1.degree, 3)
        self.assertEqual(self.node2.parent, self.node1)
        self.assertEqual(self.node3.parent, self.node1)
        self.assertEqual(self.node4.parent, self.node1)

        # Check circular list structure
        children = self.node1.get_children()
        self.assertEqual(len(children), 3)
        self.assertIn(self.node2, children)
        self.assertIn(self.node3, children)
        self.assertIn(self.node4, children)

    def test_remove_child(self):

        # Add children first
        self.node1.add_child(self.node2)
        self.node1.add_child(self.node3)

        # Remove one child
        self.node1.remove_child(self.node2)

        self.assertEqual(self.node1.degree, 1)
        self.assertIsNone(self.node2.parent)
        self.assertEqual(self.node2.left, self.node2)
        self.assertEqual(self.node2.right, self.node2)

        children = self.node1.get_children()
        self.assertEqual(len(children), 1)
        self.assertIn(self.node3, children)
        self.assertNotIn(self.node2, children)

    def test_remove_last_child(self):

        self.node1.add_child(self.node2)
        self.node1.remove_child(self.node2)

        self.assertEqual(self.node1.degree, 0)
        self.assertIsNone(self.node1.child)
        self.assertIsNone(self.node2.parent)

    def test_get_children(self):

        # No children
        self.assertEqual(self.node1.get_children(), [])

        # Add children
        self.node1.add_child(self.node2)
        self.node1.add_child(self.node3)

        children = self.node1.get_children()
        self.assertEqual(len(children), 2)
        self.assertIn(self.node2, children)
        self.assertIn(self.node3, children)

    def test_get_siblings(self):

        # Single node
        siblings = self.node1.get_siblings()
        self.assertEqual(len(siblings), 1)
        self.assertEqual(siblings[0], self.node1)

        # Add to circular list
        self.node1.right = self.node2
        self.node2.left = self.node1
        self.node2.right = self.node3
        self.node3.left = self.node2
        self.node3.right = self.node1
        self.node1.left = self.node3

        siblings = self.node1.get_siblings()
        self.assertEqual(len(siblings), 3)
        self.assertIn(self.node1, siblings)
        self.assertIn(self.node2, siblings)
        self.assertIn(self.node3, siblings)

    def test_is_root(self):

        self.assertTrue(self.node1.is_root())

        self.node1.add_child(self.node2)
        self.assertTrue(self.node1.is_root())
        self.assertFalse(self.node2.is_root())

    def test_is_leaf(self):

        self.assertTrue(self.node1.is_leaf())

        self.node1.add_child(self.node2)
        self.assertFalse(self.node1.is_leaf())
        self.assertTrue(self.node2.is_leaf())

    def test_subtree_size(self):

        # Single node
        self.assertEqual(self.node1.subtree_size(), 1)

        # Add children
        self.node1.add_child(self.node2)
        self.assertEqual(self.node1.subtree_size(), 2)

        self.node1.add_child(self.node3)
        self.assertEqual(self.node1.subtree_size(), 3)

        # Add grandchild
        self.node2.add_child(self.node4)
        self.assertEqual(self.node1.subtree_size(), 4)
        self.assertEqual(self.node2.subtree_size(), 2)

    def test_max_degree_in_subtree(self):

        # Single node
        self.assertEqual(self.node1.max_degree_in_subtree(), 0)

        # Add children
        self.node1.add_child(self.node2)
        self.node1.add_child(self.node3)
        self.assertEqual(self.node1.max_degree_in_subtree(), 2)

        # Add grandchildren
        self.node2.add_child(self.node4)
        node5 = FibonacciNode(25)
        node6 = FibonacciNode(30)
        self.node2.add_child(node5)
        self.node2.add_child(node6)

        self.assertEqual(self.node1.max_degree_in_subtree(), 3)
        self.assertEqual(self.node2.max_degree_in_subtree(), 3)

    def test_fibonacci_property_verification(self):

        # Single node (degree 0, size 1, F_2 = 1)
        self.assertTrue(self.node1.verify_fibonacci_property())

        # Node with one child (degree 1, size 2, F_3 = 2)
        self.node1.add_child(self.node2)
        self.assertTrue(self.node1.verify_fibonacci_property())

        # Node with two children (degree 2, size 3, F_4 = 3)
        self.node1.add_child(self.node3)
        self.assertTrue(self.node1.verify_fibonacci_property())

        # Build larger tree to test property
        # Create tree of degree 3 with minimum required size (F_5 = 5)
        node5 = FibonacciNode(25)
        node6 = FibonacciNode(30)
        self.node1.add_child(self.node4)
        self.node2.add_child(node5)

        # Should still satisfy property
        self.assertTrue(self.node1.verify_fibonacci_property())

    def test_string_representations(self):

        node = FibonacciNode(42, "test")

        # Test __str__
        self.assertIn("42", str(node))
        self.assertIn("degree=0", str(node))

        # Test marked node
        node.marked = True
        self.assertIn("*", str(node))

        # Test __repr__
        repr_str = repr(node)
        self.assertIn("FibonacciNode", repr_str)
        self.assertIn("key=42", repr_str)
        self.assertIn("data=test", repr_str)

if __name__ == '__main__':
    unittest.main()
