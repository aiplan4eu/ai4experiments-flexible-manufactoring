from fm_demo_process.fm_process_fluents import *

########################################################## Annealing
a_annealing_capacity = DurativeAction(
    "action_annealing_capacity",
    machine=type_machine,
    family=type_family,
    piece=type_piece
)
annealing_machine_capacity = a_annealing_capacity.parameter("machine")
annealing_family_capacity = a_annealing_capacity.parameter("family")
annealing_piece_capacity = a_annealing_capacity.parameter("piece")
a_annealing_capacity.set_fixed_duration((duration(step_annealing, annealing_machine_capacity, annealing_family_capacity, annealing_piece_capacity)))

a_annealing_capacity.add_condition(
    StartTiming(),
    And(
        # this machine is not currently in used
        Not(is_machine_used(annealing_machine_capacity)),
        # this machine can anneal
        GT(has_capacity(annealing_machine_capacity, annealing_family_capacity, annealing_piece_capacity, step_annealing), 0),
        # there is actually something to be done, i.e. we need to anneal some pieces and can't just take the stock
        GT(to_be_processed(step_annealing, annealing_family_capacity, annealing_piece_capacity), 0),
        # there is enough items in the input buffer to perform the task
        GE(buff_start(annealing_family_capacity, annealing_piece_capacity),
           to_be_processed(step_annealing, annealing_family_capacity, annealing_piece_capacity)),
    )
)

# the machine is being used
a_annealing_capacity.add_effect(
    StartTiming(),
    is_machine_used(annealing_machine_capacity),
    TRUE()
)

# we store the amount in the machine as currently being processed
a_annealing_capacity.add_effect(
    StartTiming(),
    nb_elements_in_machine(annealing_machine_capacity),
    has_capacity(annealing_machine_capacity, annealing_family_capacity, annealing_piece_capacity, step_annealing)
)

# the input buffer is reduced
a_annealing_capacity.add_effect(
    StartTiming(),
    buff_start(annealing_family_capacity, annealing_piece_capacity),
    buff_start(annealing_family_capacity, annealing_piece_capacity) -
    has_capacity(annealing_machine_capacity, annealing_family_capacity, annealing_piece_capacity, step_annealing)
)

# the to_be_annealed amount is reduced
a_annealing_capacity.add_effect(
    StartTiming(),
    to_be_processed(step_annealing, annealing_family_capacity, annealing_piece_capacity),
    to_be_processed(step_annealing, annealing_family_capacity, annealing_piece_capacity) -
    has_capacity(annealing_machine_capacity, annealing_family_capacity, annealing_piece_capacity, step_annealing)
)

# at the end, the machine is not in used anymore
a_annealing_capacity.add_effect(
    EndTiming(),
    is_machine_used(annealing_machine_capacity),
    FALSE()
)

# at the end, the output buffer is increased
a_annealing_capacity.add_effect(
    EndTiming(),
    stock_after(step_annealing, annealing_family_capacity, annealing_piece_capacity),
    stock_after(step_annealing, annealing_family_capacity, annealing_piece_capacity) +
    nb_elements_in_machine(annealing_machine_capacity),
    )
