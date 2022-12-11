import bnb
from branch_and_bound import *

if __name__ == '__main__':
    with open('input.txt') as f:
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
        coefficients_of_restrictions[i].remove(right_side[i])

    model = Model(sense=MAXIMIZE, solver_name=CBC)
    variables = [model.add_var() for _ in range(quantity_of_vars_and_restrictions[0])]
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
    my_bnb = branch_and_bound(model)[0].objective_value
    egidio = bnb.branch_and_bound(model)[0].objective_value
    print(f"Meu BNB: {my_bnb}")
    print(f"BNB de Egídio: {egidio}")
    f.close()
