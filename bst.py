# Name: Michael Fitzgibbon
# OSU Email: fitzgibm@oregonstate.edu
# Course: CS261 - Data Structures
# Assignment: 4
# Due Date: 07/28/2025
# Description: A binary search tree and its corresponding methods, implemented in O(N) runtime complexity

import random
from queue_and_stack import Queue, Stack


class BSTNode:
    """
    Binary Search Tree Node class
    DO NOT CHANGE THIS CLASS IN ANY WAY
    """

    def __init__(self, value: object) -> None:
        """
        Initialize a new BST node
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        self.value = value  # to store node's data
        self.left = None    # pointer to root of left subtree
        self.right = None   # pointer to root of right subtree

    def __str__(self) -> str:
        """
        Override string method
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        return 'BST Node: {}'.format(self.value)


class BST:
    """Binary Search Tree class"""

    def __init__(self, start_tree=None) -> None:
        """
        Initialize new Binary Search Tree
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        self._root = None

        # populate BST with initial values (if provided)
        # before using this feature, implement add() method
        if start_tree is not None:
            for value in start_tree:
                self.add(value)

    def __str__(self) -> str:
        """
        Override string method; display in pre-order
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        values = []
        self._str_helper(self._root, values)
        return "BST pre-order { " + ", ".join(values) + " }"

    def _str_helper(self, node: BSTNode, values: []) -> None:
        """
        Helper method for __str__. Does pre-order tree traversal
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        if not node:
            return
        values.append(str(node.value))
        self._str_helper(node.left, values)
        self._str_helper(node.right, values)

    def get_root(self) -> BSTNode:
        """
        Return root of tree, or None if empty
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        return self._root

    def is_valid_bst(self) -> bool:
        """
        Perform pre-order traversal of the tree.
        Return False if nodes don't adhere to the bst ordering property.

        This is intended to be a troubleshooting method to help find any
        inconsistencies in the tree after the add() or remove() operations.
        A return of True from this method doesn't guarantee that your tree
        is the 'correct' result, just that it satisfies bst ordering.

        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        stack = Stack()
        stack.push(self._root)
        while not stack.is_empty():
            node = stack.pop()
            if node:
                if node.left and node.left.value >= node.value:
                    return False
                if node.right and node.right.value < node.value:
                    return False
                stack.push(node.right)
                stack.push(node.left)
        return True

    def print_tree(self):
        """
        Prints the tree using the print_subtree function.

        This method is intended to assist in visualizing the structure of the
        tree. You are encouraged to add this method to the tests in the Basic
        Testing section of the starter code or your own tests as needed.

        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        if self.get_root():
            self._print_subtree(self.get_root())
        else:
            print('(empty tree)')

    def _print_subtree(self, node, prefix: str = '', branch: str = ''):
        """
        Recursively prints the subtree rooted at this node.

        This is intended as a 'helper' method to assist in visualizing the
        structure of the tree.

        DO NOT CHANGE THIS METHOD IN ANY WAY
        """

        def add_junction(string):
            if len(string) < 2 or branch == '':
                return string
            junction = '|' if string[-2] == '|' else '`'
            return string[:-2] + junction + '-'

        if not node:
            print(add_junction(prefix) + branch + "None")
            return

        if len(prefix) > 2 * 16:
            print(add_junction(prefix) + branch + "(tree continues)")
            return

        if node.left or node.right:
            postfix = ' (root)' if branch == '' else ''
            print(add_junction(prefix) + branch + str(node.value) + postfix)
            self._print_subtree(node.right, prefix + '| ', 'R: ')
            self._print_subtree(node.left, prefix + '  ', 'L: ')
        else:
            print(add_junction(prefix) + branch + str(node.value) + ' (leaf)')

    # ------------------------------------------------------------------ #

    def add(self, value: object) -> None:
        """
        Adds a node of the provided value to the tree. Duplicates allowed, greater or equal values to right.

        args:
            value: The desired node value to be added
        returns:
            None
        """
        current = None
        node = self.get_root()
        while node is not None:
            current = node
            if value < node.value:
                node = node.left
            else:
                node = node.right

        new_node = BSTNode(value)

        if current is None:
            self._root = new_node
        else:
            if value < current.value:
                current.left = new_node
            else:
                current.right = new_node

    def remove(self, value: object) -> bool:
        """
        Removes a node from the tree of the corresponding value. Removes first encountered value.
        :param value: The value to remove from the tree
        :return: True if value removed, false if no value found
        """
        parent = None
        node = self.get_root()

        while node is not None:
            if node.value == value:
                #value found
                if node.left is None and node.right is None:
                    self._remove_no_subtrees(parent, node)
                    return True
                elif node.left is not None and node.right is not None:
                    self._remove_two_subtrees(parent, node)
                    return True
                else:
                    self._remove_one_subtree(parent, node)
                    return True
            elif value < node.value:
                parent = node
                node = node.left
            else:
                parent = node
                node = node.right

        return False

    def _remove_no_subtrees(self, remove_parent: BSTNode, remove_node: BSTNode) -> None:
        """
        For use in the remove method. Removes a node with no subtrees
        """
        # remove node that has no subtrees (no left or right nodes)
        #If none is provided as the parent, we are at the root
        if remove_parent is None:
            self._root = None
            return

        if remove_node.value < remove_parent.value:
            remove_parent.left = None
        else:
            remove_parent.right = None

    def _remove_one_subtree(self, remove_parent: BSTNode, remove_node: BSTNode) -> None:
        """
        For use in the remove method. Removes a node with one subtree
        """
        # remove node that has a left or right subtree (only)

        if remove_node.right is None:
            node = remove_node.left
        else:
            node = remove_node.right

        #If none is provided as the parent, we are at the root
        if remove_parent is None:
            self._root = node
            return

        if remove_node.value < remove_parent.value:
            remove_parent.left = node
        else:
            remove_parent.right = node

    def _remove_two_subtrees(self, remove_parent: BSTNode, remove_node: BSTNode) -> None:
        """
        For use in the remove method. Removes a node with 2 subtrees
        """
        # remove node that has two subtrees
        # need to find inorder successor and its parent

        successor_queue = self._inorder_successor(remove_node)
        successor = successor_queue.dequeue()
        parent = successor_queue.dequeue()

        successor.left = remove_node.left
        if remove_node.right.value != successor.value:
            parent.left = successor.right
            successor.right = remove_node.right

        #If none is provided as the parent, we are at the root
        if remove_parent is None:
            self._root = successor
            return

        if remove_node.value < remove_parent.value:
            remove_parent.left = successor
        else:
            remove_parent.right = successor

    def _inorder_successor(self, remove_node: BSTNode) -> Queue|BSTNode:
        """
        Determines the inorder successor for a given node. For use in removal of a node with 2 subtrees
        :param remove_node: The node to be removed
        :return: A queue of the inorder successor and its parent, in successor, parent order
        """
        parent = None
        current = None
        node = remove_node.right

        while node is not None:
            parent = current
            current = node
            node = current.left

        ret = Queue()

        ret.enqueue(current)
        ret.enqueue(parent)
        return ret



    def contains(self, value: object) -> bool:
        """
        Checks if a value is found in the tree.
        :param value: The value to find
        :return: True if found, False otherwise
        """
        node =self._root

        while node is not None:
            if node.value == value:
                return True
            elif node.value < value:
                node = node.right
            else:
                node = node.left

        return False

    def inorder_traversal(self) -> Queue:
        """
        Utilizes the recursive_inorder method to generate a Queue of the values of the tree in order.

        :return: Queue of sorted values
        """
        ret = Queue()

        self.recursive_inorder(self._root, ret)

        return ret



    def recursive_inorder(self, node: BSTNode, queue: Queue):
        """
        This is a recursive function that is intended to assist with the inorder traversal method
        :param node: Current node
        :param queue: The queue to add the result to
        :return: None, results are stored in passed queue.
        """
        if node is not None:
            self.recursive_inorder(node.left, queue)
            queue.enqueue(node.value)
            self.recursive_inorder(node.right, queue)




    def find_min(self) -> object:
        """
        Finds the left most node on the tree, the minimum value
        :return: The minimum node
        """
        if self.get_root() is None:
            return None

        node = self.get_root()

        while node is not None:
            if node.left is None:
                return node.value
            else:
                node = node.left

    def find_max(self) -> object:
        """
        Finds the right most node on the tree, the maximum value
        :return: The maximum node
        """
        if self.get_root() is None:
            return None

        node = self.get_root()

        while node is not None:
            if node.right is None:
                return node.value
            else:
                node = node.right

    def is_empty(self) -> bool:
        """
        Returns true if the tree is empty, false if not
        """
        if self.get_root() is not None:
            return False
        else:
            return True

    def make_empty(self) -> None:
        """
        Sets the root node to None, emptying the tree
        """
        self._root = None


# ------------------- BASIC TESTING -----------------------------------------


if __name__ == '__main__':

    print("\nPDF - method add() example 1")
    print("----------------------------")
    test_cases = (
        (1, 2, 3),
        (3, 2, 1),
        (1, 3, 2),
        (3, 1, 2),
    )
    for case in test_cases:
        tree = BST(case)
        print(tree)
        tree.print_tree()

    print("\nPDF - method add() example 2")
    print("----------------------------")
    test_cases = (
        (10, 20, 30, 40, 50),
        (10, 20, 30, 50, 40),
        (30, 20, 10, 5, 1),
        (30, 20, 10, 1, 5),
        (5, 4, 6, 3, 7, 2, 8),
        (range(0, 30, 3)),
        (range(0, 31, 3)),
        (range(0, 34, 3)),
        (range(10, -10, -2)),
        ('A', 'B', 'C', 'D', 'E'),
        (1, 1, 1, 1),
    )
    for case in test_cases:
        tree = BST(case)
        print('INPUT  :', case)
        print('RESULT :', tree)

    print("\nPDF - method add() example 3")
    print("----------------------------")
    for _ in range(100):
        case = list(set(random.randrange(1, 20000) for _ in range(900)))
        tree = BST()
        for value in case:
            tree.add(value)
        if not tree.is_valid_bst():
            raise Exception("PROBLEM WITH ADD OPERATION")
    print('add() stress test finished')

    print("\nPDF - method remove() example 1")
    print("-------------------------------")
    test_cases = (
        ((1, 2, 3), 1),
        ((1, 2, 3), 2),
        ((1, 2, 3), 3),
        ((50, 40, 60, 30, 70, 20, 80, 45), 0),
        ((50, 40, 60, 30, 70, 20, 80, 45), 45),
        ((50, 40, 60, 30, 70, 20, 80, 45), 40),
        ((50, 40, 60, 30, 70, 20, 80, 45), 30),
    )
    for case, del_value in test_cases:
        tree = BST(case)
        print('INPUT  :', tree, 'DEL:', del_value)
        tree.remove(del_value)
        print('RESULT :', tree)

    print("\nPDF - method remove() example 2")
    print("-------------------------------")
    test_cases = (
        ((50, 40, 60, 30, 70, 20, 80, 45), 20),
        ((50, 40, 60, 30, 70, 20, 80, 15), 40),
        ((50, 40, 60, 30, 70, 20, 80, 35), 20),
        ((50, 40, 60, 30, 70, 20, 80, 25), 40),
    )
    for case, del_value in test_cases:
        tree = BST(case)
        print('INPUT  :', tree, 'DEL:', del_value)
        tree.print_tree()
        tree.remove(del_value)
        print('RESULT :', tree)
        tree.print_tree()
        print('')

    print("\nPDF - method remove() example 3")
    print("-------------------------------")
    case = range(-9, 16, 2)
    tree = BST(case)
    for del_value in case:
        print('INPUT  :', tree, del_value)
        tree.remove(del_value)
        print('RESULT :', tree)

    print("\nPDF - method remove() example 4")
    print("-------------------------------")
    case = range(0, 34, 3)
    tree = BST(case)
    for _ in case[:-2]:
        root_value = tree.get_root().value
        print('INPUT  :', tree, root_value)
        tree.remove(root_value)
        if not tree.is_valid_bst():
            raise Exception("PROBLEM WITH REMOVE OPERATION")
        print('RESULT :', tree)

    print("\nPDF - method remove() example 5")
    print("-------------------------------")
    for _ in range(100):
        case = list(set(random.randrange(1, 20000) for _ in range(900)))
        tree = BST(case)
        for value in case[::2]:
            tree.remove(value)
        if not tree.is_valid_bst():
            raise Exception("PROBLEM WITH REMOVE OPERATION")
    print('remove() stress test finished')

    print("\nPDF - method contains() example 1")
    print("---------------------------------")
    tree = BST([10, 5, 15])
    print(tree.contains(15))
    print(tree.contains(-10))
    print(tree.contains(15))

    print("\nPDF - method contains() example 2")
    print("---------------------------------")
    tree = BST()
    print(tree.contains(0))

    print("\nPDF - method inorder_traversal() example 1")
    print("---------------------------------")
    tree = BST([10, 20, 5, 15, 17, 7, 12])
    print(tree.inorder_traversal())

    print("\nPDF - method inorder_traversal() example 2")
    print("---------------------------------")
    tree = BST([8, 10, -4, 5, -1])
    print(tree.inorder_traversal())

    print("\nPDF - method find_min() example 1")
    print("---------------------------------")
    tree = BST([10, 20, 5, 15, 17, 7, 12])
    print(tree)
    print("Minimum value is:", tree.find_min())

    print("\nPDF - method find_min() example 2")
    print("---------------------------------")
    tree = BST([8, 10, -4, 5, -1])
    print(tree)
    print("Minimum value is:", tree.find_min())

    print("\nPDF - method find_max() example 1")
    print("---------------------------------")
    tree = BST([10, 20, 5, 15, 17, 7, 12])
    print(tree)
    print("Maximum value is:", tree.find_max())

    print("\nPDF - method find_max() example 2")
    print("---------------------------------")
    tree = BST([8, 10, -4, 5, -1])
    print(tree)
    print("Maximum value is:", tree.find_max())

    print("\nPDF - method is_empty() example 1")
    print("---------------------------------")
    tree = BST([10, 20, 5, 15, 17, 7, 12])
    print("Tree is empty:", tree.is_empty())

    print("\nPDF - method is_empty() example 2")
    print("---------------------------------")
    tree = BST()
    print("Tree is empty:", tree.is_empty())

    print("\nPDF - method make_empty() example 1")
    print("---------------------------------")
    tree = BST([10, 20, 5, 15, 17, 7, 12])
    print("Tree before make_empty():", tree)
    tree.make_empty()
    print("Tree after make_empty(): ", tree)

    print("\nPDF - method make_empty() example 2")
    print("---------------------------------")
    tree = BST()
    print("Tree before make_empty():", tree)
    tree.make_empty()
    print("Tree after make_empty(): ", tree)
