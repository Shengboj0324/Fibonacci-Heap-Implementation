from typing import Optional, Any, List
import math

class FibonacciNode:
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
        siblings = [self]
        current = self.right
        while current != self:
            siblings.append(current)
            current = current.right

        return siblings

    def is_root(self) -> bool:
        return self.parent is None

    def is_leaf(self) -> bool:
        return self.child is None

    def subtree_size(self) -> int:
        size = 1
        if self.child is not None:
            current = self.child
            while True:
                size += current.subtree_size()
                current = current.right
                if current == self.child:
                    break

        return size

    def max_degree_in_subtree(self) -> int:
        max_deg = self.degree
        if self.child is not None:
            current = self.child
            while True:
                max_deg = max(max_deg, current.max_degree_in_subtree())
                current = current.right
                if current == self.child:
                    break

        return max_deg

    def verify_fibonacci_property(self) -> bool:
        # Fibonacci property: subtree of degree d has size ≥ F_{d+2}
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
