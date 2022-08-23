"""
A Single Machine Scheduling problem implementation with solvers and other tools
"""
from logic.problem import *
from copy import deepcopy

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

