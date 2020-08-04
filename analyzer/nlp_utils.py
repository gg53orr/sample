"""
General utility functions to go through Spacy
"""
# Just some negations, should be generalized
ENGLISH_NEGATIONS = ["no", "not"]


def is_child(a_token, possible_ancestor):
    """
    Check if this token is immediate child of a possible ancestor
    :param a_token:
    :param possible_ancestor:
    :return: True if the possible ancestor is head of a_token
    """
    head = a_token.head
    head_text = head.text.lower()

    if head_text == possible_ancestor.lower() or head_text.endswith(possible_ancestor):
        return True
    if head.lemma_.lower() == possible_ancestor.lower():
        return True

    return False


def has_negation(phrase):
    """
    Very basic negation finder for phrases
    :param phrase:
    :return:
    """
    for token in phrase:

        if token.text.lower() in ENGLISH_NEGATIONS:
            return True

    return False


def is_relevant_attribute(token):
    """

    :param token: Spacy token
    :return: True if this is a relevant token
    giving some attribute to the noun
    """
    if not token.text.isalnum():
        # Sometimes the tagger can get non
        # alphanumeric wrong
        return False

    if token.pos_ == "ADJ" or token.pos_ == "NUM":
        return True
    return False
