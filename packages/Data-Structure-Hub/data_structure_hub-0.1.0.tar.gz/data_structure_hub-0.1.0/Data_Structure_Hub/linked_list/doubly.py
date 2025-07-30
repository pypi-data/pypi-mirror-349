from typing import Any, Optional, Union


class Node:
    """A node in a doubly linked list.

    Attributes:
        data: The data stored in the node.
        prev: Reference to the previous node in the list.
        next: Reference to the next node in the list.
    """

    def __init__(self, data: Any) -> None:
        """Initialize a node with the given data.

        Args:
            data: The data to be stored in the node.
        """
        self.data: Any = data
        self.prev: Optional['Node'] = None
        self.next: Optional['Node'] = None


class DoublyLinkedList:
    """A doubly linked list implementation.

    Attributes:
        head: The first node in the linked list.
        tail: The last node in the linked list.
        size: The number of nodes in the linked list.
    """

    def __init__(self, data: Any = None) -> None:
        """Initialize the doubly linked list.

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
            'DoublyLinkedList(head <-> ... <-> tail)'
        """
        nodes = []
        current = self.head
        while current:
            nodes.append(str(current.data))
            current = current.next
        return f"DoublyLinkedList({' <-> '.join(nodes)})" if nodes else "DoublyLinkedList()"

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
            new_node.prev = self.tail
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
            self.head.prev = new_node  # type: ignore
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
            if index <= self._size // 2:
                # Traverse from head
                current = self.head
                for _ in range(index - 1):
                    current = current.next  # type: ignore
            else:
                # Traverse from tail
                current = self.tail
                for _ in range(self._size - index):
                    current = current.prev  # type: ignore

            new_node.next = current.next  # type: ignore
            new_node.prev = current
            current.next.prev = new_node  # type: ignore
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
            self.head.prev = None  # type: ignore
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
            self.tail = self.tail.prev  # type: ignore
            self.tail.next = None  # type: ignore
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
            if index <= self._size // 2:
                # Traverse from head
                current = self.head
                for _ in range(index):
                    current = current.next  # type: ignore
            else:
                # Traverse from tail
                current = self.tail
                for _ in range(self._size - index - 1):
                    current = current.prev  # type: ignore

            data = current.data
            current.prev.next = current.next  # type: ignore
            current.next.prev = current.prev  # type: ignore
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

        current = self.head
        while current and current.data != value:
            current = current.next

        if current is None:
            return False

        if current == self.head:
            self.delete_front()
        elif current == self.tail:
            self.delete_end()
        else:
            current.prev.next = current.next  # type: ignore
            current.next.prev = current.prev  # type: ignore
            self._size -= 1
        return True

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

        if index <= self._size // 2:
            # Traverse from head
            current = self.head
            for _ in range(index):
                current = current.next  # type: ignore
        else:
            # Traverse from tail
            current = self.tail
            for _ in range(self._size - index - 1):
                current = current.prev  # type: ignore
        return current.data  # type: ignore

    def reverse(self) -> None:
        """Reverse the linked list in-place."""
        current = self.head
        self.head, self.tail = self.tail, self.head
        while current:
            current.prev, current.next = current.next, current.prev
            current = current.prev

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

    def add_before(self, node: Node, data: Any) -> None:
        """Insert a new node with the given data before the specified node.

        Args:
            node: The node before which to insert the new node.
            data: The data to be stored in the new node.

        Raises:
            ValueError: If the node is not in the list.
        """
        if node not in self:
            raise ValueError("Node not in list")

        if node == self.head:
            self.prepend(data)
        else:
            new_node = Node(data)
            new_node.prev = node.prev
            new_node.next = node
            node.prev.next = new_node  # type: ignore
            node.prev = new_node
            self._size += 1

    def add_after(self, node: Node, data: Any) -> None:
        """Insert a new node with the given data after the specified node.

        Args:
            node: The node after which to insert the new node.
            data: The data to be stored in the new node.

        Raises:
            ValueError: If the node is not in the list.
        """
        if node not in self:
            raise ValueError("Node not in list")

        if node == self.tail:
            self.append(data)
        else:
            new_node = Node(data)
            new_node.prev = node
            new_node.next = node.next
            node.next.prev = new_node  # type: ignore
            node.next = new_node
            self._size += 1

    def remove_node(self, node: Node) -> Any:
        """Remove the specified node from the list in O(1) time.

        Args:
            node: The node to be removed.

        Returns:
            The data from the removed node.

        Raises:
            ValueError: If the node is not in the list.
        """
        if node not in self:
            raise ValueError("Node not in list")

        if node == self.head:
            return self.delete_front()
        elif node == self.tail:
            return self.delete_end()
        else:
            node.prev.next = node.next  # type: ignore
            node.next.prev = node.prev  # type: ignore
            self._size -= 1
            return node.data

    def __contains__(self, node: Node) -> bool:
        """Check if the node exists in the list.

        Args:
            node: The node to check for existence.

        Returns:
            True if the node is in the list, False otherwise.
        """
        current = self.head
        while current:
            if current is node:
                return True
            current = current.next
        return False