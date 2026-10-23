import unittest
from command_engine import safe_calculate

class CalculatorTests(unittest.TestCase):
    def test_basic_math(self):
        self.assertEqual(safe_calculate("2 + 3 * 4"), 14)

    def test_power(self):
        self.assertEqual(safe_calculate("2 ** 3"), 8)

    def test_rejects_python_code(self):
        with self.assertRaises(ValueError):
            safe_calculate("__import__('os').system('echo unsafe')")

if __name__ == "__main__":
    unittest.main()
