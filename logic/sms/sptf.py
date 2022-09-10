from logic.problem import Solver
from logic.sms.entities import Job, Machine

class SPTFRuleScheduler(Solver):
    """ A solver that uses Shortest Processing Time First (SPTF) rule to solve a preemptive Single Machine Problem.
    """

    def __call__(self, smsProblem):
                
        shortestJob = Job() # job with the lowest remaining time among released ones
        while smsProblem.machine.completed < len(smsProblem.vars):
            
            nextReleaseTime = float('inf') # earliest release time after current time
            for job in smsProblem.vars:
                  
                # finds nearest release time among unreleased jobs
                if job.releaseTime > smsProblem.machine.currentTime and job.releaseTime < nextReleaseTime:
                    nextReleaseTime = job.releaseTime
                
                # finds the not completed released job with the shortest remaining time
                if job.releaseTime <= smsProblem.machine.currentTime and (shortestJob.remainingTime == 0 or job.remainingTime < shortestJob.remainingTime) and job.remainingTime > 0:
                    shortestJob = job
                
            if shortestJob.remainingTime != 0:
                
                # add the job to the schedule if not already scheduled
                if smsProblem.machine.currentlyScheduled is None or shortestJob.id != smsProblem.machine.currentlyScheduled.id:

                    shortestJob.startingTimes.append(smsProblem.machine.currentTime)
                    smsProblem.machine.currentlyScheduled = shortestJob
                
                # time progresses until the job is completed or a new job is released
                progress = min(shortestJob.remainingTime, nextReleaseTime - smsProblem.machine.currentTime)
                shortestJob.remainingTime -= progress if progress <= shortestJob.remainingTime else shortestJob.remainingTime   # remaining time must be at least 0
                if shortestJob.remainingTime == 0:
                    shortestJob.completionTime = smsProblem.machine.currentTime + progress - 1
                    smsProblem.machine.completed += 1
            else:
                
                # no job is released, time progresses until the next release time
                progress = nextReleaseTime - smsProblem.machine.currentTime
            
            smsProblem.machine.currentTime += progress
