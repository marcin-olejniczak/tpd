import json
import numpy
from pprint import pprint

with open('config.json') as data_file:
    config = json.load(data_file)

g_matrix = config['matrix']

def add_min_max_column_and_row(matrix):
    """
    add to game matrix min and max columnd and row
    :param matrix:
    :return:
    """
    matrix = list(matrix)
    for row in matrix:
        # columns
        row = row.append(None)
    # row
    matrix.append([None for i in matrix[0]])
    return matrix

def remove_dominated_columns(matrix):
    """
    Returns matrix with dominated columns removed
    Jezeli wszystki el. w kol. sa >= odpowiednim el w innej kolumnie i
    conajmniej jeden jest wiekszy to kolumna jest zdominowana
    :param matrix:
    Wiersze moga byc dominowane podobnie jak kolumny z tym, ze tam warunkiem
    jest, ze el. zd. wiersza <= odpowiednim el w innych wierszach
    :return:
    """
    pass

def fill_min_max_columns(matrix):
    """
    Calculate
    :param matrix:
    :return:
    """
    for row in matrix[:len(matrix) - 1 ]:
        min_value = min(row[:len(row) - 1])
        # store value in the last position - max column
        row[len(row) - 1] = min_value

    transponsed = list(zip(*matrix))
    for column in list(transponsed[:len(transponsed) - 1]):
        col_i = transponsed.index(column)
        column = list(column)
        max_value = max(column[:len(column) - 1])
        column[len(column) -1] = max_value
        transponsed[col_i] = column

    return list(zip(*transponsed))

def find_saddle_points(matrix):
    """
    Find sadlle points
    :param matrix:
    :return:
    """
    min_column = [row[len(row) - 1] for row in matrix[:len(matrix) - 1]]
    max_row = matrix[len(matrix) - 1]
    saddle_points = []
    for i, x in enumerate(max_row):
        for j, y in enumerate(min_column):
            if x == y:
                # to indicate index in matrix j-row, i-column index
                saddle_points.append((j, i))

    return saddle_points

matrix_with_min_max_calculated = fill_min_max_columns(
    add_min_max_column_and_row(g_matrix)
)

print numpy.matrix(
    matrix_with_min_max_calculated
)
print find_saddle_points(matrix_with_min_max_calculated)