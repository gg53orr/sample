"""
Functionality for normalizing some tokens, processing numbers
"""

NUMBER_ERROR = -100000000


class NumberConverter:
    """
    Currently just a basic number converter
    Convert the first 10 numbers, handle some
    exceptions and the rest properly
    """

    def __init__(self):

        self.basic_numbers = {'one': 1, 'two': 2, 'three': 3, \
                              'four': 4, 'five': 5, 'six': 6, \
                              'seven': 7, 'eight': 8, 'nine': 9, 'ten': 10}

    def to_number(self, text: str):
        """
        If number, we try to get the numeric value
        :param text:
        :return:
        """
        text = text.lower()
        if text in self.basic_numbers:
            return self.basic_numbers[text]
        try:
            return float(text)
        except:
            return NUMBER_ERROR


class TokenNormalizer:
    """
    Token normalizer, currently for numbers
    """

    def __init__(self):
        self.number_converter = NumberConverter()

    def normalize_token(self, token):
        """
        Currently only trying to convert number
        :param token:
        :return:
        """
        if token.pos_ == "NUM":
            return self.number_converter.to_number(token.text)

        return token.text
