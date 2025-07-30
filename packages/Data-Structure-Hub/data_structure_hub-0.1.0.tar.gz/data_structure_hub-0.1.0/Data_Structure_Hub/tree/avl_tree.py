from __future__ import annotations
from typing import Any, Optional, List
from collections import deque
import sys


class AVLTree:
    """An AVL tree implementation with self-balancing functionality."""

    def __init__(self, value: Any) -> None:
        """Initialize an AVL tree node with the given value.

        Args:
            value: The value to be stored in the node.
        """
        self.value = value
        self.left: Optional[AVLTree] = None
        self.right: Optional[AVLTree] = None
        self.parent: Optional[AVLTree] = None
        self.height: int = 1  # Height starts at 1 for leaf nodes

    def _update_height(self) -> None:
        """Update the height of the node based on children's heights."""
        left_height = self.left.height if self.left else 0
        right_height = self.right.height if self.right else 0
        self.height = max(left_height, right_height) + 1

    def _balance_factor(self, node: Optional[AVLTree]) -> int:
        """Calculate the balance factor of a node.

        Args:
            node: The node to calculate balance factor for.

        Returns:
            The balance factor (left_height - right_height).
            0 if node is None.
        """
        if not node:
            return 0
        left_height = node.left.height if node.left else 0
        right_height = node.right.height if node.right else 0
        return left_height - right_height

    def _rotate_left(self, z: AVLTree) -> AVLTree:
        """Perform a left rotation around the given node.

        Args:
            z: The node to rotate around.

        Returns:
            The new root of the subtree after rotation.
        """
        y = z.right
        if y is None:
            return z

        T2 = y.left

        # Perform rotation
        y.left = z
        z.right = T2

        # Update parents
        y.parent = z.parent
        z.parent = y
        if T2:
            T2.parent = z

        # Update heights
        z._update_height()
        y._update_height()

        return y

    def _rotate_right(self, z: AVLTree) -> AVLTree:
        """Perform a right rotation around the given node.

        Args:
            z: The node to rotate around.

        Returns:
            The new root of the subtree after rotation.
        """
        y = z.left
        if y is None:
            return z

        T3 = y.right

        # Perform rotation
        y.right = z
        z.left = T3

        # Update parents
        y.parent = z.parent
        z.parent = y
        if T3:
            T3.parent = z

        # Update heights
        z._update_height()
        y._update_height()

        return y

    def _rebalance(self, node: AVLTree) -> AVLTree:
        """Rebalance the tree starting from the given node up to the root.

        Args:
            node: The node to start rebalancing from.

        Returns:
            The new root of the subtree after rebalancing.
        """
        current = node
        new_root = node

        while current:
            current._update_height()
            balance = self._balance_factor(current)

            # Left Heavy
            if balance > 1:
                if self._balance_factor(current.left) < 0:
                    current.left = self._rotate_left(current.left)
                    if current.left:
                        current.left.parent = current
                new_root = self._rotate_right(current)
                current = new_root

            # Right Heavy
            elif balance < -1:
                if self._balance_factor(current.right) > 0:
                    current.right = self._rotate_right(current.right)
                    if current.right:
                        current.right.parent = current
                new_root = self._rotate_left(current)
                current = new_root

            # Move up to parent
            current = current.parent

        return new_root

    def insert(self, value: Any) -> AVLTree:
        """Insert a value into the AVL tree with automatic rebalancing.

        Args:
            value: The value to be inserted.

        Returns:
            The root of the tree after insertion and rebalancing.
        """
        if value < self.value:
            if self.left is None:
                self.left = AVLTree(value)
                self.left.parent = self
            else:
                self.left = self.left.insert(value)
        else:
            if self.right is None:
                self.right = AVLTree(value)
                self.right.parent = self
            else:
                self.right = self.right.insert(value)

        self._update_height()
        return self._rebalance(self)

    def delete(self, value: Any) -> Optional[AVLTree]:
        """Delete a value from the AVL tree with automatic rebalancing.

        Args:
            value: The value to be deleted.

        Returns:
            The root of the tree after deletion and rebalancing.
        """
        if value < self.value:
            if self.left:
                self.left = self.left.delete(value)
        elif value > self.value:
            if self.right:
                self.right = self.right.delete(value)
        else:
            # Node with only one child or no child
            if self.left is None:
                temp = self.right
                if temp:
                    temp.parent = self.parent
                return temp
            elif self.right is None:
                temp = self.left
                if temp:
                    temp.parent = self.parent
                return temp

            # Node with two children
            temp = self.right.find_min()
            self.value = temp.value
            self.right = self.right.delete(temp.value)

        self._update_height()
        return self._rebalance(self)

    # Inherited BST methods with AVL-specific adjustments

    def find_min(self) -> AVLTree:
        """Find the node with the minimum value in the AVL tree.

        Returns:
            The node containing the minimum value.
        """
        current = self
        while current.left is not None:
            current = current.left
        return current

    def find_max(self) -> AVLTree:
        """Find the node with the maximum value in the AVL tree.

        Returns:
            The node containing the maximum value.
        """
        current = self
        while current.right is not None:
            current = current.right
        return current

    def is_valid(self) -> bool:
        """Check if the tree satisfies both BST and AVL properties.

        Returns:
            True if the tree is a valid AVL tree, False otherwise.
        """
        if not super().is_valid():
            return False

        balance = self._balance_factor(self)
        if abs(balance) > 1:
            return False

        left_valid = self.left.is_valid() if self.left else True
        right_valid = self.right.is_valid() if self.right else True

        return left_valid and right_valid

    def balance(self) -> AVLTree:
        """Balance the AVL tree (already balanced by operations, but can force rebalance).

        Returns:
            The root of the balanced tree.
        """
        return self._rebalance(self)

    def successor(self, value: Any) -> Optional[AVLTree]:
        """Find the in-order successor of the node with given value.

        Args:
            value: The value whose successor is to be found.

        Returns:
            The successor node or None if no successor exists.
        """
        node = self.find(value)
        if not node:
            return None

        if node.right is not None:
            return node.right.find_min()

        current = node
        parent = node.parent
        while parent is not None and current == parent.right:
            current = parent
            parent = parent.parent
        return parent

    def predecessor(self, value: Any) -> Optional[AVLTree]:
        """Find the in-order predecessor of the node with given value.

        Args:
            value: The value whose predecessor is to be found.

        Returns:
            The predecessor node or None if no predecessor exists.
        """
        node = self.find(value)
        if not node:
            return None

        if node.left is not None:
            return node.left.find_max()

        current = node
        parent = node.parent
        while parent is not None and current == parent.left:
            current = parent
            parent = parent.parent
        return parent

    # Binary Tree methods with AVL-specific adjustments

    def height(self) -> int:
        """Get the height of the AVL tree.

        Returns:
            The height of the tree.
        """
        return self.height  # Now stored as instance variable

    @property
    def size(self) -> int:
        """Count all nodes in the AVL tree.

        Returns:
            The total number of nodes in the tree.
        """
        left_size = self.left.size if self.left else 0
        right_size = self.right.size if self.right else 0
        return left_size + right_size + 1

    def find(self, value: Any) -> Optional[AVLTree]:
        """Find a node with the given value in the AVL tree.

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

    # Traversal methods (same as BST but return type adjusted)
    def preorder(self) -> List[Any]:
        """Return the preorder traversal of the AVL tree.

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
        """Return the inorder traversal of the AVL tree (which will be sorted).

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
        """Return the postorder traversal of the AVL tree.

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
        """Return the level-order (BFS) traversal of the AVL tree.

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
