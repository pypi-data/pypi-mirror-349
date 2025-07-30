from __future__ import annotations
from typing import Any, Optional, List, Union
from collections import deque
import sys


class BinarySearchTree:
    """A binary search tree implementation with comprehensive operations."""

    def __init__(self, value: Any) -> None:
        """Initialize a BST node with the given value.

        Args:
            value: The value to be stored in the node.
        """
        self.value = value
        self.left: Optional[BinarySearchTree] = None
        self.right: Optional[BinarySearchTree] = None
        # For easier rotations and successor/predecessor
        self.parent: Optional[BinarySearchTree] = None

    def insert(self, value: Any) -> BinarySearchTree:
        """Insert a value into the BST following BST rules.

        Args:
            value: The value to be inserted.

        Returns:
            The newly inserted node.
        """
        if value < self.value:
            if self.left is None:
                self.left = BinarySearchTree(value)
                self.left.parent = self
                return self.left
            else:
                return self.left.insert(value)
        else:
            if self.right is None:
                self.right = BinarySearchTree(value)
                self.right.parent = self
                return self.right
            else:
                return self.right.insert(value)

    def delete(self, value: Any) -> Optional[BinarySearchTree]:
        """Delete a node with the given value from the BST.

        Args:
            value: The value to be deleted.

        Returns:
            The root of the modified tree or None if the value wasn't found.
        """
        node = self.find(value)
        if not node:
            return None

        # Case 1: Node has no children
        if not node.left and not node.right:
            self._replace_node_in_parent(node, None)
        # Case 2: Node has one child
        elif node.left and not node.right:
            self._replace_node_in_parent(node, node.left)
        elif node.right and not node.left:
            self._replace_node_in_parent(node, node.right)
        # Case 3: Node has two children
        else:
            successor = node.right.find_min()
            node.value = successor.value
            return node.right.delete(successor.value)

        return self

    def _replace_node_in_parent(self, node: BinarySearchTree, new_node: Optional[BinarySearchTree]) -> None:
        """Helper method to replace a node in its parent with another node."""
        if node.parent:
            if node.parent.left == node:
                node.parent.left = new_node
            else:
                node.parent.right = new_node
        if new_node:
            new_node.parent = node.parent

    def find_min(self) -> BinarySearchTree:
        """Find the node with the minimum value in the BST.

        Returns:
            The node containing the minimum value.
        """
        current = self
        while current.left is not None:
            current = current.left
        return current

    def find_max(self) -> BinarySearchTree:
        """Find the node with the maximum value in the BST.

        Returns:
            The node containing the maximum value.
        """
        current = self
        while current.right is not None:
            current = current.right
        return current

    def is_valid(self) -> bool:
        """Check if the tree satisfies the BST property.

        Returns:
            True if the tree is a valid BST, False otherwise.
        """
        return self._is_valid_helper(-sys.maxsize, sys.maxsize)

    def _is_valid_helper(self, min_val: Any, max_val: Any) -> bool:
        """Helper method for BST validation.

        Args:
            min_val: The minimum allowed value for this subtree.
            max_val: The maximum allowed value for this subtree.

        Returns:
            True if the subtree is valid, False otherwise.
        """
        if not (min_val < self.value < max_val):
            return False

        left_valid = self.left._is_valid_helper(
            min_val, self.value) if self.left else True
        right_valid = self.right._is_valid_helper(
            self.value, max_val) if self.right else True

        return left_valid and right_valid

    def balance(self) -> BinarySearchTree:
        """Balance the BST using Day-Stout-Warren algorithm.

        Returns:
            The root of the balanced tree.
        """
        nodes = []
        self._store_nodes_in_order(self, nodes)
        return self._build_balanced_tree(nodes, 0, len(nodes) - 1)

    def _store_nodes_in_order(self, node: Optional[BinarySearchTree], nodes: List[BinarySearchTree]) -> None:
        """Store nodes in order in a list."""
        if node is None:
            return
        self._store_nodes_in_order(node.left, nodes)
        nodes.append(node)
        self._store_nodes_in_order(node.right, nodes)

    def _build_balanced_tree(self, nodes: List[BinarySearchTree], start: int, end: int) -> BinarySearchTree:
        """Build a balanced tree from sorted nodes."""
        if start > end:
            return None

        mid = (start + end) // 2
        node = nodes[mid]

        node.left = self._build_balanced_tree(nodes, start, mid - 1)
        if node.left:
            node.left.parent = node

        node.right = self._build_balanced_tree(nodes, mid + 1, end)
        if node.right:
            node.right.parent = node

        return node

    def successor(self, value: Any) -> Optional[BinarySearchTree]:
        """Find the in-order successor of the node with given value.

        Args:
            value: The value whose successor is to be found.

        Returns:
            The successor node or None if no successor exists.
        """
        node = self.find(value)
        if not node:
            return None

        # Case 1: Node has right subtree
        if node.right is not None:
            return node.right.find_min()

        # Case 2: No right subtree - go up until we find a parent that's a left child
        current = node
        parent = node.parent
        while parent is not None and current == parent.right:
            current = parent
            parent = parent.parent
        return parent

    def predecessor(self, value: Any) -> Optional[BinarySearchTree]:
        """Find the in-order predecessor of the node with given value.

        Args:
            value: The value whose predecessor is to be found.

        Returns:
            The predecessor node or None if no predecessor exists.
        """
        node = self.find(value)
        if not node:
            return None

        # Case 1: Node has left subtree
        if node.left is not None:
            return node.left.find_max()

        # Case 2: No left subtree - go up until we find a parent that's a right child
        current = node
        parent = node.parent
        while parent is not None and current == parent.left:
            current = parent
            parent = parent.parent
        return parent

    # Binary Tree methods (from binary_tree.py) with BST-specific optimizations

    def height(self) -> int:
        """Calculate the height of the BST.

        Returns:
            The height of the tree.
        """
        left_height = self.left.height() if self.left else -1
        right_height = self.right.height() if self.right else -1
        return max(left_height, right_height) + 1

    @property
    def size(self) -> int:
        """Count all nodes in the BST.

        Returns:
            The total number of nodes in the tree.
        """
        left_size = self.left.size if self.left else 0
        right_size = self.right.size if self.right else 0
        return left_size + right_size + 1

    @property
    def is_empty(self) -> bool:
        """Check if the BST is empty.

        Returns:
            True if the tree is empty, False otherwise.
        """
        return self.size == 0

    def preorder(self) -> List[Any]:
        """Return the preorder traversal of the BST.

        Returns:
            A list of node values in preorder (Root, Left, Right).
        """
        result = [self.value]
        if self.left:
            result.extend(self.left.preorder())
        if self.right:
            result.extend(self.right.preorder())
        return result

    def inorder(self) -> List[Any]:
        """Return the inorder traversal of the BST (which will be sorted).

        Returns:
            A list of node values in inorder (Left, Root, Right).
        """
        result = []
        if self.left:
            result.extend(self.left.inorder())
        result.append(self.value)
        if self.right:
            result.extend(self.right.inorder())
        return result

    def postorder(self) -> List[Any]:
        """Return the postorder traversal of the BST.

        Returns:
            A list of node values in postorder (Left, Right, Root).
        """
        result = []
        if self.left:
            result.extend(self.left.postorder())
        if self.right:
            result.extend(self.right.postorder())
        result.append(self.value)
        return result

    def level_order(self) -> List[Any]:
        """Return the level-order (BFS) traversal of the BST.

        Returns:
            A list of node values in level-order.
        """
        result = []
        queue = deque([self])
        while queue:
            node = queue.popleft()
            result.append(node.value)
            if node.left:
                queue.append(node.left)
            if node.right:
                queue.append(node.right)
        return result

    def is_balanced(self) -> bool:
        """Check if the BST is height-balanced.

        Returns:
            True if the tree is balanced, False otherwise.
        """
        if not self.left and not self.right:
            return True

        left_height = self.left.height() if self.left else -1
        right_height = self.right.height() if self.right else -1

        if abs(left_height - right_height) > 1:
            return False

        left_balanced = self.left.is_balanced() if self.left else True
        right_balanced = self.right.is_balanced() if self.right else True

        return left_balanced and right_balanced

    def is_complete(self) -> bool:
        """Check if the BST is complete.

        Returns:
            True if the tree is complete, False otherwise.
        """
        queue = deque([self])
        seen_null = False
        while queue:
            node = queue.popleft()
            if node is None:
                seen_null = True
                continue
            if seen_null:
                return False
            queue.append(node.left)
            queue.append(node.right)
        return True

    def is_perfect(self) -> bool:
        """Check if the BST is perfect.

        Returns:
            True if the tree is perfect, False otherwise.
        """
        height = self.height()
        return self._is_perfect_helper(height, 0)

    def _is_perfect_helper(self, height: int, level: int) -> bool:
        """Helper method for is_perfect()."""
        if not self.left and not self.right:
            return height == level

        if not self.left or not self.right:
            return False

        return (self.left._is_perfect_helper(height, level + 1) and
                self.right._is_perfect_helper(height, level + 1))

    def find(self, value: Any) -> Optional[BinarySearchTree]:
        """Find a node with the given value in the BST.

        Args:
            value: The value to search for.

        Returns:
            The node containing the value, or None if not found.
        """
        if self.value == value:
            return self
        elif value < self.value and self.left:
            return self.left.find(value)
        elif value > self.value and self.right:
            return self.right.find(value)
        return None

    def lowest_common_ancestor(self, a: Any, b: Any) -> Optional[BinarySearchTree]:
        """Find the lowest common ancestor of two nodes in the BST.

        Args:
            a: Value of the first node.
            b: Value of the second node.

        Returns:
            The LCA node, or None if one or both values aren't present.
        """
        node_a = self.find(a)
        node_b = self.find(b)
        if not node_a or not node_b:
            return None

        current = self
        while current:
            if a < current.value and b < current.value:
                current = current.left
            elif a > current.value and b > current.value:
                current = current.right
            else:
                return current
        return None
