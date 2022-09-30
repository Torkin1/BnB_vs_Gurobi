"""
A Single Machine Scheduling problem implementation with solvers and other tools
"""
from logic.problem import Problem
from copy import deepcopy

class SingleMachineScheduling(Problem):
    """
    Single Machine Scheduling Problem.
    """

    def __init__(self, jobs, machine):
        """
        @param jobs: a list of jobs to be scheduled
        """
        super().__init__()
        self.vars = jobs
        self.machine = machine

class Machine:
    """ jobs are scheduled to be processed on a machine """

    def __init__(self, id=-1):

        # read-only attributes
        self.id = id
        """ id of the machine """
        
        # dynamic attributes, can be used by schedulers to update the machine state
        self.currentlyScheduled = None
        """ a pointer to the currently scheduled job """
        self.currentTime = 0
        """ current time on the machine """
        self.completed = 0
        """ number of completed jobs """

class Job:
    """
    A job that can be scheduled on a single machine
    """

    def __init__(self, id=-1, processingTime=0, releaseTime=float('inf'), dueDate=float("inf"), weight=1):
        
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

        # dynamic attributes. They may change among each schedule and are updated by schedulers
        self.startingTimes = []
        """ times when job processing has started. Since preemption exists, there can be multiple starting times """
        self.remainingTime = processingTime
        """ Time left for a job to complete. A zero value means that the job is completed. """
        self.completionTime = None
        """ time when the job has completed """

