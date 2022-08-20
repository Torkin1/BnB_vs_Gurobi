from logic.sms import *
from unittest import TestCase

class Solver_Test(TestCase):

    params = []
    
    @classmethod
    def setUpClass(cls):
        cls.params = [
    #([ Job(0, 7, 0, 13, 1), Job(1, 5, 10, 13, 1), Job(2, 14, 3, 13, 1), Job(3, 2, 3, 13, 1) ], [[0,5], [10], [9,15], [3]], SPTFRuleSolver()),
    ([ Job(0, 7, 0, 13, 1), Job(1, 5, 10, 13, 1), Job(2, 14, 3, 13, 1), Job(3, 2, 3, 13, 1) ], [[0,5], [10], [9,15], [3]], CombinatorialBnB(SPTFRuleSolver))
     ]
 
    def test_solver(self):
        for jobs, expected, solver in self.params:
            with self.subTest():
                p = SingleMachineScheduling()
                p.jobs = jobs
                p.solver = solver
                p.target = WeightedCompletionsSum()
                p.solve()
                for i in range(0, len(jobs)):
                    self.assertEquals(expected[i], p.jobs[i].startingTimes)
                 
