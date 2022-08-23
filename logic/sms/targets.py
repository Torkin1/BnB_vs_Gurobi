from logic.problem import Target
from logic.sms import *

class WeightedCompletionsSum(Target):

    def __call__(self, smsProblem):

        weightedCompletions = []
        for j in smsProblem.jobs:
            weightedCompletions.append(j.weight * j.completionTime)
        return sum(weightedCompletions)

