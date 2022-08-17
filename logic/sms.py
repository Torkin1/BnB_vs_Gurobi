from problem import *

class WeightedCompletionsSum(Target):

    def __call__(self, smsProblem):

        weightedCompletions = []
        for j in smsProblem.jobs:
            weightedCompletions.append(j.weight * j.completionTime)
        return sum(weightedCompletions)

class SPTFfRuleSolver(Solver):
    """ A solver that uses Shortest Processing Time First (SPTF) rule to solve a preemptive Single Machine Problem.
    """

    def solve(self, smsProblem):
        schedule = []   # ordered list of job id
        time = 0        # current time
        shortestJob = Job() # job with the lowest remaining time among released ones
        completed = 0   # number of completed jobs
        
        while completed < len(smsProblem.jobs):
            
            nextReleaseTime = float('inf') # earliest release time after current time
            
            for job in smsProblem.jobs:
                  
                # finds nearest release time among unreleased jobs
                if job.releaseTime > time and job.releaseTime < nextReleaseTime:
                    nextReleaseTime = job.releaseTime
                
                # find the not completed released job with the shortest remaining time
                if job.releaseTime <= time and (shortestJob.remainingTime == 0 or job.remainingTime < shortestJob.remainingTime) and job.remainingTime > 0:
                    shortestJob = job
            
            if shortestJob != None:
                
                # add the job to the schedule
                schedule.append((shortestJob.id, time))
                
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

        return schedule


class SingleMachineScheduling(Problem):
    """
    Single Machine Scheduling Problem represented using time indexing
    """
    
    jobs = [] 
    """
    Jobs to schedule on a single machine
    """

    completions = []

class SMS_timeIndexed(SingleMachineScheduling):
    """
    Single Machine Scheduling Problem represented using time indexing variables
    """

    def __init__(self, jobs):
        
        # initialize time indexed sparse matrix, with jobs as rows and time as columns.
        self.jobs = jobs
        self.vars["x"] = []
        for j in self.jobs:
            self.vars["x"].append([])
    
    def solve(self):
        
        # calculate schedule
        schedule = self.solver.solve(self)
        
        # populate vars according to schedule
        for j in schedule:
            self.vars["x"][j[0]].append(j[1])

        # update value of target function
        self.value = self.target(self)

class Job:
    """
    A job that can be scheduled on a single machine
    """

    id = None
    """ Identifier of the job """
    
    processingTime = None
    """
    Time needed for a job to complete
    """
    
    releaseTime = None
    """
    a job cannot be scheduled before its release time
    """

    dueDate = None
    """
    a job should be completed before its due date (it depends on the problem nature)
    """

    weight = None
    """
    Multiplied with completion times to get the cost of each job
    """

    # dynamic attributes. They can change at runtime
    
    remainingTime = processingTime
    """
    Time left for a job to complete. A zero value means that the job is completed.
    """
    
    completionTime = None
    """ time when the job has completed """

    def __init__(self, id=-1, processingTime=float('inf'), releaseTime=float('inf'), dueDate=-1, weight=-1):
        self.id = id
        self.processingTime = processingTime
        self.remainingTime = processingTime
        self.releaseTime = releaseTime
        self.dueDate = dueDate
        self.weight = weight
    
