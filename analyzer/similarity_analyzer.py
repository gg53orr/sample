"""
Module for comparing documents
"""
import spacy


class DocumentComparator:
    """
    Basic comparison tool using
    the big general English model for Spacy
    """
    def __init__(self):
        """
        Loading model
        """
        self.big_model = spacy.load("en_core_web_lg")
        self.docs = dict()
        self.analyses = dict()

    def add_document(self, name, data, analysis):
        """
        Adding a document
        :param name:
        :param data:
        :param analysis:
        :return:
        """
        self.docs[name] = self.big_model(data)
        self.analyses[name] = self.big_model(analysis.to_json())

    def get_document_data(self, name, mode):
        """
        We deliver either the actual document
        or just the succinct analysis thereof
        :param name:
        :param mode:
        :return:
        """
        if mode == "standard":

            return self.docs[name]
        return self.analyses[name]

    def compare(self, mode: str = "standard"):
        """
        Comparing the whole lot and producing
        distances
        :return:
        """
        names = self.docs.keys()
        distances = []
        for name in names:
            the_doc = self.get_document_data(name, mode)
            row = []
            for other_name in names:
                the_other = self.get_document_data(other_name, mode)
                distance = the_doc.similarity(the_other)
                row.append(distance)
            distances.append(row)

        return names, distances
