from __future__ import annotations
from typing import Any, Optional, Iterator, Tuple
from heapq import heappush, heappop, heapify


class Queue:
    """A standard FIFO queue implementation with comprehensive operations."""

    def __init__(self) -> None:
        """Initialize an empty queue."""
        self._items: list[Any] = []

    def enqueue(self, item: Any) -> None:
        """Add an item to the rear of the queue.

        Args:
            item: The item to be added to the queue.
        """
        self._items.append(item)

    def dequeue(self) -> Any:
        """Remove and return the front item from the queue.

        Returns:
            The front item of the queue.

        Raises:
            IndexError: If queue is empty.
        """
        if self.is_empty():
            raise IndexError("Dequeue from empty queue")
        return self._items.pop(0)

    def peek_front(self) -> Any:
        """Return the front item without removing it from the queue.

        Returns:
            The front item of the queue.

        Raises:
            IndexError: If queue is empty.
        """
        if self.is_empty():
            raise IndexError("Peek from empty queue")
        return self._items[0]

    def peek_rear(self) -> Any:
        """Return the rear item without removing it from the queue.

        Returns:
            The rear item of the queue.

        Raises:
            IndexError: If queue is empty.
        """
        if self.is_empty():
            raise IndexError("Peek from empty queue")
        return self._items[-1]

    def is_empty(self) -> bool:
        """Check if the queue is empty.

        Returns:
            True if queue is empty, False otherwise.
        """
        return len(self._items) == 0

    @property
    def size(self) -> int:
        """Get the number of items in the queue.

        Returns:
            The number of items in the queue.
        """
        return len(self._items)

    def clear(self) -> None:
        """Remove all items from the queue."""
        self._items = []

    def __contains__(self, item: Any) -> bool:
        """Check if an item is present in the queue.

        Args:
            item: The item to check for membership.

        Returns:
            True if item is in queue, False otherwise.
        """
        return item in self._items

    def __iter__(self) -> Iterator[Any]:
        """Return an iterator for the queue (front to rear).

        Returns:
            An iterator object for the queue.
        """
        return iter(self._items)

    def __len__(self) -> int:
        """Return the size of the queue when len() is called.

        Returns:
            The number of items in the queue.
        """
        return self.size

    def __str__(self) -> str:
        """Return string representation of the queue.

        Returns:
            A string showing the queue from front to rear.
        """
        return f"Queue({self._items})"

    def __bool__(self) -> bool:
        """Return True if queue is not empty.

        Returns:
            True if queue has items, False if empty.
        """
        return not self.is_empty()


class PriorityQueue(Queue):
    """A priority queue implementation where items with higher priority dequeued first."""

    def __init__(self) -> None:
        """Initialize an empty priority queue."""
        super().__init__()
        self._items: list[Tuple[int, Any]] = []  # (priority, item) pairs
        self._entry_finder: dict[Any, int] = {}  # For tracking priorities

    def enqueue(self, item: Any, priority: int = 0) -> None:
        """Add an item to the queue with specified priority.

        Args:
            item: The item to be added.
            priority: The priority of the item (lower value = higher priority). Defaults to 0.
        """
        if item in self._entry_finder:
            self.change_priority(item, priority)
        else:
            entry = (priority, item)
            heappush(self._items, entry)
            self._entry_finder[item] = priority

    def dequeue(self) -> Any:
        """Remove and return the highest priority item from the queue.

        Returns:
            The item with highest priority (lowest priority value).

        Raises:
            IndexError: If queue is empty.
        """
        while self._items:
            priority, item = heappop(self._items)
            if item is not None:  # Handle removed items
                del self._entry_finder[item]
                return item
        raise IndexError("Dequeue from empty priority queue")

    def change_priority(self, item: Any, new_priority: int) -> None:
        """Change the priority of an existing item in the queue.

        Args:
            item: The item whose priority needs to be changed.
            new_priority: The new priority value.

        Raises:
            KeyError: If item is not found in queue.
        """
        if item not in self._entry_finder:
            raise KeyError(f"Item {item} not found in priority queue")

        # Mark the existing entry as removed
        self._entry_finder[item] = new_priority
        # Add new entry with updated priority
        heappush(self._items, (new_priority, item))

    def peek_highest_priority(self) -> Any:
        """Return the highest priority item without removing it.

        Returns:
            The item with highest priority (lowest priority value).

        Raises:
            IndexError: If queue is empty.
        """
        while self._items:
            priority, item = self._items[0]
            if item is not None:
                return item
            heappop(self._items)  # Remove dummy entries
        raise IndexError("Peek from empty priority queue")

    def __contains__(self, item: Any) -> bool:
        """Check if an item is present in the priority queue.

        Args:
            item: The item to check for membership.

        Returns:
            True if item is in queue, False otherwise.
        """
        return item in self._entry_finder


class CircularQueue(Queue):
    """A circular queue implementation with fixed capacity."""

    def __init__(self, capacity: int = 10) -> None:
        """Initialize an empty circular queue with specified capacity.

        Args:
            capacity: Maximum number of items the queue can hold. Defaults to 10.
        """
        super().__init__()
        self._capacity = capacity
        self._front = 0
        self._rear = -1
        self._size = 0
        self._items = [None] * capacity

    def enqueue(self, item: Any) -> None:
        """Add an item to the rear of the circular queue.

        Args:
            item: The item to be added.

        Raises:
            OverflowError: If queue is full.
        """
        if self.is_full():
            raise OverflowError("Circular queue is full")
        self._rear = (self._rear + 1) % self._capacity
        self._items[self._rear] = item
        self._size += 1

    def dequeue(self) -> Any:
        """Remove and return the front item from the circular queue.

        Returns:
            The front item of the queue.

        Raises:
            IndexError: If queue is empty.
        """
        if self.is_empty():
            raise IndexError("Dequeue from empty circular queue")
        item = self._items[self._front]
        self._front = (self._front + 1) % self._capacity
        self._size -= 1
        return item

    def peek_front(self) -> Any:
        """Return the front item without removing it from the queue.

        Returns:
            The front item of the queue.

        Raises:
            IndexError: If queue is empty.
        """
        if self.is_empty():
            raise IndexError("Peek from empty circular queue")
        return self._items[self._front]

    def peek_rear(self) -> Any:
        """Return the rear item without removing it from the queue.

        Returns:
            The rear item of the queue.

        Raises:
            IndexError: If queue is empty.
        """
        if self.is_empty():
            raise IndexError("Peek from empty circular queue")
        return self._items[self._rear]

    def is_full(self) -> bool:
        """Check if the circular queue has reached its capacity.

        Returns:
            True if queue is full, False otherwise.
        """
        return self._size == self._capacity

    def resize(self, new_size: int) -> None:
        """Resize the circular queue to new capacity.

        Args:
            new_size: The new capacity of the queue.

        Raises:
            ValueError: If new size is smaller than current number of items.
        """
        if new_size < self._size:
            raise ValueError(
                "New size cannot be smaller than current item count")

        new_items = [None] * new_size
        for i in range(self._size):
            new_items[i] = self._items[(self._front + i) % self._capacity]

        self._items = new_items
        self._capacity = new_size
        self._front = 0
        self._rear = self._size - 1

    def clear(self) -> None:
        """Remove all items from the queue and reset pointers."""
        self._items = [None] * self._capacity
        self._front = 0
        self._rear = -1
        self._size = 0

    @property
    def size(self) -> int:
        """Get the number of items in the circular queue.

        Returns:
            The number of items in the queue.
        """
        return self._size

    def __contains__(self, item: Any) -> bool:
        """Check if an item is present in the circular queue.

        Args:
            item: The item to check for membership.

        Returns:
            True if item is in queue, False otherwise.
        """
        for i in range(self._size):
            if self._items[(self._front + i) % self._capacity] == item:
                return True
        return False

    def __iter__(self) -> Iterator[Any]:
        """Return an iterator for the circular queue (front to rear).

        Returns:
            An iterator object for the queue.
        """
        for i in range(self._size):
            yield self._items[(self._front + i) % self._capacity]

    def __str__(self) -> str:
        """Return string representation of the circular queue.

        Returns:
            A string showing the queue from front to rear.
        """
        items = list(self)
        return f"CircularQueue(size={self._size}, capacity={self._capacity}, items={items})"
