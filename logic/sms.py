"""
A Single Machine Scheduling problem implementation with solvers and other tools
"""
from logic.problem import *
from copy import deepcopy

class WeightedCompletionsSum(Target):

    def __call__(self, smsProblem):

        weightedCompletions = []
        for j in smsProblem.jobs:
            weightedCompletions.append(j.weight * j.completionTime)
        return sum(weightedCompletions)

class SingleMachineScheduling(Problem):
    """
    Single Machine Scheduling Problem represented using time indexing
    """
    
    def __init__(self):
        self.jobs = []
        """Jobs to schedule on a single machine"""

class Job:
    """
    A job that can be scheduled on a single machine
    """

    def __init__(self, id=-1, processingTime=float('inf'), releaseTime=float('inf'), dueDate=-1, weight=-1):
        
        # read-only attributes. They are the same for every schedule
        self.id = id
        """ Identifier of the job """

        self.processingTime = processingTime
        """Time needed for a job to complete"""
        
        self.releaseTime = releaseTime
        """ a job cannot be scheduled before its release time """

        self.dueDate = dueDate
        """ a job should be completed before its due date (it depends on the problem nature) """

        self.weight = weight
        """ Multiplied with completion times to get the cost of each job """

        # dynamic attributes. They may change among each schedule
        self.startingTimes = []
        """ times when job processing has started. Since preemtion exists, there can be multiple starting times """
                
        self.remainingTime = processingTime
        """ Time left for a job to complete. A zero value means that the job is completed. """
        
        self.completionTime = None
        """ time when the job has completed """

class SPTFRuleSolver(Solver):
    """ A solver that uses Shortest Processing Time First (SPTF) rule to solve a preemptive Single Machine Problem.
    """

    def __call__(self, smsProblem):
        
        time = 0        # current time
        shortestJob = Job() # job with the lowest remaining time among released ones
        completed = 0   # number of completed jobs
        
        # time will start from the first time slot next to latest completion time (useful when the schedule is already partially calculated)
        for job in smsProblem.jobs:
            if job.remainingTime == 0 and job.completionTime > time:
                time = job.completionTime + 1
                completed += 1  # we note that some jobs are already completed
        
        while completed < len(smsProblem.jobs):
            
            nextReleaseTime = float('inf') # earliest release time after current time
            for job in smsProblem.jobs:
                  
                # finds nearest release time among unreleased jobs
                if job.releaseTime > time and job.releaseTime < nextReleaseTime:
                    nextReleaseTime = job.releaseTime
                
                # finds the not completed released job with the shortest remaining time
                if job.releaseTime <= time and (shortestJob.remainingTime == 0 or job.remainingTime < shortestJob.remainingTime) and job.remainingTime > 0:
                    shortestJob = job
                
            if shortestJob != None:
                
                # add the job to the schedule
                shortestJob.startingTimes.append(time)
                
                # time progresses until the job is completed or a new job is released
                progress = min(shortestJob.remainingTime, nextReleaseTime - time)
                shortestJob.remainingTime -= progress if progress <= shortestJob.remainingTime else shortestJob.remainingTime   # remaining time must be at least 0
                if shortestJob.remainingTime == 0:
                    shortestJob.completionTime = time + progress
                    completed += 1
            else:
                
                # no job is released, time progresses until the next release time
                progress = nextReleaseTime - time
            
            time += progress

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