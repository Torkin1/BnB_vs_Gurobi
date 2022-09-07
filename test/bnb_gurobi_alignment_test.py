from logic.sms.entities import SingleMachineScheduling, Job, Machine
from logic.sms.sptf import SPTFRuleScheduler
from logic.sms.cbnb import CombinatorialBnB
from logic.sms.objectives import CompletionsSum
from logic.sms.gurobi import GurobiSolver, SMS_LP_minWeightedSum_timeIndexed, UpdateValue
from unittest import TestCase

class Solver_Test(TestCase):

    params = []
    
    @classmethod
    def setUpClass(cls):
        jobs = [ Job(0, 7, 0, 13, 1), Job(1, 5, 10, 13, 1), Job(2, 14, 3, 13, 1), Job(3, 2, 3, 13, 1) ]
        cls.params = [
            [ Job(0, 7, 0, 13, 1), Job(1, 5, 10, 13, 1), Job(2, 14, 3, 13, 1), Job(3, 2, 3, 13, 1) ],
        ]
 
    def test_solver(self):
        for jobs in self.params:
            with self.subTest():
                
                pBnb = SingleMachineScheduling(jobs, Machine(0))
                pBnb.solver = CombinatorialBnB(SPTFRuleScheduler)
                pBnb.objective = CompletionsSum()
                pBnb.solve()
                
                pGurobi = SMS_LP_minWeightedSum_timeIndexed(jobs)
                pGurobi.solver = GurobiSolver()
                pGurobi.objective = UpdateValue()
                pGurobi.solve()
                
                self.assertEquals(pBnb.value, pGurobi.value)                 
