## This file contains the initialization of fluents that are static in the flexible manufacturing process,
## i.e. that do not change for each EDI

from fm_demo_process.fm_process_base import *

############################################
# Inputs / Outputs of the whole process
#############################################
# fluent describing the number of elements already in the starting buffer
buff_start = up.model.Fluent("buffer_start",
                               IntType(),
                               family = type_family,
                               piece = type_piece)

# fluent that stored the expected amount of final output (to be taken from EDI later)
expected_final_output = up.model.Fluent("final_output",
                                        IntType(),
                                        family = type_family)


############################################
# Outputs of each step
#############################################
# Stock after a step
stock_after = Fluent("stock_after",
                     IntType(),
                     step = type_step,
                     family = type_family,
                     piece = type_piece)

# we need a specific one for lapped set
stock_lapped = Fluent("stock_lapped",
                      IntType(),
                      family = type_family,
                      )

############################################
# Characteristic of the EDI
#############################################
# these fluents are necessary to backpropagate the amount to be processed based on the stock
# annealing
to_be_processed = Fluent("to_be_processed",
                         IntType(),
                         step = type_step,
                         family = type_family,
                         piece = type_piece)

# lapping
to_be_lapped = Fluent("to_be_lapped",
                      IntType(),
                      family = type_family)

############################################
# Characteristics of the machines
#############################################
## Capacity of a machine for a given family, piece, and step
has_capacity = Fluent("has_capacity",
                      IntType(),
                      machine = type_machine,
                      family = type_family,
                      piece = type_piece,
                      step = type_step)


# and we set it up for each machine for which it is not 0

## If the machine is in use
is_machine_used = Fluent("is_machine_used",
                           BoolType(),
                           machine=type_machine)

## Number of items in the machine
nb_elements_in_machine = up.model.Fluent("nb_elements_in_machine",
                                           IntType(),
                                           machine=type_machine)

## Duration of each step per machine and per family
duration = Fluent("duration",
                  RealType(),
                  step = type_step,
                  machine = type_machine,
                  family = type_family,
                  piece = type_piece)

############################################
# Function to instanciate a meritor problem based on these fluents
#############################################
def add_fluents_to_problem(fm_problem):
    all_pieces, all_families, all_machines, all_steps = get_all_objects_from_problem(fm_problem)
    fm_problem.add_fluent(buff_start)
    for f in all_families:
        for p in all_pieces:
            fm_problem.set_initial_value(buff_start(f,p), 0)

    fm_problem.add_fluent(expected_final_output)
    for f in all_families:
        fm_problem.set_initial_value(expected_final_output(f), 0)

    fm_problem.add_fluent(to_be_processed)
    for s in all_steps:
        for f in all_families:
            for p in all_pieces:
                fm_problem.set_initial_value(to_be_processed(s, f, p), 0)

    fm_problem.add_fluent(to_be_lapped)
    for f in all_families:
        fm_problem.set_initial_value(to_be_lapped(f),0)

    fm_problem.add_fluent(stock_after)
    for s in all_steps:
        for f in all_families:
            for p in all_pieces:
                fm_problem.set_initial_value(stock_after(s, f, p), 0)

    fm_problem.add_fluent(stock_lapped)
    for f in all_families:
        fm_problem.set_initial_value(stock_lapped(f), 0)


    fm_problem.add_fluent(has_capacity)
    # we initialize all machines capacity to 0
    for m in all_machines:
        for f in all_families:
            for p in all_pieces:
                for s in all_steps:
                    fm_problem.set_initial_value(has_capacity(m, f, p, s), 0)

    # the annealing machines works for all families
    for f in all_families:
        fm_problem.set_initial_value(
            has_capacity(
                machine_A1, f, piece_gear, step_annealing
            ), 10)
        fm_problem.set_initial_value(
            has_capacity(
                machine_A1, f, piece_pinion, step_annealing
            ), 20)
        fm_problem.set_initial_value(
            has_capacity(
                machine_A2, f, piece_gear, step_annealing
            ), 20
        )
        fm_problem.set_initial_value(
            has_capacity(
                machine_A2, f, piece_pinion, step_annealing
            ), 50)



    # cutting (gear)
    fm_problem.set_initial_value(
        has_capacity(machine_C3, family_F1, piece_gear, step_cutting), 50)
    fm_problem.set_initial_value(
        has_capacity(machine_C3, family_F2, piece_gear, step_cutting), 20)
    fm_problem.set_initial_value(
        has_capacity(machine_C3, family_F3, piece_gear, step_cutting), 50)

    # cutting (pinion)
    fm_problem.set_initial_value(
        has_capacity(machine_C1, family_F1, piece_pinion, step_cutting), 50)
    fm_problem.set_initial_value(
        has_capacity(machine_C1, family_F3, piece_pinion, step_cutting), 50)


    fm_problem.set_initial_value(
        has_capacity(machine_C2, family_F1, piece_pinion, step_cutting), 25)
    fm_problem.set_initial_value(
        has_capacity(machine_C2, family_F2, piece_pinion, step_cutting), 25)
    fm_problem.set_initial_value(
        has_capacity(machine_C2, family_F3, piece_pinion, step_cutting), 25)


    # heat treatment
    # for f in all_families:
    #     fm_problem.set_initial_value(
    #         has_capacity(machine_H1, f, piece_pinion, step_heat_treatment), 15)
    #     fm_problem.set_initial_value(
    #         has_capacity(machine_H2, f, piece_gear, step_heat_treatment), 10)
    #     fm_problem.set_initial_value(
    #         has_capacity(machine_H2, f, piece_pinion, step_heat_treatment), 15)
    #
    # # hard turning
    # fm_problem.set_initial_value(
    #     has_capacity(machine_T1, family_F1, piece_gear, step_hard_turning), 50)
    # fm_problem.set_initial_value(
    #     has_capacity(machine_T1, family_F3, piece_gear, step_hard_turning), 50)
    #
    # fm_problem.set_initial_value(
    #     has_capacity(machine_T2, family_F3, piece_gear, step_hard_turning), 50)
    # fm_problem.set_initial_value(
    #     has_capacity(machine_T2, family_F2, piece_gear, step_hard_turning), 50)
    #
    # for f in all_families:
    #     fm_problem.set_initial_value(
    #         has_capacity(machine_T3, f, piece_pinion, step_hard_turning), 50
    #     )

    # lapping
    fm_problem.set_initial_value(
        has_capacity(machine_L1, family_F1, piece_gear, step_lapping), 20)
    fm_problem.set_initial_value(
        has_capacity(machine_L1, family_F3, piece_gear, step_lapping), 20)
    fm_problem.set_initial_value(
        has_capacity(machine_L1, family_F2, piece_gear, step_lapping), 20)

    fm_problem.set_initial_value(
        has_capacity(machine_L1, family_F1, piece_pinion, step_lapping), 20)
    fm_problem.set_initial_value(
        has_capacity(machine_L1, family_F3, piece_pinion, step_lapping), 20)
    fm_problem.set_initial_value(
        has_capacity(machine_L1, family_F2, piece_pinion, step_lapping), 20)

    fm_problem.set_initial_value(
        has_capacity(machine_L2, family_F1, piece_gear, step_lapping), 25)
    fm_problem.set_initial_value(
        has_capacity(machine_L2, family_F1, piece_gear, step_lapping), 25)


    fm_problem.add_fluent(is_machine_used)
    for m in all_machines:
        fm_problem.set_initial_value(is_machine_used(m), FALSE())

    fm_problem.add_fluent(nb_elements_in_machine)
    for m in all_machines:
        fm_problem.set_initial_value(nb_elements_in_machine(m), 0)

    fm_problem.add_fluent(duration)
    for s in all_steps:
        for m in all_machines:
            for f in all_families:
                for p in all_pieces:
                    fm_problem.set_initial_value(duration(s, m, f, p), 0)

    for f in all_families:
        fm_problem.set_initial_value(duration(step_annealing, machine_A1, f, piece_gear), 15)
        fm_problem.set_initial_value(duration(step_annealing, machine_A1, f, piece_pinion), 15)
        fm_problem.set_initial_value(duration(step_annealing, machine_A2, f, piece_gear), 15)
        fm_problem.set_initial_value(duration(step_annealing, machine_A2, f, piece_pinion), 15)

    fm_problem.set_initial_value(
        duration(step_cutting, machine_C1, family_F1, piece_pinion), 5)
    fm_problem.set_initial_value(
        duration(step_cutting, machine_C1, family_F3, piece_pinion), 6)

    fm_problem.set_initial_value(
        duration(step_cutting, machine_C2, family_F1, piece_pinion), 15)
    fm_problem.set_initial_value(
        duration(step_cutting, machine_C2, family_F2, piece_pinion), 15)
    fm_problem.set_initial_value(
        duration(step_cutting, machine_C2, family_F3, piece_pinion), 12)

    for f in all_families:
        fm_problem.set_initial_value(
            duration(step_cutting, machine_C3, f, piece_gear), 13
        )


    # for f in all_families:
    #     fm_problem.set_initial_value(
    #         duration(step_heat_treatment, machine_H1, f, piece_pinion), 12)
    #     fm_problem.set_initial_value(
    #         duration(step_heat_treatment, machine_H2, f, piece_gear), 12)
    #     fm_problem.set_initial_value(
    #         duration(step_heat_treatment, machine_H2, f, piece_pinion), 12)
    #
    # fm_problem.set_initial_value(
    #     duration(step_hard_turning, machine_T1, family_F1, piece_gear), 3)
    # fm_problem.set_initial_value(
    #     duration(step_hard_turning, machine_T1, family_F3, piece_gear), 2)
    #
    # fm_problem.set_initial_value(
    #     duration(step_hard_turning, machine_T2, family_F3, piece_gear), 3)
    # fm_problem.set_initial_value(
    #     duration(step_hard_turning, machine_T2, family_F2, piece_gear), 3)
    #
    # for f in all_families:
    #     fm_problem.set_initial_value(
    #         duration(step_hard_turning, machine_T3, f, piece_pinion), 5
    #     )

    fm_problem.set_initial_value(
        duration(step_lapping, machine_L1, family_F1, piece_gear), 15)
    fm_problem.set_initial_value(
        duration(step_lapping, machine_L1, family_F3, piece_gear), 6)
    fm_problem.set_initial_value(
        duration(step_lapping, machine_L1, family_F2, piece_gear), 13)

    fm_problem.set_initial_value(
        duration(step_lapping, machine_L1, family_F1, piece_pinion), 15)
    fm_problem.set_initial_value(
        duration(step_lapping, machine_L1, family_F3, piece_pinion), 6)
    fm_problem.set_initial_value(
        duration(step_lapping, machine_L1, family_F2, piece_pinion), 13)

    fm_problem.set_initial_value(
        duration(step_lapping, machine_L2, family_F1, piece_gear), 15)

    fm_problem.set_initial_value(
        duration(step_lapping, machine_L2, family_F1, piece_pinion), 15)
