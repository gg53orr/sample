"""
General utility functions to access files and the like
"""
import os
from operator import itemgetter


def get_files(the_path: str):
    """
    Gets all the files in a directory
    :param the_path:
    :return:
    """
    files_only = []
    for path in os.listdir(the_path):
        full_path = os.path.join(the_path, path)
        if os.path.isfile(full_path):
            files_only.append(full_path)
    return files_only


def print_tokens(the_counter, output):
    """

    :param the_counter:
    :param output:
    :return:
    """
    all_items = sorted(the_counter.items(), key=itemgetter(0))
    with open(output + "/token_view.txt", encoding="utf-8", mode="w") as handle:
        for item in all_items:
            handle.write(str(item) + "\n")
