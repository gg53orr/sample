import unittest
import sys
import os
import logging
sys.path.append(os.path.join(os.path.dirname(__file__), "..", "analyzer"))
import core_analyzer
import normalizer
from main import HouseAnalyzer
LOGGER = logging.getLogger(__name__)


class TestHouseAnalyzer(unittest.TestCase):
    """
    General house analyzer
    """
    def test_basic_analysis(self):
        """
        Basic analysis
        :return:
        """
        analyzer = HouseAnalyzer()
        analysis = analyzer.process_entry("There is one bedroom")
        numeric = analysis.get_attributes("numeric")
        self.assertTrue("bedroom" in numeric)
        self.assertTrue(1 in numeric["bedroom"])
        self.assertFalse("bathroom" in numeric)

        analysis2 = analyzer.process_entry("The house has 4 bedrooms and 2 bathrooms")
        numeric2 = analysis2.get_attributes("numeric")
        self.assertTrue("bedroom" in numeric2)
        self.assertTrue(4 in numeric2["bedroom"])
        self.assertTrue("bathroom" in numeric2)


if __name__ == '__main__':
    logging.basicConfig(level=logging.DEBUG, format='%(name)s %(levelname)s %(message)s')
    unittest.main()
