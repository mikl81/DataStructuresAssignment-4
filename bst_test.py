import unittest
from bst import *

class MyTestCase(unittest.TestCase):
    def test_add(self):
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


if __name__ == '__main__':
    unittest.main()
