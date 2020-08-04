"""
Core modules for analysis of properties
"""
import os
import json
from collections import Counter
from ranges import RangeSet, Range
import spacy

from normalizer import TokenNormalizer
from nlp_utils import is_relevant_attribute, has_negation, is_child


def set_default(obj):
    """
    Just a small function to make the sets serial
    :param obj:
    :return:
    """
    if isinstance(obj, set):
        return list(obj)
    raise TypeError


class Analysis:
    """
    Container for all results of ever record
    """
    def __init__(self):
        """
        Constructor with 3 main dicts:
        one for adjectives, one with numeric values
        and one with numeric values connected to something else, relations
        """
        self.noun_adjectives = dict()
        self.noun_numeric = dict()
        self.noun_relations = dict()

    def get_dict(self, pos_: str):
        """
        Gets the right dictionary, whether for
        numerical or other adjectives
        :param pos_:
        :return: dict
        """
        if pos_ == "NUM":
            return self.noun_numeric

        return self.noun_adjectives

    def add_relation(self, item1, item2, determiner):
        """
        Adds a relation between a noun, another noun and a number
        :param item1:
        :param item2:
        :param determiner:
        :return:
        """
        if item1 in self.noun_relations:
            relations = self.noun_relations[item1]
            relations.add([item2, determiner])
        else:
            relations = [[item2, determiner]]
            self.noun_relations[item1] = relations

    def add_default_attribute(self, item, value):
        """
        When there is only the mention of an item
        We assume for Western European language
        presence of article
        :param item:
        :param determiner:
        :param value: 0 or 1 usually, consider other
        :return:
        """
        dictionary = self.get_dict("NUM")
        if item in dictionary:
            attributes = dictionary[item]
            # This needs to be generalized
            attributes.add(value)
        else:
            dictionary[item] = set([value])

    def add_attribute(self, item, original_token, determiner):
        """

        :param item:
        :param original_token:
        :param determiner:
        :return:
        """
        dictionary = self.get_dict(original_token.pos_)
        if item in dictionary:
            attributes = dictionary[item]
            attributes.add(determiner)
        else:
            dictionary[item] = set([determiner])

    def get_attributes(self, the_type: str):
        """
        Gets the right dictionary
        :param the_type:
        :return:
        """
        if the_type == "numeric":
            return self.noun_numeric

        return self.noun_adjectives

    def get_relations(self):
        """
        Gets the noun relations
        :return:
        """
        return self.noun_relations

    def to_json(self):
        """
        Prints a json form, transforming a set into an array
        :return:
        """
        return json.dumps(self.__dict__, indent=4, sort_keys=True, default=set_default)


class HouseAnalyzer:
    """
    The main analyzer
    """
    def __init__(self, language: str = "en"):

        self.__load_resources(language)
        self.measure_words = ["ft", "feet"]
        self.normalizer = TokenNormalizer()
        self.do_general_analysis = False
        self.all_tokens = Counter()

    def __load_resources(self, language: str):

        self.nlp = spacy.load(language + "_core_web_sm")

        resource = os.path.join(".", "ling_data", "housing_" + language + ".json")
        # Loading two dictionaries to access the linguistic semantic data
        self.housing_dict = dict()
        self.triggers_to_keys = dict()
        with open(resource, encoding="utf-8") as json_file:
            self.housing_dict = json.load(json_file)
        keys = self.housing_dict.keys()
        for key in keys:
            items = self.housing_dict[key]
            for item in items:
                self.triggers_to_keys[item] = key
        self.all_triggers = list(self.triggers_to_keys.keys())
        self.all_triggers.sort(key=len, reverse=True)  # sorts by descending length

    def count_tokens(self, sent):
        """
        Just a counter to get a glimpse on the tokens and frequency
        :param sent: sentence
        :return:
        """
        for token in sent:
            if token.text.isalnum:
                self.all_tokens[token.text.lower()] += 1

    def activate_general_analysis(self):
        """
        This activates the counter of words for
        initial analysis of data
        :return:
        """
        self.do_general_analysis = True

    def process_entry(self, entry: str):
        """
        Process a whole entry
        :param entry:
        :return:
        """

        doc = self.nlp(entry)
        analysis = Analysis()

        for sent in doc.sents:

            if self.do_general_analysis:
                self.count_tokens(sent)
            for noun_phrase in sent.noun_chunks:
                covered = RangeSet()

                for trigger in self.all_triggers:

                    if trigger in noun_phrase.text.lower():

                        start = noun_phrase.text.lower().index(trigger)

                        if not Range(start, len(noun_phrase.text) + start).intersection(covered):

                            covered.add(Range(noun_phrase.start, noun_phrase.end))
                            self.__process_np(trigger, noun_phrase, doc, analysis)

        return analysis

    def __process_np(self, trigger, noun_phrase, doc, analysis):
        """

        :param trigger:
        :param noun_phrase:
        :param doc:
        :param analysis:
        :return:
        """
        attribute_found = False
        noun = self.triggers_to_keys[trigger]

        for token in noun_phrase:

            if is_relevant_attribute(token):

                attribute_found = True

                if self.is_numeric_of_determiner(token, doc):

                    determiner = self.normalizer.normalize_token(token)
                    analysis.add_relation(noun, determiner, doc[token.i + 1].text)
                else:
                    determiner = self.normalizer.normalize_token(token)
                    if is_child(token, trigger):
                        analysis.add_attribute(noun, token, determiner)
        if not attribute_found:
            # Eventually we can check here the presence of
            # an article for EN/NO/DE/NL/ES etc, not for Slavic languages
            # We assume there is at least one
            if has_negation(noun_phrase):
                analysis.add_default_attribute(noun, 0)
            else:
                analysis.add_default_attribute(noun, 1)

    def is_numeric_of_determiner(self, token, doc):
        """
        True if the item is actually number linked
        to another token. Consider generalizing
        for language where there is no continuity
        between relevant tokens
        (Chinese, Japanese)
        :param token:
        :param doc:
        :return:
        """
        total = doc.__len__()
        if token.i + 1 < total:
            next_token = doc[token.i + 1]
            if next_token.text.lower() in self.measure_words:
                return True
        return False
