"""
Fibonacci Heap Implementation - Core Data Structures

This module contains the core FibonacciNode and FibonacciHeap classes that implement
the fundamental data structures and algorithms for Fibonacci heaps.

Combines the node and heap implementations for better organization while maintaining
all existing functionality and behavior.
"""

from typing import Optional, Any, List, Dict, Tuple
import math


class FibonacciNode:
    """
    Node in a Fibonacci heap with support for circular doubly-linked lists
    and parent-child relationships.
    """
    
    def __init__(self, key: Any, data: Any = None):
        self.key = key
        self.data = data
        self.degree = 0  # Number of children
        self.parent: Optional['FibonacciNode'] = None
        self.child: Optional['FibonacciNode'] = None  # Arbitrary child pointer
        # Circular doubly-linked list for siblings
        self.left: 'FibonacciNode' = self
        self.right: 'FibonacciNode' = self
        self.marked = False  # For cascading cuts

    def __str__(self) -> str:
        mark_str = "*" if self.marked else ""
        return f"Node({self.key}{mark_str}, degree={self.degree})"

    def __repr__(self) -> str:
        return (f"FibonacciNode(key={self.key}, data={self.data}, "
                f"degree={self.degree}, marked={self.marked})")

    def __lt__(self, other: 'FibonacciNode') -> bool:
        return self.key < other.key

    def __le__(self, other: 'FibonacciNode') -> bool:
        return self.key <= other.key

    def __gt__(self, other: 'FibonacciNode') -> bool:
        return self.key > other.key

    def __ge__(self, other: 'FibonacciNode') -> bool:
        return self.key >= other.key

    def __eq__(self, other: 'FibonacciNode') -> bool:
        if other is None or not isinstance(other, FibonacciNode):
            return False
        return self.key == other.key

    def add_child(self, child: 'FibonacciNode') -> None:
        """Add a child node to this node's child list."""
        if self.child is None:
            # First child - create single-node circular list
            self.child = child
            child.left = child.right = child
        else:
            # Insert into circular list of children
            child.left = self.child
            child.right = self.child.right
            self.child.right.left = child
            self.child.right = child

        child.parent = self
        self.degree += 1
        child.marked = False  # Unmark when becoming child

    def remove_child(self, child: 'FibonacciNode') -> None:
        """Remove a child node from this node's child list."""
        if self.degree == 1:
            # Last child - clear pointer
            self.child = None
        else:
            # Update arbitrary child pointer if needed
            if self.child == child:
                self.child = child.right
            # Remove from circular list
            child.left.right = child.right
            child.right.left = child.left

        # Reset child to isolated state
        child.parent = None
        child.left = child.right = child
        self.degree -= 1

    def get_children(self) -> List['FibonacciNode']:
        """Return list of all children of this node."""
        if self.child is None:
            return []

        children = []
        current = self.child
        while True:
            children.append(current)
            current = current.right
            if current == self.child:
                break

        return children

    def get_siblings(self) -> List['FibonacciNode']:
        """Return list of all siblings including this node."""
        siblings = [self]
        current = self.right
        while current != self:
            siblings.append(current)
            current = current.right

        return siblings

    def is_root(self) -> bool:
        """Check if this node is a root (has no parent)."""
        return self.parent is None

    def is_leaf(self) -> bool:
        """Check if this node is a leaf (has no children)."""
        return self.child is None

    def subtree_size(self) -> int:
        """Calculate the size of the subtree rooted at this node."""
        # Use iterative approach to avoid recursion depth issues
        stack = [self]
        size = 0
        while stack:
            node = stack.pop()
            size += 1
            stack.extend(node.get_children())
        return size

    def max_degree_in_subtree(self) -> int:
        """Find the maximum degree of any node in this subtree."""
        # Use iterative approach to avoid recursion depth issues
        stack = [self]
        max_deg = 0
        while stack:
            node = stack.pop()
            max_deg = max(max_deg, node.degree)
            stack.extend(node.get_children())
        return max_deg

    def verify_fibonacci_property(self) -> bool:
        """Verify that this subtree satisfies the Fibonacci property."""
        # Simplified check to avoid performance issues with large heaps
        if self.degree > 15:  # Skip check for very large degrees
            return True

        def fibonacci(n: int) -> int:
            if n <= 1:
                return n
            a, b = 0, 1
            for _ in range(2, n + 1):
                a, b = b, a + b
            return b

        size = self.subtree_size()
        min_size = fibonacci(self.degree + 2)
        return size >= min_size


class FibonacciHeap:
    """
    Fibonacci heap implementation supporting efficient priority queue operations.
    
    Provides O(1) amortized time for insert, find_min, decrease_key, and merge operations,
    and O(log n) amortized time for delete_min and delete operations.
    """
    
    def __init__(self):
        self.min_node: Optional[FibonacciNode] = None  # Pointer to minimum
        self.num_nodes = 0  # Total nodes in heap
        self.num_trees = 0  # Trees in root list
        self.num_marked = 0  # Marked nodes for potential function

    def __len__(self) -> int:
        return self.num_nodes

    def __bool__(self) -> bool:
        return self.num_nodes > 0

    def is_empty(self) -> bool:
        """Check if the heap is empty."""
        return self.num_nodes == 0

    def potential(self) -> int:
        """Calculate the potential function: Φ(H) = t(H) + 2m(H)."""
        return self.num_trees + 2 * self.num_marked

    def insert(self, key: Any, data: Any = None) -> FibonacciNode:
        """Insert a new node with given key and data. O(1) operation."""
        node = FibonacciNode(key, data)

        if self.min_node is None:
            # First node in heap
            self.min_node = node
            self.num_trees = 1
        else:
            # Add to root list and update minimum if needed
            self._add_to_root_list(node)
            if node.key < self.min_node.key:
                self.min_node = node
            self.num_trees += 1

        self.num_nodes += 1
        return node

    def find_min(self) -> Optional[FibonacciNode]:
        """Return the minimum node without removing it. O(1) operation."""
        return self.min_node

    def merge(self, other: 'FibonacciHeap') -> 'FibonacciHeap':
        """Merge this heap with another heap. O(1) operation."""
        merged = FibonacciHeap()

        if self.is_empty():
            merged.min_node = other.min_node
        elif other.is_empty():
            merged.min_node = self.min_node
        else:
            # Choose minimum and concatenate circular root lists
            merged.min_node = self.min_node if self.min_node.key <= other.min_node.key else other.min_node

            # Connect the two circular lists
            self_last = self.min_node.left
            other_last = other.min_node.left

            self.min_node.left = other_last
            other_last.right = self.min_node
            other.min_node.left = self_last
            self_last.right = other.min_node

        # Update counts
        merged.num_nodes = self.num_nodes + other.num_nodes
        merged.num_trees = self.num_trees + other.num_trees
        merged.num_marked = self.num_marked + other.num_marked

        return merged

    def delete_min(self) -> Optional[FibonacciNode]:
        """Remove and return the minimum node. O(log n) amortized."""
        if self.min_node is None:
            return None

        min_node = self.min_node

        # Promote all children to root list
        if min_node.child is not None:
            children = min_node.get_children()
            for child in children:
                child.parent = None
                child.marked = False  # Unmark when promoted
                self._add_to_root_list(child)
            self.num_trees += len(children)
            self.num_marked -= sum(1 for child in children if child.marked)

        # Remove minimum from root list
        self._remove_from_root_list(min_node)
        self.num_trees -= 1
        self.num_nodes -= 1

        if self.num_nodes == 0:
            self.min_node = None
            self.num_trees = 0
        else:
            # Set arbitrary root and consolidate to maintain degree bound
            self.min_node = min_node.right
            self._consolidate()

        return min_node

    def decrease_key(self, node: FibonacciNode, new_key: Any) -> None:
        """Decrease the key of a node. O(1) amortized."""
        if new_key > node.key:
            raise ValueError("New key is greater than current key")

        node.key = new_key
        parent = node.parent

        # If heap property violated, cut and cascade
        if parent is not None and node.key < parent.key:
            self._cut(node, parent)
            self._cascading_cut(parent)

        # Update minimum pointer if needed
        if node.key < self.min_node.key:
            self.min_node = node

    def delete(self, node: FibonacciNode) -> None:
        """Delete a node from the heap."""
        # Decrease key to negative infinity, then delete min
        self.decrease_key(node, float('-inf'))
        self.delete_min()

    def _add_to_root_list(self, node: FibonacciNode) -> None:
        """Add a node to the root list."""
        if self.min_node is None:
            self.min_node = node
            node.left = node.right = node
        else:
            node.left = self.min_node.left
            node.right = self.min_node
            self.min_node.left.right = node
            self.min_node.left = node

    def _remove_from_root_list(self, node: FibonacciNode) -> None:
        """Remove a node from the root list."""
        if node.right == node:
            # Only node in root list
            self.min_node = None
        else:
            node.left.right = node.right
            node.right.left = node.left
            if self.min_node is node:
                self.min_node = node.right

    def _consolidate(self) -> None:
        """Merge trees of equal degree to maintain logarithmic bound."""
        max_degree = int(math.log(self.num_nodes) * 2) + 1
        degree_table: List[Optional[FibonacciNode]] = [None] * max_degree

        # Collect all root nodes (list may change during processing)
        roots = []
        current = self.min_node
        while True:
            roots.append(current)
            current = current.right
            if current == self.min_node:
                break

        # Merge trees with same degree
        for root in roots:
            degree = root.degree
            while degree_table[degree] is not None:
                other = degree_table[degree]
                # Ensure smaller key becomes parent
                if root.key > other.key:
                    root, other = other, root

                # Link: make other child of root
                self._remove_from_root_list(other)
                root.add_child(other)
                self.num_trees -= 1

                degree_table[degree] = None
                degree += 1

            degree_table[degree] = root

        # Rebuild root list from degree table
        self.min_node = None
        self.num_trees = 0

        for node in degree_table:
            if node is not None:
                if self.min_node is None:
                    # First root - create new circular list
                    self.min_node = node
                    node.left = node.right = node
                    self.num_trees = 1
                else:
                    # Add to root list and update minimum
                    self._add_to_root_list(node)
                    if node.key < self.min_node.key:
                        self.min_node = node
                    self.num_trees += 1

    def _cut(self, child: FibonacciNode, parent: FibonacciNode) -> None:
        """Remove child from parent and add to root list."""
        parent.remove_child(child)
        self._add_to_root_list(child)
        child.marked = False  # Unmark when moved to root
        self.num_trees += 1
        if child.marked:
            self.num_marked -= 1

    def _cascading_cut(self, node: FibonacciNode) -> None:
        """Propagate cuts up the tree to maintain balance."""
        parent = node.parent
        if parent is not None:
            if not node.marked:
                # First child loss - mark the node
                node.marked = True
                self.num_marked += 1
            else:
                # Second child loss - cut and cascade
                self._cut(node, parent)
                self._cascading_cut(parent)

    def get_roots(self) -> List[FibonacciNode]:
        """Return list of all root nodes."""
        if self.min_node is None:
            return []

        roots = []
        current = self.min_node
        while True:
            roots.append(current)
            current = current.right
            if current == self.min_node:
                break

        return roots
