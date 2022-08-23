from copy import deepcopy
from logic.problem import Solver
from logic.sms.entities import SingleMachineScheduling, Job
from logic.bnb import BranchAndBound


class CombinatorialBnB(BranchAndBound):
    """ an implementation of the Branch and Bound algorithm for solving Single Machine Scheduling Problem """

    def branch(self, smsProblem):

        subProblems = []
        latestCompletion = -1
        
        # finds latest completion time among original jobs
        for j in smsProblem.vars:
            if j.remainingTime == 0 and j.completionTime > latestCompletion:
                latestCompletion = j.completionTime
        
        # creates subproblems for each uncompleted job
        for j in smsProblem.vars:
            if j.remainingTime > 0:

                # creates subproblem identical to the original, but current job is already scheduled after latest completion time among original jobs
                smsProblemCopy = deepcopy(smsProblem)
                job = smsProblemCopy.vars[smsProblem.vars.index(j)]
                job.startingTimes.append(max(latestCompletion + 1, job.releaseTime))
                job.completionTime = job.startingTimes[-1] + job.remainingTime
                job.remainingTime = 0

                # sets a solver which will be used to calculate bounds
                smsProblemCopy.solver = self.subSolverClass()

                # adds subproblem to the list of subproblems
                subProblems.append(smsProblemCopy)
              
        return subProblems
    
    def getLevel(self, problem):
        """ calculates level of branching tree of problem p by counting how many jobs are already scheduled """

        level = 0
        for j in problem.vars:
            if len(j.startingTimes) != 0:
                scheduled += 1

        return level
    
    def dominate(self, p, subProblems):

        # TODO: implement dominance rule
        return False
                
    def fathom(self, toFathom, otherProblems) -> "True if problem does not need further decomposition, False otherwise":
        
        # a dominated problem can be immediately considered as fathomed
        if self.dominate(toFathom, otherProblems):
            return True
        
        # calculates bound for the problem
        toFathomCopy = deepcopy(toFathom)
        toFathomCopy.solve()  # bounding
        if toFathomCopy.value == float("nan") or toFathomCopy.value >= self.incumbentBound: 
            
            # bound is worse than the incumbent bound, so the problem can be fathomed
            return True
        
        if toFathomCopy.value < self.incumbentBound:
            
            # bound is better than the incumbent bound, so the problem can be further decomposed
            self.incumbentBound = toFathomCopy.value
            self.incumbent = toFathomCopy.vars
            return False
