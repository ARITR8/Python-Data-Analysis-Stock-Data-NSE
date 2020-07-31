from unittest_example import add_2_numbers
import unittest
import pytest


class test_add_2_numbers(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        print('Entering Test Class')

    @classmethod
    def tearDownClass(cls):
        print('Exiting Test Class')
    def test_2_possitive_number(self):
        self.assertEqual(add_2_numbers.add_numbers(2 , 4), 11 )
        print(self.id)



class power_test(unittest.TestCase):
    def power_test_sequence(self):
        self.assertEqual(add_2_numbers.power2number( 2, 3), 12)

if __name__ == '__main__':
    unittest.main()


