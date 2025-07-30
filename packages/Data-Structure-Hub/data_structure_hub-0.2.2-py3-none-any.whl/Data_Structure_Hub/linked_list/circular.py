from typing import Any, Optional, Tuple, Union


class Node:
    """A node in a circular linked list.

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


class CircularLinkedList:
    """A circular linked list implementation.

    Attributes:
        head: The first node in the linked list.
        tail: The last node in the linked list.
        size: The number of nodes in the linked list.
    """

    def __init__(self, data: Any = None) -> None:
        """Initialize the circular linked list.

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
            'CircularLinkedList(head -> ... -> tail -> head)'
        """
        if self.is_empty:
            return "CircularLinkedList()"

        nodes = []
        current = self.head
        for _ in range(self._size):
            nodes.append(str(current.data))  # type: ignore
            current = current.next  # type: ignore
        return f"CircularLinkedList({' -> '.join(nodes)} -> head)"

    def append(self, data: Any) -> None:
        """Add a node with the given data at the end of the list.

        Args:
            data: The data to be stored in the new node.
        """
        new_node = Node(data)
        if self.is_empty:
            self.head = new_node
            self.tail = new_node
            new_node.next = new_node  # Circular reference
        else:
            new_node.next = self.head
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
            new_node.next = new_node  # Circular reference
        else:
            new_node.next = self.head
            self.head = new_node
            self.tail.next = new_node  # type: ignore
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
            self.tail.next = self.head  # type: ignore
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
            current.next = self.head  # type: ignore
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
        for _ in range(self._size - 1):
            if current.next.data == value:  # type: ignore
                if current.next == self.tail:  # type: ignore
                    self.tail = current
                current.next = current.next.next  # type: ignore
                self._size -= 1
                return True
            current = current.next  # type: ignore
        return False

    def search(self, value: Any) -> bool:
        """Check if a node with the given value exists in the list.

        Args:
            value: The value to search for.

        Returns:
            True if the value is found, False otherwise.
        """
        if self.is_empty:
            return False

        current = self.head
        for _ in range(self._size):
            if current.data == value:  # type: ignore
                return True
            current = current.next  # type: ignore
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
        if self.is_empty or self._size == 1:
            return

        prev = self.tail
        current = self.head
        next_node = current.next  # type: ignore

        for _ in range(self._size):
            current.next = prev  # type: ignore
            prev = current
            current = next_node
            next_node = current.next  # type: ignore

        self.head, self.tail = self.tail, self.head

    def to_list(self) -> list[Any]:
        """Convert the linked list to a Python list.

        Returns:
            A list containing all the data from the linked list nodes.
        """
        result = []
        if self.is_empty:
            return result

        current = self.head
        for _ in range(self._size):
            result.append(current.data)  # type: ignore
            current = current.next  # type: ignore
        return result

    def clear(self) -> None:
        """Empty the linked list by removing all nodes."""
        self.head = None
        self.tail = None
        self._size = 0

    def split_into_halves(self) -> Tuple['CircularLinkedList', 'CircularLinkedList']:
        """Split the circular list into two equal circular lists.

        If the number of nodes is odd, the first list will contain one more node.

        Returns:
            A tuple containing two new circular linked lists.
        """
        if self.is_empty:
            return CircularLinkedList(), CircularLinkedList()

        slow = self.head
        fast = self.head
        while fast.next != self.head and fast.next.next != self.head:  # type: ignore
            slow = slow.next  # type: ignore
            fast = fast.next.next  # type: ignore

        # Create first half
        first_list = CircularLinkedList()
        current = self.head
        first_tail = slow
        while current != first_tail.next:  # type: ignore
            first_list.append(current.data)  # type: ignore
            current = current.next  # type: ignore

        # Create second half
        second_list = CircularLinkedList()
        while current != self.head:  # type: ignore
            second_list.append(current.data)  # type: ignore
            current = current.next  # type: ignore

        return first_list, second_list

    def josephus_problem(self, step: int) -> Any:
        """Solve the Josephus problem using the circular linked list.

        Args:
            step: The counting step size for elimination.

        Returns:
            The data of the last remaining node.

        Raises:
            ValueError: If step is less than 1 or list is empty.
        """
        if step < 1:
            raise ValueError("Step must be at least 1")
        if self.is_empty:
            raise ValueError("List is empty")

        if self._size == 1:
            return self.head.data  # type: ignore

        current = self.head
        while self._size > 1:
            # Move to the node before the one to be eliminated
            for _ in range(step - 2):
                current = current.next  # type: ignore

            # Eliminate the next node
            node_to_remove = current.next  # type: ignore
            current.next = node_to_remove.next  # type: ignore
            self._size -= 1

            # Move to the next starting position
            current = current.next  # type: ignore

        # Update head and tail to the surviving node
        self.head = current
        self.tail = current
        self.tail.next = self.head  # type: ignore

        return current.data  # type: ignore
