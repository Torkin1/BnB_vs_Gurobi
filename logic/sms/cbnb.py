from copy import deepcopy
from logic.problem import Solver
from logic.sms.entities import SingleMachineScheduling, Job, Machine
from logic.bnb import BranchAndBound
from treelib import Node

class CombinatorialBnB(BranchAndBound):
    """ an implementation of the Branch and Bound algorithm for solving Single Machine Scheduling Problem """
    
    def branch(self, smsProblemNode):

        subProblemNodes = []
        smsProblem = smsProblemNode.data
        
        # creates subproblems for each uncompleted job
        for j in smsProblem.vars:
            if j.remainingTime > 0:

                # creates subproblem identical to the original
                smsProblemCopy = deepcopy(smsProblem)
                jobCopy = smsProblemCopy.vars[smsProblem.vars.index(j)]
                if smsProblemCopy.machine.currentlyScheduled is None or jobCopy.id != smsProblemCopy.machine.currentlyScheduled.id:
                    
                    # schedules another job
                    startingTime = max(smsProblem.machine.currentTime, jobCopy.releaseTime)
                    jobCopy.startingTimes.append(startingTime)
                    smsProblemCopy.machine.currentlyScheduled = jobCopy
                    progress = startingTime - smsProblem.machine.currentTime + 1   
                else:
                    
                    # keeps scheduled the current job
                    progress = 1

                # updates machine time and currently scheduled remaining time
                smsProblemCopy.machine.currentTime += progress
                smsProblemCopy.machine.currentlyScheduled.remainingTime -= progress

                # checks if job has been completed 
                if smsProblemCopy.machine.currentlyScheduled.remainingTime <= 0:
                    smsProblemCopy.machine.currentlyScheduled.remainingTime = 0
                    smsProblemCopy.machine.currentlyScheduled.completionTime = smsProblemCopy.machine.currentTime
                    smsProblemCopy.machine.completed += 1

                # sets a solver which will be used to calculate bounds
                smsProblemCopy.solver = self.subSolverClass()

                # adds subproblem to the list of subproblems
                subProblemNodes.append(Node(identifier=smsProblemCopy, data=smsProblemCopy))
              
        return subProblemNodes
        
    def isDominated(self, pNode):
        
        k = pNode.data.machine.currentlyScheduled        
        sNodes = self.problemsTree.siblings(pNode.identifier)
        for s in sNodes:
            # Problem is dominated if job k is released after the estimated
            # completion time of the currently scheduled job in all other sibling problems,
            # assuming that no preemption occurs.
            j = s.data.machine.currentlyScheduled
            if k.releaseTime <= s.data.machine.currentTime + j.remainingTime:
                return False
        return True
                
    def isFathomed(self, toFathomNode):
        
        # a dominated problem can be immediately considered as fathomed
        if self.isDominated(toFathomNode):
            return True
        
        # calculates bound for the problem
        toFathom = toFathomNode.data
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
