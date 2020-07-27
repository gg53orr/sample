"""
Visualization functions
"""
import os
import seaborn as sn
import pandas as pd
import matplotlib.pyplot as plt


def plot_similarity_matrix(names, correlations, output):
    """
    For plotting similarity matrix
    :param names: names of the documents
    :param correlations: the distances
    :param output: png
    :return:
    """
    confusion_matrix_frame = pd.DataFrame(correlations, names, names)
    sn.set(font_scale=1.4)
    sn.heatmap(confusion_matrix_frame, annot=True, annot_kws={"size": 16}).set_title("Similarity Matrix")
    plt.savefig(output)


