from __future__ import annotations
from typing import Any, Optional, List, Union
import sys


class Heap:
    """A heap implementation with both min-heap and max-heap functionality."""

    def __init__(self, heap_type: str = 'min') -> None:
        """Initialize the heap with specified type (min or max).

        Args:
            heap_type: Type of heap ('min' or 'max'). Defaults to 'min'.

        Raises:
            ValueError: If heap_type is neither 'min' nor 'max'.
        """
        if heap_type not in ('min', 'max'):
            raise ValueError("heap_type must be either 'min' or 'max'")
        self.heap_type = heap_type
        self.heap: List[Any] = []

    def _parent(self, index: int) -> int:
        """Get the parent index of a given node index.

        Args:
            index: The index of the node.

        Returns:
            The parent index.
        """
        return (index - 1) // 2

    def _left_child(self, index: int) -> int:
        """Get the left child index of a given node index.

        Args:
            index: The index of the node.

        Returns:
            The left child index.
        """
        return 2 * index + 1

    def _right_child(self, index: int) -> int:
        """Get the right child index of a given node index.

        Args:
            index: The index of the node.

        Returns:
            The right child index.
        """
        return 2 * index + 2

    def _compare(self, a: Any, b: Any) -> bool:
        """Compare two elements based on heap type.

        Args:
            a: First element to compare.
            b: Second element to compare.

        Returns:
            True if the comparison holds based on heap type.
        """
        if self.heap_type == 'min':
            return a < b
        return a > b

    def _sift_up(self, index: int) -> None:
        """Move the element at given index up to maintain heap property.

        Args:
            index: The index of the element to sift up.
        """
        while index > 0 and self._compare(
            self.heap[index],
            self.heap[self._parent(index)]
        ):
            parent = self._parent(index)
            self.heap[index], self.heap[parent] = self.heap[parent], self.heap[index]
            index = parent

    def _sift_down(self, index: int) -> None:
        """Move the element at given index down to maintain heap property.

        Args:
            index: The index of the element to sift down.
        """
        size = len(self.heap)
        while True:
            left = self._left_child(index)
            right = self._right_child(index)
            candidate = index

            if left < size and self._compare(self.heap[left], self.heap[candidate]):
                candidate = left

            if right < size and self._compare(self.heap[right], self.heap[candidate]):
                candidate = right

            if candidate == index:
                break

            self.heap[index], self.heap[candidate] = self.heap[candidate], self.heap[index]
            index = candidate

    def insert(self, value: Any) -> None:
        """Insert a value into the heap.

        Args:
            value: The value to be inserted.
        """
        self.heap.append(value)
        self._sift_up(len(self.heap) - 1)

    def extract_top(self) -> Any:
        """Remove and return the top element of the heap.

        Returns:
            The top element of the heap.

        Raises:
            IndexError: If the heap is empty.
        """
        if not self.heap:
            raise IndexError("Extract from empty heap")

        top = self.heap[0]
        last = self.heap.pop()
        if self.heap:
            self.heap[0] = last
            self._sift_down(0)
        return top

    def peek_top(self) -> Any:
        """Return the top element of the heap without removing it.

        Returns:
            The top element of the heap.

        Raises:
            IndexError: If the heap is empty.
        """
        if not self.heap:
            raise IndexError("Peek from empty heap")
        return self.heap[0]

    def heapify(self, array: List[Any]) -> None:
        """Create a heap from an array in O(n) time.

        Args:
            array: The array to transform into a heap.
        """
        self.heap = array.copy()
        for i in range(len(self.heap) // 2 - 1, -1, -1):
            self._sift_down(i)

    def merge(self, other_heap: Heap) -> Heap:
        """Merge this heap with another heap of the same type.

        Args:
            other_heap: Another heap to merge with.

        Returns:
            A new heap containing elements from both heaps.

        Raises:
            ValueError: If heap types don't match.
        """
        if self.heap_type != other_heap.heap_type:
            raise ValueError("Cannot merge heaps of different types")

        new_heap = Heap(self.heap_type)
        new_heap.heap = self.heap + other_heap.heap
        new_heap.heapify(new_heap.heap)
        return new_heap

    def decrease_key(self, index: int, new_value: Any) -> None:
        """Decrease the value of a key at the given index (for min-heap).

        Args:
            index: The index of the key to decrease.
            new_value: The new value for the key.

        Raises:
            IndexError: If index is out of bounds.
            ValueError: If new value is not appropriate for the operation.
        """
        if index < 0 or index >= len(self.heap):
            raise IndexError("Index out of bounds")

        if self.heap_type == 'min':
            if new_value > self.heap[index]:
                raise ValueError("New value must be smaller in a min-heap")
        else:  # max-heap
            if new_value < self.heap[index]:
                raise ValueError("New value must be larger in a max-heap")

        self.heap[index] = new_value
        self._sift_up(index)

    def increase_key(self, index: int, new_value: Any) -> None:
        """Increase the value of a key at the given index (for max-heap).

        Args:
            index: The index of the key to increase.
            new_value: The new value for the key.

        Raises:
            IndexError: If index is out of bounds.
            ValueError: If new value is not appropriate for the operation.
        """
        if index < 0 or index >= len(self.heap):
            raise IndexError("Index out of bounds")

        if self.heap_type == 'min':
            if new_value < self.heap[index]:
                raise ValueError("New value must be larger in a min-heap")
        else:  # max-heap
            if new_value > self.heap[index]:
                raise ValueError("New value must be smaller in a max-heap")

        self.heap[index] = new_value
        self._sift_down(index)

    @property
    def size(self) -> int:
        """Get the number of elements in the heap.

        Returns:
            The size of the heap.
        """
        return len(self.heap)

    @property
    def is_empty(self) -> bool:
        """Check if the heap is empty.

        Returns:
            True if the heap is empty, False otherwise.
        """
        return self.size == 0

    def __str__(self) -> str:
        """Return string representation of the heap.

        Returns:
            A string representation of the heap.
        """
        return str(self.heap)
