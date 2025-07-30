from __future__ import annotations
from typing import Any, Optional, List, Union
from collections import deque


class BinaryTree:
    """A binary tree node class with various tree operations."""

    def __init__(self, value: Any) -> None:
        """Initialize a binary tree node with the given value.

        Args:
            value: The value to be stored in the node.
        """
        self.value = value
        self.left: Optional[BinaryTree] = None
        self.right: Optional[BinaryTree] = None

    def insert_left(self, value: Any) -> BinaryTree:
        """Insert a node as the left child of the current node.

        If a left child already exists, it will be pushed down as the left child
        of the new node.

        Args:
            value: The value to be inserted.

        Returns:
            The newly created left child node.
        """
        new_node = BinaryTree(value)
        if self.left is not None:
            new_node.left = self.left
        self.left = new_node
        return new_node

    def insert_right(self, value: Any) -> BinaryTree:
        """Insert a node as the right child of the current node.

        If a right child already exists, it will be pushed down as the right child
        of the new node.

        Args:
            value: The value to be inserted.

        Returns:
            The newly created right child node.
        """
        new_node = BinaryTree(value)
        if self.right is not None:
            new_node.right = self.right
        self.right = new_node
        return new_node

    def delete_left(self) -> None:
        """Remove the left subtree of the current node."""
        self.left = None

    def delete_right(self) -> None:
        """Remove the right subtree of the current node."""
        self.right = None

    def height(self) -> int:
        """Calculate the height of the tree.

        The height is the number of edges on the longest path from the node
        to a leaf. A leaf node has height 0.

        Returns:
            The height of the tree.
        """
        left_height = self.left.height() if self.left else -1
        right_height = self.right.height() if self.right else -1
        return max(left_height, right_height) + 1

    @property
    def size(self) -> int:
        """Count all nodes in the subtree rooted at this node.

        Returns:
            The total number of nodes in the subtree.
        """
        left_size = self.left.size if self.left else 0
        right_size = self.right.size if self.right else 0
        return left_size + right_size + 1

    @property
    def is_empty(self) -> bool:
        """Check if the tree is empty (has no nodes).

        Returns:
            True if the tree is empty, False otherwise.
        """
        return self.size == 0

    def preorder(self) -> List[Any]:
        """Return the preorder traversal of the tree.

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
        """Return the inorder traversal of the tree.

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
        """Return the postorder traversal of the tree.

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
        """Return the level-order (BFS) traversal of the tree.

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
        """Check if the tree is height-balanced.

        A tree is balanced if the heights of the two child subtrees of every
        node differ by at most one.

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
        """Check if the tree is a complete binary tree.

        A complete binary tree is one where all levels except possibly the last
        are completely filled, and all nodes are as far left as possible.

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
        """Check if the tree is a perfect binary tree.

        A perfect binary tree is one where all interior nodes have two children
        and all leaves are at the same level.

        Returns:
            True if the tree is perfect, False otherwise.
        """
        height = self.height()
        return self._is_perfect_helper(height, 0)

    def _is_perfect_helper(self, height: int, level: int) -> bool:
        """Helper method for is_perfect().

        Args:
            height: The height of the tree.
            level: The current level being checked.

        Returns:
            True if the subtree is perfect, False otherwise.
        """
        if not self.left and not self.right:
            return height == level

        if not self.left or not self.right:
            return False

        return (self.left._is_perfect_helper(height, level + 1) and
                self.right._is_perfect_helper(height, level + 1))

    def find(self, value: Any) -> Optional[BinaryTree]:
        """Find and return the node with the given value.

        Args:
            value: The value to search for.

        Returns:
            The node containing the value, or None if not found.
        """
        if self.value == value:
            return self

        left_result = self.left.find(value) if self.left else None
        if left_result:
            return left_result

        right_result = self.right.find(value) if self.right else None
        if right_result:
            return right_result

        return None

    def lowest_common_ancestor(self, a: Any, b: Any) -> Optional[BinaryTree]:
        """Find the lowest common ancestor of two nodes with values a and b.

        Args:
            a: Value of the first node.
            b: Value of the second node.

        Returns:
            The lowest common ancestor node, or None if one or both values
            are not present in the tree.
        """
        def lca_helper(node: Optional[BinaryTree], p: Any, q: Any) -> Optional[BinaryTree]:
            if not node:
                return None
            if node.value == p or node.value == q:
                return node
            left = lca_helper(node.left, p, q)
            right = lca_helper(node.right, p, q)
            if left and right:
                return node
            return left if left else right

        node_a = self.find(a)
        node_b = self.find(b)
        if not node_a or not node_b:
            return None
        return lca_helper(self, a, b)
