from unified_planning.shortcuts import *

############################################
# Defining types
#############################################
type_family = UserType("type_family")
type_machine = UserType("type_machine")
type_piece = UserType("type_piece")
type_step = UserType("type_step")

############################################
# Defining objects
#############################################
# pieces
piece_gear = Object("gear", type_piece)
piece_pinion = Object("pinion", type_piece)

# families
family_F1 = Object("F1", type_family)
family_F2 = Object("F2", type_family)
family_F3 = Object("F3", type_family)

# process steps
step_annealing = Object("annealing", type_step)
step_cutting = Object("cutting", type_step)
#step_hard_turning = Object("hard_turning", type_step)
step_lapping = Object("lapping", type_step)

# machines
# annealing
machine_A1 = Object("A1", type_machine)
machine_A2 = Object("A2", type_machine)

# cutting
machine_C1 = Object("C1", type_machine)
machine_C2 = Object("C2", type_machine)
machine_C3 = Object("C3", type_machine)
#
# # hard turning
# machine_T1 = Object("T1", type_machine)
# machine_T2 = Object("T2", type_machine)
# machine_T3 = Object("T3", type_machine)

# lapping
machine_L1 = Object("L1", type_machine)
machine_L2 = Object("L2", type_machine)

def add_base_objects_to_problem(fm_problem):
    fm_problem.add_object(piece_gear)
    fm_problem.add_object(piece_pinion)

    fm_problem.add_object(family_F1)
    fm_problem.add_object(family_F2)
    fm_problem.add_object(family_F3)

    fm_problem.add_object(machine_A1)
    fm_problem.add_object(machine_A2)
    fm_problem.add_object(machine_C1)
    fm_problem.add_object(machine_C2)
    fm_problem.add_object(machine_C3)
    fm_problem.add_object(machine_L1)
    fm_problem.add_object(machine_L2)

    fm_problem.add_object(step_annealing)
    fm_problem.add_object(step_cutting)
    #fm_problem.add_object(step_hard_turning)
    fm_problem.add_object(step_lapping)

def get_all_objects_from_problem(fm_problem):
    ###########################################
    # Getting all the objects for initialization
    #############################################
    all_pieces = list(fm_problem.objects(type_piece))
    all_families = list(fm_problem.objects(type_family))
    all_machines = list(fm_problem.objects(type_machine))
    all_steps = list(fm_problem.objects(type_step))
    return all_pieces, all_families, all_machines, all_steps