import unittest
import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), "..", "analyzer"))
import core_analyzer
import normalizer
from main import HouseAnalyzer


class TestHouseAnalyzer(unittest.TestCase):

    def test_start(self):
        analyzer = HouseAnalyzer()
        analyzer.process_entry("There is a room")

if __name__ == '__main__':
    unittest.main()
