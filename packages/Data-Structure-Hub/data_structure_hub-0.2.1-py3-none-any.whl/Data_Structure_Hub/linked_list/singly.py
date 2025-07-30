from typing import Any, Optional, Union


class Node:
    """A node in a singly linked list.

    Attributes:
        data: The data stored in the node.
        next: Reference to the next node in the list.
    """

    def __init__(self, data: Any) -> None:
        """Initialize a node with the given data.

        Args:
            data: The data to be stored in the node.
        """
        self.data: Any = data
        self.next: Optional['Node'] = None


class SinglyLinkedList:
    """A singly linked list implementation.

    Attributes:
        head: The first node in the linked list.
        tail: The last node in the linked list.
        size: The number of nodes in the linked list.
    """

    def __init__(self, data: Any = None) -> None:
        """Initialize the linked list.

        Args:
            data: Optional initial data to populate the list with.
                  If provided, creates a list with one node containing this data.
        """
        self.head: Optional[Node] = None
        self.tail: Optional[Node] = None
        self._size: int = 0

        if data is not None:
            self.append(data)

    def __len__(self) -> int:
        """Return the number of nodes in the linked list.

        Returns:
            The size of the linked list.
        """
        return self._size

    @property
    def size(self) -> int:
        """Get the number of nodes in the linked list.

        Returns:
            The size of the linked list.
        """
        return self._size

    @property
    def is_empty(self) -> bool:
        """Check if the linked list is empty.

        Returns:
            True if the list is empty, False otherwise.
        """
        return self._size == 0

    def __repr__(self) -> str:
        """Return a string representation of the linked list.

        Returns:
            A string representing the linked list in the format:
            'SinglyLinkedList(head -> ... -> tail)'
        """
        nodes = []
        current = self.head
        while current:
            nodes.append(str(current.data))
            current = current.next
        return f"SinglyLinkedList({' -> '.join(nodes)})" if nodes else "SinglyLinkedList()"

    def append(self, data: Any) -> None:
        """Add a node with the given data at the end of the list.

        Args:
            data: The data to be stored in the new node.
        """
        new_node = Node(data)
        if self.is_empty:
            self.head = new_node
            self.tail = new_node
        else:
            self.tail.next = new_node  # type: ignore
            self.tail = new_node
        self._size += 1

    def prepend(self, data: Any) -> None:
        """Add a node with the given data at the beginning of the list.

        Args:
            data: The data to be stored in the new node.
        """
        new_node = Node(data)
        if self.is_empty:
            self.head = new_node
            self.tail = new_node
        else:
            new_node.next = self.head
            self.head = new_node
        self._size += 1

    def insert_at(self, index: int, data: Any) -> None:
        """Insert a node with the given data at the specified index.

        Args:
            index: The position at which to insert the new node.
            data: The data to be stored in the new node.

        Raises:
            IndexError: If the index is out of range.
        """
        if index < 0 or index > self._size:
            raise IndexError("Index out of range")

        if index == 0:
            self.prepend(data)
        elif index == self._size:
            self.append(data)
        else:
            new_node = Node(data)
            current = self.head
            for _ in range(index - 1):
                current = current.next  # type: ignore
            new_node.next = current.next  # type: ignore
            current.next = new_node  # type: ignore
            self._size += 1

    def delete_front(self) -> Any:
        """Remove and return the data from the first node in the list.

        Returns:
            The data from the removed node.

        Raises:
            IndexError: If the list is empty.
        """
        if self.is_empty:
            raise IndexError("List is empty")

        data = self.head.data  # type: ignore
        if self._size == 1:
            self.head = None
            self.tail = None
        else:
            self.head = self.head.next  # type: ignore
        self._size -= 1
        return data

    def delete_end(self) -> Any:
        """Remove and return the data from the last node in the list.

        Returns:
            The data from the removed node.

        Raises:
            IndexError: If the list is empty.
        """
        if self.is_empty:
            raise IndexError("List is empty")

        data = self.tail.data  # type: ignore
        if self._size == 1:
            self.head = None
            self.tail = None
        else:
            current = self.head
            while current.next != self.tail:  # type: ignore
                current = current.next  # type: ignore
            current.next = None  # type: ignore
            self.tail = current
        self._size -= 1
        return data

    def delete_at(self, index: int) -> Any:
        """Remove and return the data from the node at the specified index.

        Args:
            index: The position of the node to be removed.

        Returns:
            The data from the removed node.

        Raises:
            IndexError: If the index is out of range or the list is empty.
        """
        if index < 0 or index >= self._size:
            raise IndexError("Index out of range")

        if index == 0:
            return self.delete_front()
        elif index == self._size - 1:
            return self.delete_end()
        else:
            current = self.head
            for _ in range(index - 1):
                current = current.next  # type: ignore
            data = current.next.data  # type: ignore
            current.next = current.next.next  # type: ignore
            self._size -= 1
            return data

    def delete_value(self, value: Any) -> bool:
        """Remove the first occurrence of a node with the given value.

        Args:
            value: The value to be removed from the list.

        Returns:
            True if the value was found and removed, False otherwise.
        """
        if self.is_empty:
            return False

        if self.head.data == value:  # type: ignore
            self.delete_front()
            return True

        current = self.head
        while current.next and current.next.data != value:  # type: ignore
            current = current.next  # type: ignore

        if current.next and current.next.data == value:  # type: ignore
            if current.next == self.tail:
                self.tail = current
            current.next = current.next.next  # type: ignore
            self._size -= 1
            return True
        return False

    def search(self, value: Any) -> bool:
        """Check if a node with the given value exists in the list.

        Args:
            value: The value to search for.

        Returns:
            True if the value is found, False otherwise.
        """
        current = self.head
        while current:
            if current.data == value:
                return True
            current = current.next
        return False

    def get_at(self, index: int) -> Any:
        """Get the data from the node at the specified index.

        Args:
            index: The position of the node to retrieve data from.

        Returns:
            The data from the node at the specified index.

        Raises:
            IndexError: If the index is out of range.
        """
        if index < 0 or index >= self._size:
            raise IndexError("Index out of range")

        current = self.head
        for _ in range(index):
            current = current.next  # type: ignore
        return current.data  # type: ignore

    def reverse(self) -> None:
        """Reverse the linked list in-place."""
        prev = None
        current = self.head
        self.tail = self.head
        while current:
            next_node = current.next
            current.next = prev
            prev = current
            current = next_node
        self.head = prev

    def to_list(self) -> list[Any]:
        """Convert the linked list to a Python list.

        Returns:
            A list containing all the data from the linked list nodes.
        """
        result = []
        current = self.head
        while current:
            result.append(current.data)
            current = current.next
        return result

    def clear(self) -> None:
        """Empty the linked list by removing all nodes."""
        self.head = None
        self.tail = None
        self._size = 0