from copy import deepcopy
from logic.problem import Solver
from logic.sms.entities import Job

class SPTFRuleSolver(Solver):
    """ A solver that uses Shortest Processing Time First (SPTF) rule to solve a preemptive Single Machine Problem.
    """

    def __call__(self, smsProblem):
        
        time = 0        # current time
        shortestJob = Job() # job with the lowest remaining time among released ones
        completed = 0   # number of completed jobs
        
        # time will start from the first time slot next to latest completion time (useful when the schedule is already partially calculated)
        for job in smsProblem.vars:
            if job.remainingTime == 0 and job.completionTime > time:
                time = job.completionTime + 1
                completed += 1  # we note that some jobs are already completed
        
        while completed < len(smsProblem.vars):
            
            nextReleaseTime = float('inf') # earliest release time after current time
            for job in smsProblem.vars:
                  
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
