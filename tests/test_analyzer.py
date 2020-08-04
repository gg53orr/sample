import unittest
import sys
import os
import logging
import spacy
sys.path.append(os.path.join(os.path.dirname(__file__), "..", "analyzer"))
from main import HouseAnalyzer
LOGGER = logging.getLogger(__name__)
NLP = spacy.load("en_core_web_sm")


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
        json = analysis2.to_json()
        self.assertTrue("bedroom" in numeric2)
        self.assertTrue(4 in numeric2["bedroom"])
        self.assertTrue("bathroom" in numeric2)

    def do_relation(self, text, analyzer):
        """
        :param text:
        :param analyzer:
        :return:
        """
        doc = NLP(text)
        for token in doc:
            if token.pos_ == "NUM":
                link = analyzer.is_numeric_of_determiner(token, doc)
                if link:
                    return True

        return False

    def test_negation(self):
        """"
        """
        analyzer = HouseAnalyzer()
        inputs = ["There is a W/C", "The house has no W/C here", "There are 3 bathrooms"]
        expected_bathrooms = [[1], [0], [3.0]]
        # There is a bug on negations at certain positions!!
        hits = 0
        for index, an_input in enumerate(inputs):
            analysis = analyzer.process_entry(an_input)
            numeric_dictionary = analysis.get_attributes("numeric")
            json = analysis.to_json()
            possibilities = list(numeric_dictionary["bathroom"])
            if possibilities == expected_bathrooms[index]:
                hits += 1

        self.assertTrue(hits == 3)

    def test_numeric_relations(self):
        """
        numeric relations
        :return:
        """
        analyzer = HouseAnalyzer()
        inputs = ["The garden is 44 feet long", "There are 3 bathrooms"]
        expected = [True, False]
        errors = 0
        for index, an_input in enumerate(inputs):
            if self.do_relation(an_input, analyzer) == expected[index]:
                LOGGER.info("OK")
            else:
                LOGGER.info("ERROR")
                errors += 1
        self.assertTrue(errors == 0)


if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO, format='%(name)s %(levelname)s %(message)s')
    unittest.main()
