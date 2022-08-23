from logic.sms.entities import SingleMachineScheduling, Job
from logic.sms.solvers.sptf import SPTFRuleSolver
from logic.sms.solvers.cbnb import CombinatorialBnB
from logic.sms.targets import WeightedCompletionsSum
from unittest import TestCase

class Solver_Test(TestCase):

    params = []
    
    @classmethod
    def setUpClass(cls):
        cls.params = [
    ([ Job(0, 7, 0, 13, 1), Job(1, 5, 10, 13, 1), Job(2, 14, 3, 13, 1), Job(3, 2, 3, 13, 1) ], 57, SPTFRuleSolver()),
    # TODO: need to find an expected schedule for the bnb test case.
    #       Anyway, analyzing the execution with debugging mode seems to show that the algorithm works as expected.
    ([ Job(0, 7, 0, 13, 1), Job(1, 5, 10, 13, 1), Job(2, 14, 3, 13, 1), Job(3, 2, 3, 13, 1) ], 57, CombinatorialBnB(SPTFRuleSolver))
     ]
 
    def test_solver(self):
        for jobs, expected, solver in self.params:
            with self.subTest():
                p = SingleMachineScheduling(jobs)
                p.solver = solver
                p.target = WeightedCompletionsSum()
                p.solve()
                self.assertTrue(p.value == expected)                 
