from logic.problem import Objective
from logic.sms import *

class WeightedCompletionsSum(Objective):

    def __call__(self, smsProblem):

        weightedCompletions = []
        for j in smsProblem.vars:
            weightedCompletions.append(j.weight * j.completionTime)
        return sum(weightedCompletions)

class CompletionsSum(Objective):

    def __call__(self, smsProblem):

        completions = []
        for j in smsProblem.vars:
            completions.append(j.completionTime)
        return sum(completions)