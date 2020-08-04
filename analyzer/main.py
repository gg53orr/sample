"""
Main tool to try the analyzer
We read from a directory with input data
"""
import os
import sys

sys.path.append(os.path.join(os.path.basename(__file__)))
sys.path.append(os.path.join(os.path.dirname(__file__)))

from household_analyzer import HouseAnalyzer
from io_utils import get_files, print_tokens
from similarity_analyzer import DocumentComparator
from visualizer import plot_similarity_matrix


def process_input(records, target):
    """
    This is the entry point, processes the records and prints
    results in target
    :param records:
    :param target:
    :return:
    """
    analyzer = HouseAnalyzer()

    analyzer.activate_general_analysis()

    comparator = DocumentComparator()

    for record in records:

        with open(record, encoding="utf-8", mode="r") as input_handle:
            print(record)
            file_data = input_handle.read()
            analysis = analyzer.process_entry(file_data)
            base_name = os.path.basename(record)
            comparator.add_document(base_name, file_data, analysis)
            with open(TARGET + "/" + base_name, "w") as file_analysis:
                file_analysis.write(analysis.to_json())
    # We do a comparison with out of the box Spacy
    names_1, distances1 = comparator.compare()
    plot_similarity_matrix(names_1, distances1, os.path.join(TARGET, "distance_matrix.png"))

    # A very trivial print out that should not go on production
    # Just to have an initial look at the tokens and frequency
    if analyzer.do_general_analysis:
        print_tokens(analyzer.all_tokens, target)


if __name__ == '__main__':

    SOURCE = os.path.join(".", "input_data")
    TARGET = os.path.join(".", "output_data")
    RECORDS = get_files(SOURCE)
    process_input(RECORDS, TARGET)
