from logic.sms.entities import SingleMachineScheduling, Job, Machine
from logic.sms.solvers.sptf import SPTFRuleScheduler
from logic.sms.solvers.cbnb import CombinatorialBnB
from logic.sms.targets import WeightedCompletionsSum
from unittest import TestCase

class Solver_Test(TestCase):

    params = []
    
    @classmethod
    def setUpClass(cls):
        cls.params = [
    ([ Job(0, 7, 0, 13, 1), Job(1, 5, 10, 13, 1), Job(2, 14, 3, 13, 1), Job(3, 2, 3, 13, 1) ], 57, SPTFRuleScheduler()),
    ([ Job(0, 7, 0, 13, 1), Job(1, 5, 0, 13, 1), Job(2, 14, 0, 13, 1), Job(3, 2, 0, 13, 1) ], 51, CombinatorialBnB(SPTFRuleScheduler)),
    ([ Job(0, 7, 0, 13, 1), Job(1, 5, 10, 13, 1), Job(2, 14, 3, 13, 1), Job(3, 2, 3, 13, 1) ], 57, CombinatorialBnB(SPTFRuleScheduler)),
     ]
 
    def test_solver(self):
        for jobs, expected, solver in self.params:
            with self.subTest():
                p = SingleMachineScheduling(jobs, Machine(0))
                p.solver = solver
                p.target = WeightedCompletionsSum()
                p.solve()
                self.assertEquals(expected, p.value)                 
