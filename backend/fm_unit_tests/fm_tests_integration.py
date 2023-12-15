from unified_planning.io import PDDLWriter
from unified_planning.plans import ActionInstance
from fm_demo_process.fm_problem import *

import unittest


class TestFMProcessIntegration(unittest.TestCase):
    def _check_assertion_timed_action(self, a1, a2):
        #print("a1: {0} \na2: {1}".format(a1, a2))
        assert(a1[0] == a2[0]) # start time

        a1_str = "{0}".format(a1[1])
        a2_str = "{0}".format(a2[1])
        assert(a1_str == a2_str) # action

        assert(a1[2] == a2[2]) # end time
    def setUp(self):
        self.problem = create_fm_problem()
        self.planner_name = "tamer"
        self.heuristic = "hadd"

    def test_to_cut_gear(self):
        self.problem.set_initial_value(buff_start(family_F1, piece_gear), 3000)
        self.problem.set_initial_value(expected_final_output(family_F1), 5)
        self.problem.add_goal(GE(stock_after(step_cutting, family_F1, piece_gear), expected_final_output(family_F1)))

        init_domain_from_initial_values(self.problem)

        with OneshotPlanner(name=self.planner_name, params={"heuristic" : self.heuristic}) as planner:
            result = planner.solve(self.problem)
            print("{0}\n{1}".format(result.status, result.plan))
            assert(result.status == up.engines.PlanGenerationResultStatus.SOLVED_SATISFICING)
            assert(len(result.plan.timed_actions) == 2)

    def test_to_cut_pinion(self):
        self.problem.set_initial_value(buff_start(family_F1, piece_pinion), 3000)
        self.problem.set_initial_value(expected_final_output(family_F1), 1)
        self.problem.add_goal(GE(stock_after(step_cutting, family_F1, piece_pinion), expected_final_output(family_F1)))

        init_domain_from_initial_values(self.problem)

        with OneshotPlanner(name=self.planner_name, params={"heuristic" : self.heuristic}) as planner:
            result = planner.solve(self.problem)
            assert(result.status == up.engines.PlanGenerationResultStatus.SOLVED_SATISFICING)
            assert(len(result.plan.timed_actions) == 2)
            print("{0}".format(result.plan))

    # def test_to_hard_turned_gear(self):
    #     self.problem.set_initial_value(buff_start(family_F1, piece_gear), 3000)
    #     self.problem.set_initial_value(expected_final_output(family_F1), 1)
    #
    #     self.problem.add_goal(GE(stock_after(step_hard_turning, family_F1, piece_gear), expected_final_output(family_F1)))
    #
    #     init_domain_from_initial_values(self.problem)
    #
    #     with OneshotPlanner(name=self.planner_name, params={"heuristic" : self.heuristic}) as planner:
    #         result = planner.solve(self.problem)
    #         print("{0}\n{1}".format(result.status, result.plan))
    #         assert(result.status == up.engines.PlanGenerationResultStatus.SOLVED_SATISFICING)
    #         assert(len(result.plan.timed_actions) == 4)
    #
    # def test_to_hard_turned_pinion(self):
    #     self.problem.set_initial_value(buff_start(family_F1, piece_pinion), 3000)
    #     self.problem.set_initial_value(expected_final_output(family_F1), 1)
    #     self.problem.add_goal(GE(stock_after(step_hard_turning, family_F1, piece_pinion), expected_final_output(family_F1)))
    #
    #     init_domain_from_initial_values(self.problem)
    #
    #     with OneshotPlanner(name=self.planner_name, params={"heuristic" : self.heuristic}) as planner:
    #         result = planner.solve(self.problem)
    #         print("{0}\n{1}".format(result.status, result.plan))
    #         assert(result.status == up.engines.PlanGenerationResultStatus.SOLVED_SATISFICING)
    #         assert(len(result.plan.timed_actions) == 4)


    def test_from_cut(self):
        self.problem.set_initial_value(stock_after(step_cutting, family_F1, piece_pinion), 3000)
        self.problem.set_initial_value(stock_after(step_cutting, family_F1, piece_gear), 3000)
        self.problem.set_initial_value(expected_final_output(family_F1), 1)
        self.problem.add_goal(GE(stock_lapped(family_F1), expected_final_output(family_F1)))

        init_domain_from_initial_values(self.problem)

        with OneshotPlanner(name=self.planner_name, params={"heuristic" : self.heuristic}) as planner:
            result = planner.solve(self.problem)
            print("{0}\n{1}".format(result.status, result.plan))
            assert(result.status == up.engines.PlanGenerationResultStatus.SOLVED_SATISFICING)
            assert(len(result.plan.timed_actions) == 5)


    def test_from_annealed(self):
        self.problem.set_initial_value(stock_after(step_annealing, family_F1, piece_pinion), 3000)
        self.problem.set_initial_value(stock_after(step_annealing, family_F1, piece_gear), 3000)
        self.problem.set_initial_value(expected_final_output(family_F1), 1)
        self.problem.add_goal(GE(stock_lapped(family_F1), expected_final_output(family_F1)))

        init_domain_from_initial_values(self.problem)

        with OneshotPlanner(name=self.planner_name, params={"heuristic" : self.heuristic}) as planner:
            result = planner.solve(self.problem)
            print("{0}\n{1}".format(result.status, result.plan))
            assert(result.status == up.engines.PlanGenerationResultStatus.SOLVED_SATISFICING)
            assert(len(result.plan.timed_actions) == 7)

    def test_full_process_capacity(self):
        self.problem.set_initial_value(buff_start(family_F1, piece_pinion), 3000)
        self.problem.set_initial_value(buff_start(family_F1, piece_gear), 3000)
        self.problem.set_initial_value(expected_final_output(family_F1), 20)

        self.problem.add_goal(GE(stock_lapped(family_F1), expected_final_output(family_F1)))

        init_domain_from_initial_values(self.problem)
        print("{0}".format(self.problem.kind))

        with OneshotPlanner(name=self.planner_name, params={"heuristic" : self.heuristic}) as planner:
            result = planner.solve(self.problem)
            print("{0}\n{1}".format(result.status, result.plan))
            assert(result.status == up.engines.PlanGenerationResultStatus.SOLVED_SATISFICING)

    def test_full_process_multiple_families(self):
        self.problem.set_initial_value(buff_start(family_F1, piece_pinion), 3000)
        self.problem.set_initial_value(buff_start(family_F1, piece_gear), 3000)
        self.problem.set_initial_value(expected_final_output(family_F1), 20)

        self.problem.set_initial_value(buff_start(family_F2, piece_pinion), 3000)
        self.problem.set_initial_value(buff_start(family_F2, piece_gear), 3000)
        self.problem.set_initial_value(expected_final_output(family_F2), 20)

        self.problem.add_goal(GE(stock_lapped(family_F1), expected_final_output(family_F1)))
        self.problem.add_goal(GE(stock_lapped(family_F2), expected_final_output(family_F1)))

        init_domain_from_initial_values(self.problem)
        print("{0}".format(self.problem.kind))

        with OneshotPlanner(name=self.planner_name, params={"heuristic" : self.heuristic}) as planner:
            result = planner.solve(self.problem)
            print("{0}\n{1}".format(result.status, result.plan))
            assert(result.status == up.engines.PlanGenerationResultStatus.SOLVED_SATISFICING)
