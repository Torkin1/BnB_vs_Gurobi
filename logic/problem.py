from abc import ABC, abstractmethod

class Target(ABC):
    """ target functon interface"""

    @abstractmethod
    def __call__(self, problem):
        pass

class Solver(ABC):
    """ Solver interface"""
    
    @abstractmethod
    def solve(self, problem):
        pass

class Problem(ABC):
    
    '''
    Problem interface
    '''
    
    solver = None
    """ Each problem must be initalized with a solver that knows how to solve the problem """

    vars = {}
    """ values of variables of the problem. It can contain values for single variables (x = 1) or for vectors of variables (x = [x1 = 1, x2 = 0, ...])"""

    target = None
    """ target function """

    value = -1
    """ value of the last calculation of target function """

    def solve(self):
        self.solver.solve()

