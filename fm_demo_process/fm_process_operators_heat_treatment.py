# from fm_demo_process.fm_process_fluents import *
#
# ########################################################## Cutting
# a_heat_treatment_capacity = DurativeAction(
#     "action_heat_treatment_capacity",
#     machine=type_machine,
#     family=type_family,
#     piece=type_piece
# )
# heat_treatment_machine_capacity = a_heat_treatment_capacity.parameter("machine")
# heat_treatment_family_capacity = a_heat_treatment_capacity.parameter("family")
# heat_treatment_piece_capacity = a_heat_treatment_capacity.parameter("piece")
# a_heat_treatment_capacity.set_fixed_duration(duration(step_heat_treatment, heat_treatment_machine_capacity, heat_treatment_family_capacity, heat_treatment_piece_capacity))
#
# a_heat_treatment_capacity.add_condition(
#     StartTiming(),
#     And(
#         # this machine is not currently in used
#         Not(is_machine_used(heat_treatment_machine_capacity)),
#         # this machine can turn (used for step + capacity)
#         GT(has_capacity(heat_treatment_machine_capacity, heat_treatment_family_capacity, heat_treatment_piece_capacity, step_heat_treatment), 0),
#         # there is something to be done
#         GT(to_be_processed(step_heat_treatment, heat_treatment_family_capacity, heat_treatment_piece_capacity), 0),
#         # there is enough items in the input buffer to perform the task
#         GE(stock_after(step_cutting, heat_treatment_family_capacity, heat_treatment_piece_capacity), to_be_processed(step_heat_treatment, heat_treatment_family_capacity, heat_treatment_piece_capacity)),
#     )
# )
#
# # the machine is processing
# a_heat_treatment_capacity.add_effect(
#     StartTiming(),
#     is_machine_used(heat_treatment_machine_capacity),
#     TRUE()
# )
#
# # we store the amount in the machine in use
# a_heat_treatment_capacity.add_effect(
#     StartTiming(),
#     nb_elements_in_machine(heat_treatment_machine_capacity),
#     has_capacity(heat_treatment_machine_capacity, heat_treatment_family_capacity, heat_treatment_piece_capacity, step_heat_treatment)
# )
#
# # the input buffer is reduced
# a_heat_treatment_capacity.add_effect(
#     StartTiming(),
#     stock_after(step_cutting, heat_treatment_family_capacity, heat_treatment_piece_capacity),
#     stock_after(step_cutting, heat_treatment_family_capacity, heat_treatment_piece_capacity)
#     - has_capacity(heat_treatment_machine_capacity, heat_treatment_family_capacity, heat_treatment_piece_capacity, step_heat_treatment)
# )
#
# # the amount to be turned is reduced
# a_heat_treatment_capacity.add_effect(
#     StartTiming(),
#     to_be_processed(step_heat_treatment, heat_treatment_family_capacity, heat_treatment_piece_capacity),
#     to_be_processed(step_heat_treatment, heat_treatment_family_capacity, heat_treatment_piece_capacity)
#     - has_capacity(heat_treatment_machine_capacity, heat_treatment_family_capacity, heat_treatment_piece_capacity, step_heat_treatment)
# )
#
# # at the end the machine is not used anymore
# a_heat_treatment_capacity.add_effect(
#     EndTiming(),
#     is_machine_used(heat_treatment_machine_capacity),
#     FALSE()
# )
#
# # at the end the output buffer is increased:
# a_heat_treatment_capacity.add_effect(
#     EndTiming(),
#     stock_after(step_heat_treatment, heat_treatment_family_capacity, heat_treatment_piece_capacity),
#     stock_after(step_heat_treatment, heat_treatment_family_capacity, heat_treatment_piece_capacity)
#     + nb_elements_in_machine(heat_treatment_machine_capacity)
# )
