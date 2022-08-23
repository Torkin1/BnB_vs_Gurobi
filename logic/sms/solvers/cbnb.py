from copy import deepcopy
from logic.problem import Solver
from logic.sms import *


class CombinatorialBnB(Solver):
    """ an implementation of the Branch and Bound algorithm for solving Single Machine Scheduling Problem """

    def __init__(self, solver):
        """
        @param solver: which class of solver must be used to calculate bounds for generated subproblems
        """
        self.incumbentBound = float("inf")
        self.incumbent = None
        self.__solver = solver

    def branch(self, smsProblem):

        subProblems = []
        latestCompletion = -1
        
        # finds latest completion time among original jobs
        for j in smsProblem.jobs:
            if j.remainingTime == 0 and j.completionTime > latestCompletion:
                latestCompletion = j.completionTime
        
        # creates subproblems for each uncompleted job
        for j in smsProblem.jobs:
            if j.remainingTime > 0:

                # creates subproblem identical to the original, but current job is already scheduled after latest completion time among original jobs
                p = deepcopy(smsProblem)
                job = p.jobs[smsProblem.jobs.index(j)]
                job.startingTimes.append(max(latestCompletion + 1, job.releaseTime))
                job.completionTime = job.startingTimes[-1] + job.remainingTime
                job.remainingTime = 0

                # sets a solver which will be used to calculate bounds
                p.solver = self.__solver()

                # adds subproblem to the list of subproblems
                subProblems.append(p)
              
        return subProblems
    
    def getLevel(self, problem):
        """ calculates level of branching tree of problem p by counting how many jobs are already scheduled """

        level = 0
        for j in problem.jobs:
            if len(j.startingTimes) != 0:
                scheduled += 1

        return level
    
    def dominate(self, p, subProblems):

        # TODO: implement dominance rule
        return False
                
    def fathom(self, smsProblem) -> "True if problem does not need further decomposition, False otherwise":
        
        # applies fathoming rules
        smsProblemCopy = deepcopy(smsProblem)
        smsProblemCopy.solve()  # bounding
        if smsProblemCopy.value == float("nan") or smsProblemCopy.value >= self.incumbentBound:  
            return True
        if smsProblemCopy.value < self.incumbentBound:
            self.incumbentBound = smsProblemCopy.value
            self.incumbent = smsProblemCopy.jobs
            return False

    def __solve_bnb(self, smsProblems):

        if len(smsProblems) != 0:
            p = smsProblems.pop()
            if not self.dominate(p, smsProblems) and not self.fathom(p) :
                smsProblems += self.branch(p)
            self.__solve_bnb(smsProblems)
    
    def __call__(self, smsProblem):
        """ solves problem using BnB algorithm"""

        problems = self.branch(smsProblem)

        self.__solve_bnb(problems)

        smsProblem.jobs = self.incumbent
        smsProblem.value = self.incumbentBound