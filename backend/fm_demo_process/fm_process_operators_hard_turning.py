# from fm_demo_process.fm_process_fluents import *
#
# ########################################################## Cutting
# a_hard_turning_capacity = DurativeAction(
#     "action_hard_turning_capacity",
#     machine=type_machine,
#     family=type_family,
#     piece=type_piece
# )
# hard_turning_machine_capacity = a_hard_turning_capacity.parameter("machine")
# hard_turning_family_capacity = a_hard_turning_capacity.parameter("family")
# hard_turning_piece_capacity = a_hard_turning_capacity.parameter("piece")
# a_hard_turning_capacity.set_fixed_duration(duration(step_hard_turning, hard_turning_machine_capacity, hard_turning_family_capacity, hard_turning_piece_capacity))
#
# a_hard_turning_capacity.add_condition(
#     StartTiming(),
#     And(
#         # this machine is not currently in used
#         Not(is_machine_used(hard_turning_machine_capacity)),
#         # this machine can turn (used for step + capacity)
#         GT(has_capacity(hard_turning_machine_capacity, hard_turning_family_capacity, hard_turning_piece_capacity, step_hard_turning), 0),
#         # there is something to be done
#         GT(to_be_processed(step_hard_turning, hard_turning_family_capacity, hard_turning_piece_capacity), 0),
#         # there is enough items in the input buffer to perform the task
#         GE(stock_after(step_cutting, hard_turning_family_capacity, hard_turning_piece_capacity), to_be_processed(step_hard_turning, hard_turning_family_capacity, hard_turning_piece_capacity)),
#     )
# )
#
# # the machine is processing
# a_hard_turning_capacity.add_effect(
#     StartTiming(),
#     is_machine_used(hard_turning_machine_capacity),
#     TRUE()
# )
#
# # we store the amount in the machine in use
# a_hard_turning_capacity.add_effect(
#     StartTiming(),
#     nb_elements_in_machine(hard_turning_machine_capacity),
#     has_capacity(hard_turning_machine_capacity, hard_turning_family_capacity, hard_turning_piece_capacity, step_hard_turning)
# )
#
# # the input buffer is reduced
# a_hard_turning_capacity.add_effect(
#     StartTiming(),
#     stock_after(step_cutting, hard_turning_family_capacity, hard_turning_piece_capacity),
#     stock_after(step_cutting, hard_turning_family_capacity, hard_turning_piece_capacity)
#     - has_capacity(hard_turning_machine_capacity, hard_turning_family_capacity, hard_turning_piece_capacity, step_hard_turning)
# )
#
# # the amount to be turned is reduced
# a_hard_turning_capacity.add_effect(
#     StartTiming(),
#     to_be_processed(step_hard_turning, hard_turning_family_capacity, hard_turning_piece_capacity),
#     to_be_processed(step_hard_turning, hard_turning_family_capacity, hard_turning_piece_capacity)
#     - has_capacity(hard_turning_machine_capacity, hard_turning_family_capacity, hard_turning_piece_capacity, step_hard_turning)
# )
#
# # at the end the machine is not used anymore
# a_hard_turning_capacity.add_effect(
#     EndTiming(),
#     is_machine_used(hard_turning_machine_capacity),
#     FALSE()
# )
#
# # at the end the output buffer is increased:
# a_hard_turning_capacity.add_effect(
#     EndTiming(),
#     stock_after(step_hard_turning, hard_turning_family_capacity, hard_turning_piece_capacity),
#     stock_after(step_hard_turning, hard_turning_family_capacity, hard_turning_piece_capacity)
#     + nb_elements_in_machine(hard_turning_machine_capacity)
# )
