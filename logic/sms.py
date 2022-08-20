from logic.problem import *

class WeightedCompletionsSum(Target):

    def __call__(self, smsProblem):

        weightedCompletions = []
        for j in smsProblem.jobs:
            weightedCompletions.append(j.weight * j.completionTime)
        return sum(weightedCompletions)

class SPTFfRuleSolver(Solver):
    """ A solver that uses Shortest Processing Time First (SPTF) rule to solve a preemptive Single Machine Problem.
    """

    def __call__(self, smsProblem, startingTime=0):
        
        time = startingTime        # current time
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

