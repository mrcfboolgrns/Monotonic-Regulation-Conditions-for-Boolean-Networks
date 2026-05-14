from Regulation import *


class Node: #used to identify the connections and their effect (positive/negative)
    def __init__(self, name, regulation=None):
        self.regIndices = None
        if regulation is None:
            regulation = [0]
        self.name = name
        self.sources = {} #the sources of the Node
        # self.optional_activators=[]
        # self.optional_repressors=[]
        # self.definite_repressors=[]
        # self.definite_activators=[]
        self.def_sources=[]
        self.opt_sources=[]
        self.regulation = regulation

    def reset(self):
        self.sources = {}

    def add_source(self, source, effect,group=None, optional='False'): #adding source to the node (optional='False' definite)
        if not group:
            self.sources[source] = (effect, optional)
        else:
            self.sources[source] = (effect, group, optional)
        if optional=='False':
            self.def_sources.append(source)
        else:
            self.opt_sources.append(source)


    def find_reg_indices(self):
        if self.regIndices is not None:
            return
        arrn = set()
        arrm = set()
        for i in self.sources.values():

            if i[0] == 'positive':
                arrn |= {i[1]}
            else:
                arrm |= {i[1]}
        self.regIndices = startmatrix(arrn, arrm)

        # if effect=="positive" and optional=='True':
        #     self.optional_activators.append(source)
        # elif effect=="negative" and optional=='True':
        #     self.optional_repressors.append(source)
        # elif effect == "negative" and optional == 'False':
        #     self.definite_repressors.append(source)
        # else:
        #     self.definite_activators.append(source)

    def change_regulation(self, regulation):
        self.regulation = regulation



    def printall(self):
        print(f"{self.name}'s sources are {self.sources}, and the regulations are {self.regulation}")
        # print(f"definite activators: {self.definite_activators}, optional activators: {self.optional_activators}, definite repressors: {self.definite_repressors}, optional repressors: {self.optional_repressors}")