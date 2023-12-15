from fm_demo_process.fm_process_operators_annealing import *
from fm_demo_process.fm_process_operators_cutting import *
# from fm_demo_process.fm_process_operators_heat_treatment import *
# from fm_demo_process.fm_process_operators_hard_turning import *
from fm_demo_process.fm_process_operators_lapping import *

def add_operators_to_problem(fm_problem):
    fm_problem.add_action(a_annealing_capacity)

    fm_problem.add_action(a_cutting_capacity)

    #fm_problem.add_action(a_heat_treatment_capacity)

    #fm_problem.add_action(a_hard_turning_capacity)

    fm_problem.add_action(a_lapping_capacity)