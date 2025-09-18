from typing import Optional, Any, List, Dict, Tuple
import math
from .fibonacci_node import FibonacciNode

class FibonacciHeap:
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
        return self.num_nodes == 0

    def potential(self) -> int:
        # Potential function: Φ(H) = t(H) + 2m(H)
        return self.num_trees + 2 * self.num_marked

    def insert(self, key: Any, data: Any = None) -> FibonacciNode:
        # O(1) operation - just add to root list
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
        return self.min_node

    def merge(self, other: 'FibonacciHeap') -> 'FibonacciHeap':
        # O(1) operation - concatenate root lists
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
        # O(log n) amortized - triggers consolidation
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
        # O(1) amortized - uses cascading cuts
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

        # Decrease key to negative infinity, then delete min
        self.decrease_key(node, float('-inf'))
        self.delete_min()

    def _add_to_root_list(self, node: FibonacciNode) -> None:

        if self.min_node is None:
            self.min_node = node
            node.left = node.right = node
        else:
            node.left = self.min_node.left
            node.right = self.min_node
            self.min_node.left.right = node
            self.min_node.left = node

    def _remove_from_root_list(self, node: FibonacciNode) -> None:

        if node.right == node:
            # Only node in root list
            self.min_node = None
        else:
            node.left.right = node.right
            node.right.left = node.left
            if self.min_node is node:
                self.min_node = node.right

    def _consolidate(self) -> None:
        # Merge trees of equal degree to maintain logarithmic bound
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
        # Remove child from parent and add to root list
        parent.remove_child(child)
        self._add_to_root_list(child)
        child.marked = False  # Unmark when moved to root
        self.num_trees += 1
        if child.marked:
            self.num_marked -= 1

    def _cascading_cut(self, node: FibonacciNode) -> None:
        # Propagate cuts up the tree to maintain balance
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