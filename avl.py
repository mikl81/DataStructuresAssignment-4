# Name: Michael Fitzgibbon
# OSU Email: fitzgibm@oregonstate.edu
# Course: CS261 - Data Structures
# Assignment: 4
# Due Date: 07/28/2025
# Description: A self balancing AVL tree


import random
from queue_and_stack import Queue, Stack
from bst import BSTNode, BST


class AVLNode(BSTNode):
    """
    AVL Tree Node class. Inherits from BSTNode
    DO NOT CHANGE THIS CLASS IN ANY WAY
    """

    def __init__(self, value: object) -> None:
        """
        Initialize a new AVL node
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        # call __init__() from parent class
        super().__init__(value)

        # new variables needed for AVL
        self.parent = None
        self.height = 0

    def __str__(self) -> str:
        """
        Override string method
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        return 'AVL Node: {}'.format(self.value)


class AVL(BST):
    """AVL Tree class. Inherits from BST"""

    def __init__(self, start_tree=None) -> None:
        """
        Initialize a new AVL Tree
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        # call __init__() from parent class
        super().__init__(start_tree)

    def __str__(self) -> str:
        """
        Override string method; display in pre-order
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        values = []
        super()._str_helper(self._root, values)
        return "AVL pre-order { " + ", ".join(values) + " }"

    def is_valid_avl(self) -> bool:
        """
        Perform pre-order traversal of the tree. Return False if there
        are any problems with attributes of any of the nodes in the tree.

        This is intended to be a troubleshooting 'helper' method to help
        find any inconsistencies in the tree after the add() or remove()
        operations. Review the code to understand what this method is
        checking and how it determines whether the AVL tree is correct.

        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        stack = Stack()
        stack.push(self._root)
        while not stack.is_empty():
            node = stack.pop()
            if node:
                # check for correct height (relative to children)
                left = node.left.height if node.left else -1
                right = node.right.height if node.right else -1
                if node.height != 1 + max(left, right):
                    return False

                if node.parent:
                    # parent and child pointers are in sync
                    if node.value < node.parent.value:
                        check_node = node.parent.left
                    else:
                        check_node = node.parent.right
                    if check_node != node:
                        return False
                else:
                    # NULL parent is only allowed on the root of the tree
                    if node != self._root:
                        return False
                stack.push(node.right)
                stack.push(node.left)
        return True

    # ---------------------------------------------------------------------- #

    def add(self, value: object) -> None:
        """
        Inserts a node in the tree, then rebalances all affected nodes in the tree.

        :param: The value to add to the tree, duplicate values not allowed
        :return: None
        """

        new_node = AVLNode(value) # Create node


        parent = None
        node = self.get_root()
        while node is not None:
            parent = node
            if value < node.value:
                node = node.left
            elif value > node.value:
                node = node.right
            else:
                #Duplicate values not allowed
                return

        #Here parent is the last node in the tree
        if parent:
            if value < parent.value:
                #Node belongs to the left of the parent node
                parent.left = new_node
                new_node.parent = parent
            else:
                #Node belongs to right
                parent.right = new_node
                new_node.parent = parent
        else:
            #No parent means new node is the root
            self._root = new_node

        while parent is not None:
            #Rebalance starting with the parent until we reach the root
            self._rebalance(parent)
            parent = parent.parent



    def remove(self, value: object) -> bool:
        """
        Removes a node of the specified value, and returns True if value is removed. False if no value found.
        """
        parent = None
        node = self.get_root()

        while node is not None:
            if node.value == value:
                # value found
                if node.left is None and node.right is None:
                    self._remove_no_subtrees(parent, node)
                    while parent is not None:
                        self._rebalance(parent)
                        parent = parent.parent
                    return True
                elif node.left is not None and node.right is not None:
                    successor = self._remove_two_subtrees(parent, node)
                    while parent is not None:
                        self._rebalance(parent)
                        parent = parent.parent
                    return True
                else:
                    self._remove_one_subtree(parent, node)
                    while parent is not None:
                        self._rebalance(parent)
                        parent = parent.parent
                    return True
            elif value < node.value:
                parent = node
                node = node.left
            else:
                parent = node
                node = node.right

        return False



    def _remove_two_subtrees(self, remove_parent: AVLNode, remove_node: AVLNode) -> AVLNode:
        """
        Removes
        """
        successor_queue = self._inorder_successor(remove_node)
        successor = successor_queue.dequeue()
        parent = successor_queue.dequeue()

        successor.left = remove_node.left
        if successor.left:
            successor.left.parent = successor

        if remove_node.right.value != successor.value:
            parent.left = successor.right
            if successor.right:
                successor.right.parent = parent
            successor.right = remove_node.right
            successor.right.parent = successor

        successor.parent = remove_parent

        # If none is provided as the parent, we are at the root
        if remove_parent is None:
            self._root = successor
            return successor

        if remove_node.value < remove_parent.value:
            remove_parent.left = successor
        else:
            remove_parent.right = successor


        self._update_height(successor)
        self._update_height(remove_node)
        return successor

    # It's highly recommended to implement                          #
    # the following methods for balancing the AVL Tree.             #
    # Remove these comments.                                        #
    # Remove these method stubs if you decide not to use them.      #
    # Change these methods in any way you'd like.                   #

    def _balance_factor(self, node: AVLNode) -> int:
        """
        Returns the balance factor of the node, defined as the weight of the right node minus the left
        :arg node: The node to calculate balance factor
        :return: The balance factor
        """
        #Empty nodes are balanced
        if not node:
            return 0
        return self._get_height(node.right) - self._get_height(node.left)

    def _get_height(self, node: AVLNode) -> int:
        """
        Returns the height of the node, -1 for null nodes
        :arg node: The node to check
        :return: Int of the node height
        """
        #empty nodes have a height of -1
        if not node:
            return -1
        return node.height

    def _rotate_left(self, node: AVLNode) -> AVLNode:
        """
        Performs a rotation to the left of the center node. Center node is defined as right of rotating node
        """

        center = node.right #Center is right of node
        node.right = center.left #Less than center is greater than node.right
        if node.right is not None:  #If we find value, assign parents
            node.right.parent = node
        center.left = node #Move the node to the left of the center node
        center.parent = node.parent #set the parents of the center to the original parents.
        node.parent = center #set the nodes parent to the center node
        self._update_height(node) #Update both the heights
        self._update_height(center)
        return center

    def _rotate_right(self, node: AVLNode) -> AVLNode:
        """
        Performs a rotation to the right of the center node. Center node is defined as left of rotating node
        """

        #See above implementation for logic
        center = node.left
        node.left = center.right
        if node.left is not None:
            node.left.parent = node
        center.right = node
        center.parent = node.parent
        node.parent = center
        self._update_height(node)
        self._update_height(center)
        return center

    def _update_height(self, node: AVLNode) -> None:
        """
        Updates the height as 1 plus the height of the highest child node
        """
        node.height = max(self._get_height(node.left), self._get_height(node.right))+1

    def _rebalance(self, node: AVLNode) -> None:
        """
        Rebalances a node by checking its balancing factor, then performing the appropriate rotations on the node
        """
        base_parent = node.parent
        base_balance = self._balance_factor(node)

        if base_balance < -1:
            #left heavy
            if self._balance_factor(node.left) > 0:
                #double rotation
                node.left = self._rotate_left(node.left)
                node.left.parent = node
            #Grab the new center node
            new_subroot = self._rotate_right(node)
            #Set its parents
            new_subroot.parent = base_parent
            #if the parent is Null, we are at root
            if base_parent is None:
                self._root = new_subroot
            else:
                #Check value and assign
                if new_subroot.value < base_parent.value:
                    base_parent.left = new_subroot
                else:
                    base_parent.right = new_subroot
        elif base_balance  > 1:
            #right heavy
            if self._balance_factor(node.right) < 0:
                #double rotation
                node.right = self._rotate_right(node.right)
                node.right.parent = node
            new_subroot = self._rotate_left(node)
            new_subroot.parent = base_parent
            if base_parent is None:
                self._root = new_subroot
            else:
                if new_subroot.value < base_parent.value:
                    base_parent.left = new_subroot
                else:
                    base_parent.right = new_subroot
            self._update_height(new_subroot)
        else:
            self._update_height(node)



# ------------------- BASIC TESTING -----------------------------------------


if __name__ == '__main__':

    print("\nPDF - method add() example 1")
    print("----------------------------")
    test_cases = (
        (1, 2, 3),  # RR
        (3, 2, 1),  # LL
        (1, 3, 2),  # RL
        (3, 1, 2),  # LR
    )
    for case in test_cases:
        tree = AVL(case)
        print(tree)
        tree.print_tree()

    print("\nPDF - method add() example 2")
    print("----------------------------")
    test_cases = (
        (10, 20, 30, 40, 50),   # RR, RR
        (10, 20, 30, 50, 40),   # RR, RL
        (30, 20, 10, 5, 1),     # LL, LL
        (30, 20, 10, 1, 5),     # LL, LR
        (5, 4, 6, 3, 7, 2, 8),  # LL, RR
        (range(0, 30, 3)),
        (range(0, 31, 3)),
        (range(0, 34, 3)),
        (range(10, -10, -2)),
        ('A', 'B', 'C', 'D', 'E'),
        (1, 1, 1, 1),
    )
    for case in test_cases:
        tree = AVL(case)
        print('INPUT  :', case)
        print('RESULT :', tree)

    print("\nPDF - method add() example 3")
    print("----------------------------")
    for _ in range(100):
        case = list(set(random.randrange(1, 20000) for _ in range(900)))
        tree = AVL()
        for value in case:
            tree.add(value)
        if not tree.is_valid_avl():
            raise Exception("PROBLEM WITH ADD OPERATION")
    print('add() stress test finished')

    print("\nPDF - method remove() example 1")
    print("-------------------------------")
    test_cases = (
        ((1, 2, 3), 1),  # no AVL rotation
        ((1, 2, 3), 2),  # no AVL rotation
        ((1, 2, 3), 3),  # no AVL rotation
        ((50, 40, 60, 30, 70, 20, 80, 45), 0),
        ((50, 40, 60, 30, 70, 20, 80, 45), 45),  # no AVL rotation
        ((50, 40, 60, 30, 70, 20, 80, 45), 40),  # no AVL rotation
        ((50, 40, 60, 30, 70, 20, 80, 45), 30),  # no AVL rotation
    )
    for case, del_value in test_cases:
        tree = AVL(case)
        print('INPUT  :', tree, 'DEL:', del_value)
        tree.remove(del_value)
        print('RESULT :', tree)

    print("\nPDF - method remove() example 2")
    print("-------------------------------")
    test_cases = (
        ((50, 40, 60, 30, 70, 20, 80, 45), 20),  # RR
        ((50, 40, 60, 30, 70, 20, 80, 15), 40),  # LL
        ((50, 40, 60, 30, 70, 20, 80, 35), 20),  # RL
        ((50, 40, 60, 30, 70, 20, 80, 25), 40),  # LR
    )
    for case, del_value in test_cases:
        tree = AVL(case)
        print('INPUT  :', tree, 'DEL:', del_value)
        tree.print_tree()
        tree.remove(del_value)
        print('RESULT :', tree)
        tree.print_tree()
        print('')

    print("\nPDF - method remove() example 3")
    print("-------------------------------")
    case = range(-9, 16, 2)
    tree = AVL(case)
    for del_value in case:
        print('INPUT  :', tree, del_value)
        tree.remove(del_value)
        print('RESULT :', tree)

    print("\nPDF - method remove() example 4")
    print("-------------------------------")
    case = range(0, 34, 3)
    tree = AVL(case)
    for _ in case[:-2]:
        root_value = tree.get_root().value
        print('INPUT  :', tree, root_value)
        tree.remove(root_value)
        print('RESULT :', tree)

    print("\nPDF - method remove() example 5")
    print("-------------------------------")
    for _ in range(100):
        case = list(set(random.randrange(1, 20000) for _ in range(900)))
        tree = AVL(case)
        for value in case[::2]:
            tree.remove(value)
        if not tree.is_valid_avl():
            raise Exception("PROBLEM WITH REMOVE OPERATION")
    print('remove() stress test finished')

    print("\nPDF - method contains() example 1")
    print("---------------------------------")
    tree = AVL([10, 5, 15])
    print(tree.contains(15))
    print(tree.contains(-10))
    print(tree.contains(15))

    print("\nPDF - method contains() example 2")
    print("---------------------------------")
    tree = AVL()
    print(tree.contains(0))

    print("\nPDF - method inorder_traversal() example 1")
    print("---------------------------------")
    tree = AVL([10, 20, 5, 15, 17, 7, 12])
    print(tree.inorder_traversal())

    print("\nPDF - method inorder_traversal() example 2")
    print("---------------------------------")
    tree = AVL([8, 10, -4, 5, -1])
    print(tree.inorder_traversal())

    print("\nPDF - method find_min() example 1")
    print("---------------------------------")
    tree = AVL([10, 20, 5, 15, 17, 7, 12])
    print(tree)
    print("Minimum value is:", tree.find_min())

    print("\nPDF - method find_min() example 2")
    print("---------------------------------")
    tree = AVL([8, 10, -4, 5, -1])
    print(tree)
    print("Minimum value is:", tree.find_min())

    print("\nPDF - method find_max() example 1")
    print("---------------------------------")
    tree = AVL([10, 20, 5, 15, 17, 7, 12])
    print(tree)
    print("Maximum value is:", tree.find_max())

    print("\nPDF - method find_max() example 2")
    print("---------------------------------")
    tree = AVL([8, 10, -4, 5, -1])
    print(tree)
    print("Maximum value is:", tree.find_max())

    print("\nPDF - method is_empty() example 1")
    print("---------------------------------")
    tree = AVL([10, 20, 5, 15, 17, 7, 12])
    print("Tree is empty:", tree.is_empty())

    print("\nPDF - method is_empty() example 2")
    print("---------------------------------")
    tree = AVL()
    print("Tree is empty:", tree.is_empty())

    print("\nPDF - method make_empty() example 1")
    print("---------------------------------")
    tree = AVL([10, 20, 5, 15, 17, 7, 12])
    print("Tree before make_empty():", tree)
    tree.make_empty()
    print("Tree after make_empty(): ", tree)

    print("\nPDF - method make_empty() example 2")
    print("---------------------------------")
    tree = AVL()
    print("Tree before make_empty():", tree)
    tree.make_empty()
    print("Tree after make_empty(): ", tree)
