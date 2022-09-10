from logic.sms.entities import SingleMachineScheduling, Job, Machine
from logic.sms.sptf import SPTFRuleScheduler
from logic.sms.cbnb import CombinatorialBnB
from logic.sms.completions_sum import WeightedCompletionsSum
from logic.sms.gurobi import GurobiSolver, SMS_LP_minWeightedSum_timeIndexed, UpdateValue
from unittest import TestCase
from copy import deepcopy

class Solver_Test(TestCase):

    params = []
    
    @classmethod
    def setUpClass(cls):
        jobs = [ Job(0, 7, 0, 13, 1), Job(1, 5, 10, 13, 1), Job(2, 14, 3, 13, 1), Job(3, 2, 3, 13, 1) ]
        cls.params = [
            (53, SPTFRuleScheduler(), WeightedCompletionsSum(), SingleMachineScheduling(deepcopy(jobs), Machine(0))),
            (53, CombinatorialBnB(SPTFRuleScheduler), WeightedCompletionsSum(), SingleMachineScheduling(deepcopy(jobs), Machine(0))),
            (53, GurobiSolver(), UpdateValue(), SMS_LP_minWeightedSum_timeIndexed(deepcopy(jobs))),
        ]
 
    def test_solver(self):
        for expected, solver, objective, problem in self.params:
            with self.subTest(solver=solver, objective=objective, problem=problem):
                p = problem
                p.solver = solver
                p.objective = objective
                p.solve()
                self.assertEquals(expected, p.value)
