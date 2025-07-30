import math
import unittest
from src.mcp_calpower_server.calpower import find_powers

class TestCalpower(unittest.TestCase):
    def test_power(self):
        self.assertEqual(find_powers("2 ** 3"), "8")
        self.assertEqual(find_powers("2 ^ 3"), "8")

if __name__ == '__main__':
    unittest.main()