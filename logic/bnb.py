from abc import abstractmethod
from copy import deepcopy
from logic.problem import Solver

class BranchAndBound(Solver):
    """ an implementation of the Branch and Bound algorithm for solving Single Machine Scheduling Problem """

    def __init__(self, subSolverClass):

        self.incumbentBound = float("inf")  
        """value of incumbent bound"""
        self.incumbent = None   
        """a pointer to the incumbent solution, in the same format as the one used in given problem to solve"""
        self.subSolverClass = subSolverClass  
        """ a pointer to the solver class which will be instantiated to calculate bounds for generated subproblems """

    @abstractmethod
    def branch(self, problem):
        pass    
                    
    @abstractmethod
    def isFathomed(self, toFathom, otherProblems):
        """True if problem does not need further decomposition, False otherwise"""
        pass

    def __solve_bnb(self, problems):

        if len(problems) != 0:
            p = problems.pop()
            if not self.isFathomed(p, problems) :
                problems += self.branch(p)
            self.__solve_bnb(problems)
    
    def __call__(self, problem):
        """ solves problem using BnB algorithm"""

        problems = self.branch(problem)

        self.__solve_bnb(problems)

        problem.vars = self.incumbent
