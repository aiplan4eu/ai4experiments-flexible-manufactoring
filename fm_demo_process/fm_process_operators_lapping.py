from fm_demo_process.fm_process_fluents import *
########################################################## Lapping

a_lapping_capacity = DurativeAction("action_lapping_capacity",
                                    machine=type_machine,
                                    family=type_family
                                    )

lapping_machine_capacity = a_lapping_capacity.parameter("machine")
lapping_family_capacity = a_lapping_capacity.parameter("family")
a_lapping_capacity.set_fixed_duration(duration(step_lapping, lapping_machine_capacity, lapping_family_capacity, piece_gear))

a_lapping_capacity.add_condition(
    StartTiming(),
    And(
        # sanity check that the machine has the same capacity for piece_gears and piece_pinions
        Equals(has_capacity(lapping_machine_capacity, lapping_family_capacity, piece_gear, step_lapping),
               has_capacity(lapping_machine_capacity, lapping_family_capacity, piece_pinion, step_lapping)),
        # then we only use piece_gear
        # the machine is not currently in use
        Not(is_machine_used(lapping_machine_capacity)),
        # the machine can lap
        GT(has_capacity(lapping_machine_capacity, lapping_family_capacity, piece_gear, step_lapping), 0),
        # there is actually something to lap
        GT(to_be_lapped(lapping_family_capacity), 0),
        # there is enough items in both input buffers
        GE(stock_after(step_cutting,lapping_family_capacity, piece_gear), to_be_lapped(lapping_family_capacity)),
        GE(stock_after(step_cutting,lapping_family_capacity, piece_pinion), to_be_lapped(lapping_family_capacity)),
    )
)

# the machine is processing
a_lapping_capacity.add_effect(
    StartTiming(),
    is_machine_used(lapping_machine_capacity),
    TRUE()
)

# we store the amount of items in the machine
a_lapping_capacity.add_effect(
    StartTiming(),
    nb_elements_in_machine(lapping_machine_capacity),
    has_capacity(lapping_machine_capacity, lapping_family_capacity, piece_gear, step_lapping)
)

# we reduce the size of the input buffers
a_lapping_capacity.add_effect(
    StartTiming(),
    stock_after(step_cutting,lapping_family_capacity, piece_gear),
    stock_after(step_cutting,lapping_family_capacity, piece_gear)
    - has_capacity(lapping_machine_capacity, lapping_family_capacity, piece_gear, step_lapping)
)

a_lapping_capacity.add_effect(
    StartTiming(),
    stock_after(step_cutting,lapping_family_capacity, piece_pinion),
    stock_after(step_cutting,lapping_family_capacity, piece_pinion)
    - has_capacity(lapping_machine_capacity, lapping_family_capacity, piece_pinion, step_lapping)
)

# the amount to be lapped is reduced
a_lapping_capacity.add_effect(
    StartTiming(),
    to_be_lapped(lapping_family_capacity),
    to_be_lapped(lapping_family_capacity)
    - has_capacity(lapping_machine_capacity, lapping_family_capacity, piece_gear, step_lapping)
)

# at the end the machine is not used anymore
a_lapping_capacity.add_effect(
    EndTiming(),
    is_machine_used(lapping_machine_capacity),
    FALSE()
)

# at the end, the output buffer is increased
a_lapping_capacity.add_effect(
    EndTiming(),
    stock_lapped(lapping_family_capacity),
    stock_lapped(lapping_family_capacity)
    + nb_elements_in_machine(lapping_machine_capacity)
)
