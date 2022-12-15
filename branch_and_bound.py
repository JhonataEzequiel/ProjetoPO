from mip import *
import math

primal_limit = -math.inf


def branch_and_bound(my_model: Model):
    global primal_limit
    status = my_model.optimize()

    if status == OptimizationStatus.INFEASIBLE:
        return my_model, False
    if status == OptimizationStatus.NO_SOLUTION_FOUND:
        return my_model, False
    if primal_limit > my_model.objective_value:
        return my_model, False

    left_branch = my_model.copy()
    right_branch = my_model.copy()

    none_non_binary_vars = True
    min_distance_to_zero_dot_five = math.inf
    variable_closest_to_zero_dot_five = 0
    first_iteration = True

    for var in my_model.vars:

        if var.x not in [0, 1]:
            none_non_binary_vars = False

            if first_iteration:
                first_iteration = False
                variable_closest_to_zero_dot_five = var

            distance_to_zero_dot_five_now = var.x - 0.5 if var.x - 0.5 >= 0 else 0.5 - var.x

            if distance_to_zero_dot_five_now < min_distance_to_zero_dot_five:
                min_distance_to_zero_dot_five = distance_to_zero_dot_five_now
                variable_closest_to_zero_dot_five = var

    if none_non_binary_vars:
        return my_model, True

    print(f"\nVariable chosen to receive the constraints: {variable_closest_to_zero_dot_five.name}")
    print(f"Value of the variable: {variable_closest_to_zero_dot_five.x}\n")

    left_branch += variable_closest_to_zero_dot_five == 0
    right_branch += variable_closest_to_zero_dot_five == 1
    generated_model_and_status_for_left_side = branch_and_bound(left_branch)

    if generated_model_and_status_for_left_side is not None and generated_model_and_status_for_left_side[1]:
        if generated_model_and_status_for_left_side[0].objective_value > primal_limit:
            primal_limit = generated_model_and_status_for_left_side[0].objective_value

    generated_model_and_status_for_right_side = branch_and_bound(right_branch)

    if generated_model_and_status_for_right_side is not None and generated_model_and_status_for_right_side[1]:
        if generated_model_and_status_for_right_side[0].objective_value > primal_limit:
            primal_limit = generated_model_and_status_for_right_side[0].objective_value

    return
