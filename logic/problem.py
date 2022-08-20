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
    
    def __init__(self):

        self.__solver = None
        """ Each problem must be initalized with a solver that knows how to solve the problem """

        self.target = None
        """ target function """

        self.value = -1
        """ value of the last calculation of target function """

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

