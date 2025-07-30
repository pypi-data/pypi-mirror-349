# Data Structures Package 🧠⚡

**A Python library that makes data structures intuitive, efficient, and fun to use!**

![PyPI Version](https://img.shields.io/pypi/v/data-structures-pkg?color=blue)
![License](https://img.shields.io/pypi/l/data-structures-pkg?color=green)
![Python Versions](https://img.shields.io/pypi/pyversions/data-structures-pkg)

## Why Use This Package?

✅ **Battle-tested implementations** of essential data structures.  
✅ **Clean, readable code** with type hints and thorough docs.  
✅ **Zero dependencies** — works with vanilla Python.  
✅ **Perfect for learning** (students) or **production** (devs).

```python
from data_structures import Stack, AVLTree, SinglyLinkedList

stack = Stack()
stack.push("Hello, world!")  # That easy.
📦 Install
bash
pip install data-structures-pkg
🧩 What’s Inside?
Structure	Module Import Path	Key Features
Linked Lists	from data_structures.linked_list import *	Singly, Doubly, Circular variants
Trees	from data_structures.tree import *	Binary, BST, AVL, Heap
Graphs	from data_structures.graph import *	Directed, Weighted, Traversal utils
Stack/Queue	from data_structures import Stack, Queue	Thread-safe, O(1) operations


🚀 Quick Examples
1. Linked List
python
from data_structures.linked_list import SinglyLinkedList

ll = SinglyLinkedList()
ll.append(1)
ll.append(2)
print(ll)  # Output: [1 -> 2]
2. AVL Tree (Auto-Balancing)
python
from data_structures.tree import AVLTree

avl = AVLTree()
avl.insert(3)
avl.insert(1)
avl.insert(2)  # Automatically balances itself!
3. Weighted Graph
python
from data_structures.graph import WeightedGraph

wg = WeightedGraph()
wg.add_edge("A", "B", weight=4)
wg.dijkstra("A")  # Shortest path from A to all nodes
📚 Full Documentation
Explore detailed guides and API references:

Linked Lists

Trees

Graphs



🤝 Contributing
Love this package? Here’s how to help:

Star the repo ⭐

Report bugs or suggest features in Issues.

Submit a PR for improvements.

📜 License
MIT © Yashashvi bhardwaj
```
