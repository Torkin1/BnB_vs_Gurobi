"""
A generic description of a LP problem interface interface
"""
from abc import ABC, abstractmethod

class Target(ABC):
    """ target functon interface"""

    @abstractmethod
    def __call__(self, problem):
        pass

class Solver(ABC):
    """ Solver interface"""
    
    @abstractmethod
    def __call__(self, problem):
        pass

class Problem(ABC):
    
    '''
    Problem interface
    '''
    
    def getVars(self):
        return self._vars
    
    def setVars(self, vars):
        self._vars = vars

    def __init__(self):

        self.__solver = None
        """ Each problem must be initalized with a solver that knows how to solve the problem """

        self.target = None
        """ target function """

        self.value = None
        """ value of the last calculation of target function, according to the solver that attempted to solve the problem: follows semantics:
            - None: problem has not been solved yet.
            - nan: problem is infeasible
            - +inf | -inf: problem is feasible but unbounded
            - otherwise: problem is feasible, value is the optimum of the target function """
        
        self.vars = None
        """ pointer to the variables of the problem. Format of variables is defined by subclasses """

    @property
    def solver(self):
        return self.__solver
    
    @solver.setter
    def solver(self, solver):
        self.__solver = solver
    
    def solve(self):

        # calculate schedule
        self.__solver(self)
        
        # update value of target function
        self.value = self.target(self)            

