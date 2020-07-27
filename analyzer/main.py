"""
Main tool to try the analyzer
We read from a directory with input data
"""
import os
import sys
import json
from operator import itemgetter

from core_analyzer import HouseAnalyzer
from similarity_analyzer import DocumentComparator
from visualizer import plot_similarity_matrix
sys.path.append(os.path.join(os.path.dirname(__file__)))


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
    for item in all_items:
        print(item)


if __name__ == '__main__':

    ANALYZER = HouseAnalyzer()

    ANALYZER.activate_general_analysis()
    SOURCE = os.path.join(".", "input_data")
    TARGET = os.path.join(".", "output_data")
    RECORDS = get_files(SOURCE)

    COMPARATOR = DocumentComparator()

    for index, record in enumerate(RECORDS):

        with open(record, encoding="utf-8", mode="r") as input_handle:
            print(record)
            file_data = input_handle.read()
            analysis = ANALYZER.process_entry(file_data)
            base_name = os.path.basename(record)
            COMPARATOR.add_document(base_name, file_data, analysis)
            with open(TARGET + "/" + base_name, "w") as file_analysis:
                file_analysis.write(analysis.to_json())
    # We do a comparison with out of the box Spacy
    names_1, distances1 = COMPARATOR.compare()
    plot_similarity_matrix(names_1, distances1, os.path.join(TARGET, "distance_matrix.png"))

    # A very trivial print out that should not go on production
    # Just to have an initial look at the tokens and frequency
    if ANALYZER.do_general_analysis:
        print_tokens(ANALYZER.all_tokens, TARGET)
