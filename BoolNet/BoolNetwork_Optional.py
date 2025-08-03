from warnings import resetwarnings


from BoolNet.BoolNetwork import *

class BoolNetwork_Optional(BoolNetwork):
    def __init__(self):
        super().__init__()

    def eval_regulation_conditions_optional(self): #this method synthesizes the reg conditions to nuXmv
        arr=self.experiments[0][0][1] #-change it-
        h= len(self.experiments)
        # (red,black,positive,optional),(red,green,positive,optional)
        all_possible_interactions= self.possible_interactions
        possible_idx = set((i,x[1]) for i,x in enumerate(all_possible_interactions))
        for i in self.components.values():

            for k in range(h):
                self.regConds[i.name+str(k)]=RegulationConditions(i,arr).eval_dict(k) #create a dictionary for name with all regulation conditions



