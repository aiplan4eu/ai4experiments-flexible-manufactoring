from unified_planning.model import Problem
from fm_demo_process.fm_process_base import *
from fm_demo_process.fm_process_fluents import *
from fm_demo_process.fm_process_operators import *

def create_fm_problem():
    ############################################
    # Initializing the base problem
    #############################################
    fm_problem = Problem("flexible_manufacturing_problem")

    add_base_objects_to_problem(fm_problem)
    add_fluents_to_problem(fm_problem)
    add_operators_to_problem(fm_problem)

    return fm_problem

def init_domain_from_initial_values(fm_problem):
    for fam in list(fm_problem.objects(type_family)):
        # get the expected final output for each family
        final_output = fm_problem.initial_value(expected_final_output(fam)).int_constant_value()
        # we backpropagate to lapped
        fm_problem.set_initial_value(to_be_lapped(fam),
                                     final_output - fm_problem.initial_value(stock_lapped(fam)).int_constant_value())
        # gear and pinion pipelines
        for piece in fm_problem.objects(type_piece):
            # hard-turning
            to_be_hard_turned_value = max(
                0,
                fm_problem.initial_value(to_be_lapped(fam)).int_constant_value()
                - fm_problem.initial_value(stock_after(step_hard_turning, fam, piece)).int_constant_value()
            )
            fm_problem.set_initial_value(to_be_processed(step_hard_turning, fam, piece), to_be_hard_turned_value)

            # heat treatment
            to_be_heat_treated_value = max(
                0,
                fm_problem.initial_value(to_be_processed(step_hard_turning, fam, piece)).int_constant_value()
                - fm_problem.initial_value(stock_after(step_heat_treatment, fam, piece)).int_constant_value()
            )
            fm_problem.set_initial_value(to_be_processed(step_heat_treatment, fam, piece), to_be_heat_treated_value)

            # cutting
            to_be_cut_value = max(
                0,
                fm_problem.initial_value(to_be_processed(step_heat_treatment, fam, piece)).int_constant_value()
                - fm_problem.initial_value(stock_after(step_cutting, fam, piece)).int_constant_value()
            )
            fm_problem.set_initial_value(to_be_processed(step_cutting, fam, piece), to_be_cut_value)

            # annealing
            to_be_annealed_value = max(
                0,
                fm_problem.initial_value(to_be_processed(step_cutting, fam, piece)).int_constant_value()
                - fm_problem.initial_value(stock_after(step_annealing, fam, piece)).int_constant_value()
            )
            fm_problem.set_initial_value(to_be_processed(step_annealing, fam, piece), to_be_annealed_value)




