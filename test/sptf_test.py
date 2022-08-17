from logic.entities import *
from unittest import TestCase

class SPTF_test(TestCase):

    params = []
    p = None
    
    @classmethod
    def setUpClass(cls):
        cls.params = [
     ([ Job(1, 7, 0, 13, 0), Job(2, 5, 10, 13, 0), Job(3, 14, 3, 13, 0), Job(4, 2, 3, 13, 0) ], [(1,0), (4,3), (1,5), (3,9), (2,10), (3,15)])
     ]
 
    def test_sptf(self):
        for jobs, expected in self.params:
            with self.subTest():
                p = SMS_timeIndexed(jobs)
                p.solver = SPTFfRuleSolver()
                p.target = WeightedCompletionsSum()
                actual = p.solver.solve(p)
                self.assertEqual(expected, actual)  
