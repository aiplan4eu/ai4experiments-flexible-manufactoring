from fm_demo_process.fm_process_fluents import *

########################################################## Cutting
a_cutting_capacity = DurativeAction(
    "action_cutting_capacity",
    machine=type_machine,
    family=type_family,
    piece=type_piece
)
cutting_machine_capacity = a_cutting_capacity.parameter("machine")
cutting_family_capacity = a_cutting_capacity.parameter("family")
cutting_piece_capacity = a_cutting_capacity.parameter("piece")
a_cutting_capacity.set_fixed_duration(duration(step_cutting, cutting_machine_capacity, cutting_family_capacity, cutting_piece_capacity))

a_cutting_capacity.add_condition(
    StartTiming(),
    And(
        # this machine is not currently in used
        Not(is_machine_used(cutting_machine_capacity)),
        # this machine can turn (used for step + capacity)
        GT(has_capacity(cutting_machine_capacity, cutting_family_capacity, cutting_piece_capacity, step_cutting), 0),
        # there is something to be done
        GT(to_be_processed(step_cutting, cutting_family_capacity, cutting_piece_capacity), 0),
        # there is enough items in the input buffer to perform the task
        GE(stock_after(step_annealing, cutting_family_capacity, cutting_piece_capacity), to_be_processed(step_cutting, cutting_family_capacity, cutting_piece_capacity)),
    )
)

# the machine is processing
a_cutting_capacity.add_effect(
    StartTiming(),
    is_machine_used(cutting_machine_capacity),
    TRUE()
)

# we store the amount in the machine in use
a_cutting_capacity.add_effect(
    StartTiming(),
    nb_elements_in_machine(cutting_machine_capacity),
    has_capacity(cutting_machine_capacity, cutting_family_capacity, cutting_piece_capacity, step_cutting)
)

# the input buffer is reduced
a_cutting_capacity.add_effect(
    StartTiming(),
    stock_after(step_annealing, cutting_family_capacity, cutting_piece_capacity),
    stock_after(step_annealing, cutting_family_capacity, cutting_piece_capacity)
    - has_capacity(cutting_machine_capacity, cutting_family_capacity, cutting_piece_capacity, step_cutting)
)

# the amount to be turned is reduced
a_cutting_capacity.add_effect(
    StartTiming(),
    to_be_processed(step_cutting, cutting_family_capacity, cutting_piece_capacity),
    to_be_processed(step_cutting, cutting_family_capacity, cutting_piece_capacity)
    - has_capacity(cutting_machine_capacity, cutting_family_capacity, cutting_piece_capacity, step_cutting)
)

# at the end the machine is not used anymore
a_cutting_capacity.add_effect(
    EndTiming(),
    is_machine_used(cutting_machine_capacity),
    FALSE()
)

# at the end the output buffer is increased:
a_cutting_capacity.add_effect(
    EndTiming(),
    stock_after(step_cutting, cutting_family_capacity, cutting_piece_capacity),
    stock_after(step_cutting, cutting_family_capacity, cutting_piece_capacity)
    + nb_elements_in_machine(cutting_machine_capacity)
)
