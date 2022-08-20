from logic.sms import *
from unittest import TestCase

class SPTF_test(TestCase):

    params = []
    
    @classmethod
    def setUpClass(cls):
        cls.params = [
     ([ Job(1, 7, 0, 13, 0), Job(2, 5, 10, 13, 0), Job(3, 14, 3, 13, 0), Job(4, 2, 3, 13, 0) ], [[0,5], [10], [9,15], [3]])
     ]
 
    def test_sptf(self):
        for jobs, expected in self.params:
            with self.subTest():
                p = SingleMachineScheduling()
                p.jobs = jobs
                p.solver = SPTFfRuleSolver()
                p.target = WeightedCompletionsSum()
                p.solve()
                for i in range(0, len(jobs)):
                    self.assertEquals(expected[i], p.jobs[i].startingTimes)
                 
