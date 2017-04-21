from pulp import *

def print_mixed_strategy(payoff_matrix, optimalization=LpMinimize):
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

    v = 1 / sum(var_values)
    print 'V: {}'.format(v)
    # actually it's what we need to determine - how often play given strategy
    frequencies = []
    for var in variables:
        print '{}: {}'.format(var.name, value(var) * v)
# test
payoff_matrix = [
    [5, 0, 1],
    [2, 4, 3],
]
print 'Row Player Strategy'
print_mixed_strategy(payoff_matrix, LpMinimize)
print 'Column Player Strategy'
print_mixed_strategy([list(i) for i in zip(*payoff_matrix)], LpMaximize)


# test for our variant
payoff_matrix = [
    [1.2, 0.4, ],
    [0.2, 1, ],
    [0.8, 0.8, ],
]
print 'Row Player Strategy'
print_mixed_strategy(payoff_matrix, LpMinimize)
print 'Column Player Strategy'
print_mixed_strategy([list(i) for i in zip(*payoff_matrix)], LpMaximize)
