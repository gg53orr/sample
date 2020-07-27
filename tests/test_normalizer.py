import unittest
import os
import sys
import logging
import spacy
sys.path.append(os.path.join(os.path.dirname(__file__), "..", "analyzer"))
from normalizer import TokenNormalizer, NumberConverter, NUMBER_ERROR
LOGGER = logging.getLogger(__name__)


class TestHouseAnalyzer(unittest.TestCase):
    """
    Testing the core
    """
    def test_token_normalizer(self):
        normalizer = TokenNormalizer()
        nlp = spacy.load("en_core_web_sm")
        doc = nlp("We have two rooms")
        expected = ["We", "have", 2, "rooms"]
        for index, token in enumerate(doc):
            normalized_form = normalizer.normalize_token(token)
            LOGGER.debug(str(normalized_form) + " " + str(type(normalized_form)))
            self.assertTrue(normalized_form == expected[index])

    def test_number_converter(self):
        converter = NumberConverter()
        # We are currently not interested in converting
        # forty. Some library like https://pypi.org/project/word2number/
        # would do the trick for English, though
        examples = ["3et", "1.2", "1222", "three", "forty"]
        results = [NUMBER_ERROR, 1.2, 1222, 3, NUMBER_ERROR]
        for index, example in enumerate(examples):
            output = converter.to_number(example)
            LOGGER.debug(output)
            self.assertTrue(output == results[index])

if __name__ == '__main__':

    logging.basicConfig(level=logging.DEBUG, format='%(name)s %(levelname)s %(message)s')
    unittest.main()
