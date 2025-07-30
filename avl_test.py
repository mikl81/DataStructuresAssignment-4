import unittest
from avl import *

class MyTestCase(unittest.TestCase):
    def test_balance_factor(self):
        tree = AVL()
        self.assertEqual(tree._balance_factor(tree._root), 0)
        tree.add(1)
        self.assertEqual(tree._balance_factor(tree._root), 0)
        tree.add(2)
        self.assertEqual(tree._balance_factor(tree._root), 1)
        tree.add(-1)
        self.assertEqual(tree._balance_factor(tree._root), 0)

        print(tree)

    def test_add(self):
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

    def test_add_2(self):
        print("\nPDF - method add() example 2")
        print("----------------------------")
        test_cases = (
            (10, 20, 30, 40, 50),  # RR, RR
            (10, 20, 30, 50, 40),  # RR, RL
            (30, 20, 10, 5, 1),  # LL, LL
            (30, 20, 10, 1, 5),  # LL, LR
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

    def test_add_3(self):
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

    def test_remove(self):
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


if __name__ == '__main__':
    unittest.main()
