from pulp import *
from game import find_saddle_points


def print_mixed_strategy(
        payoff_matrix, optimalization=LpMinimize, added_value=0
):
    """
    Minimize for player A - row,
    Maximaze for player B - columns
    :param payoff_matrix:
    :param optimalization:
    :return:
    """
    # calc for rows
    variables = []
    # declare your variables
    for i, row in enumerate(payoff_matrix):
        variables.append(LpVariable("x{}".format(i), 0, 1))

    # defines the problem
    prob = LpProblem("problem", optimalization)

    # defines the constraints
    # transponse matrix to write conditions easier
    transponsed_matrix = [list(i) for i in zip(*payoff_matrix)]
    for row in transponsed_matrix:
        row_prob = 0
        for i, factor in enumerate(row):
            row_prob += factor * variables[i]
        if optimalization is LpMinimize:
            prob += row_prob >= 1
        else:
            prob += row_prob <= 1

    # defines the objective function to min/max-ize
    prob += sum(variables)

    # solve the problem
    status = prob.solve(GLPK(msg=0))
    LpStatus[status]

    var_values = []
    for variable in variables:
        var_value = value(variable)
        print "{}': {}".format(
            variable.name, value(variable)
        )
        var_values.append(var_value)

    v = (1 / sum(var_values)) - added_value
    print 'V: {:.2f}'.format(v)
    # actually it's what we need to determine - how often play given strategy
    frequencies = []
    for var in variables:
        print '{}: {:.2f}'.format(var.name, value(var) * v)


def make_matrix_positive(matrix):
    """
    Modify  matrix in place and return value which was added
    :param matrix:
    :return:
    """
    rows_min = []
    added_value = 0
    for row in matrix:
        rows_min.append(min(row))

    min_value = min(rows_min)
    if min_value < 0:
        added_value = abs(min_value)

    # add value to each cell
    for row in matrix:
        for i, cell in enumerate(row):
            row[i] += added_value

    return added_value


def solve_game(payoff_matrix):
    """
    Solve game by following steps:
        - find saddle points
        - remove dominated columns
        - find mixed strategies
    :param payoff_matrix:
    :return:
    """

    added_value = make_matrix_positive(payoff_matrix)

    saddle_points = find_saddle_points(payoff_matrix)
    if saddle_points:
        print 'Saddle Points {}'.format(saddle_points)
        return

    print 'Row Player Strategy'
    print_mixed_strategy(payoff_matrix, LpMinimize, added_value)
    print 'Column Player Strategy'
    print_mixed_strategy(
        [list(i) for i in zip(*payoff_matrix)],
        LpMaximize,
        added_value,
    )


# test
test_payoff_matrix = [
    [5, 0, 1],
    [2, 4, 3],
]
solve_game(test_payoff_matrix)

# test for our variant
payoff_matrix = [
    [1.2, 0.4, ],
    [0.2, 1, ],
    [0.8, 0.8, ],
]
#solve_game(payoff_matrix)
