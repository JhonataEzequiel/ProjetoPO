import branch_and_bound
from mip import *


if __name__ == '__main__':

    with open('input-1.txt') as f:
        lines = f.readlines()

    quantity_of_vars_and_restrictions = [int(lines[0].split(' ')[0]), int(lines[0].split(' ')[1].strip())]
    coefficients_in_the_objective_func = [float(coefficient.strip()) for coefficient in lines[1].split(' ')]
    coefficients_of_restrictions = [
        [
            float(coefficient.strip()) for coefficient in line.split(' ')
        ]
        for line in lines[2:]
    ]
    right_side = [coefficients[-1] for coefficients in coefficients_of_restrictions]
    for i in range(len(coefficients_of_restrictions)):
        coefficients_of_restrictions[i] = coefficients_of_restrictions[i][:-1]

    model = Model(sense=MAXIMIZE, solver_name=CBC)
    variables = [model.add_var(var_type=CONTINUOUS, lb=0, ub=1) for _ in range(quantity_of_vars_and_restrictions[0])]
    model.objective = xsum(
            coefficients_in_the_objective_func[i] * variables[i]
            for i in range(len(coefficients_in_the_objective_func))
        )

    j = 0
    for coefficients_of_restriction in coefficients_of_restrictions:
        model += xsum(coefficients_of_restriction[i] * variables[i] for i in range(len(coefficients_of_restriction))) \
                 <= right_side[j]
        j += 1

    model.write('model.lp')
    with open('model.lp') as modelo:
        print(modelo.read())
    branch_and_bound.branch_and_bound(model)
    print(branch_and_bound.primal_limit)
    f.close()
