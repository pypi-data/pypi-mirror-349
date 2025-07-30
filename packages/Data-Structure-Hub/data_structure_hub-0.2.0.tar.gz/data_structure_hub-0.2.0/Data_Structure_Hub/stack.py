from __future__ import annotations
from typing import Any, Optional, Iterator


class Stack:
    """A complete stack implementation with standard operations and iterability."""

    def __init__(self) -> None:
        """Initialize an empty stack."""
        self._items: list[Any] = []

    def push(self, item: Any) -> None:
        """Add an item to the top of the stack.

        Args:
            item: The item to be added to the stack.
        """
        self._items.append(item)

    def pop(self) -> Any:
        """Remove and return the top item from the stack.

        Returns:
            The top item of the stack.

        Raises:
            IndexError: If stack is empty.
        """
        if self.is_empty():
            raise IndexError("Pop from empty stack")
        return self._items.pop()

    def peek(self) -> Any:
        """Return the top item without removing it from the stack.

        Returns:
            The top item of the stack.

        Raises:
            IndexError: If stack is empty.
        """
        if self.is_empty():
            raise IndexError("Peek from empty stack")
        return self._items[-1]

    def is_empty(self) -> bool:
        """Check if the stack is empty.

        Returns:
            True if stack is empty, False otherwise.
        """
        return len(self._items) == 0

    @property
    def size(self) -> int:
        """Get the number of items in the stack.

        Returns:
            The number of items in the stack.
        """
        return len(self._items)

    def clear(self) -> None:
        """Remove all items from the stack."""
        self._items = []

    def __contains__(self, item: Any) -> bool:
        """Check if an item is present in the stack.

        Args:
            item: The item to check for membership.

        Returns:
            True if item is in stack, False otherwise.
        """
        return item in self._items

    def __iter__(self) -> Iterator[Any]:
        """Return an iterator for the stack (top to bottom).

        Returns:
            An iterator object for the stack.
        """
        return reversed(self._items)

    def __len__(self) -> int:
        """Return the size of the stack when len() is called.

        Returns:
            The number of items in the stack.
        """
        return self.size

    def __str__(self) -> str:
        """Return string representation of the stack.

        Returns:
            A string showing the stack from top to bottom.
        """
        return f"Stack({self._items[::-1]})"  # Show top first

    def __bool__(self) -> bool:
        """Return True if stack is not empty.

        Returns:
            True if stack has items, False if empty.
        """
        return not self.is_empty()
