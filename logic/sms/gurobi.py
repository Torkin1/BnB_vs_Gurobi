import gurobipy as gp
from gurobipy import GRB
from logic.problem import Problem, Solver, Objective

MAX_TIME = 200 
"""time horizon"""

class UpdateValue(Objective):
    """ update the value of the problem according to gurobi solution """

    def __call__(self, problem):
        if problem.vars.status == GRB.OPTIMAL:
            return problem.vars.objVal
        elif problem.vars.status == GRB.INFEASIBLE:
            return float('nan')
        elif problem.vars.status == GRB.UNBOUNDED:
            return float('inf')
        else:
            return None

class SMS_LP_minWeightedSum_timeIndexed(Problem):
    """A time indxed LP formulation of the SMS problem"""

    def __init__(self, jobs):
        """@param jobs: list of jobs to schedule"""

        super().__init__()
        
        self.objective = UpdateValue()
        
        self.vars = gp.Model("smsModel")
        model = self.vars
        
        # sets up time indexed matrix variable
        x = model.addVars(len(jobs), MAX_TIME, vtype=GRB.BINARY, name="x")
        """x[j, t]: 1 if job j is in service at time t, else 0"""
        c = model.addVars(len(jobs), vtype=GRB.INTEGER, lb=1, name="c")
        """C[j]: completion time of job j"""

        # sets up objective function
        toSum = gp.LinExpr()
        for j in range(len(jobs)):
            toSum += jobs[j].weight * c[j]
        model.setObjective(toSum, GRB.MINIMIZE)

        # add constraints
        for t in range(MAX_TIME):
            model.addConstr(x.sum('*', t) <= 1, name=f"time_slot_{t}_can_be_used_by_at_most_one_job")
        for j in range(len(jobs)):
            model.addConstr(x.sum(j, '*') == jobs[j].processingTime, f"sum_of_service_times_of_job_{j}_must_be_equal_to_its_processing_time")
            for t in range(MAX_TIME):
                model.addConstr(c[j] >= t * x[j, t], f"completion_time_of_job_{j}_must_be_greater_than_or_equal_to_time_service_{t}")
                if t < jobs[j].releaseTime:
                    model.addConstr(x[j, t] <= 0, f"cannot_execute_job_{j}_in_time_{t}_because_it_has_not_been_released_yet")

class GurobiSolver(Solver):

    def __call__(self, problem):

        problem.vars.optimize()
