from BoolNet.BoolNetwork import *

class BoolNetwork_Expanded(BoolNetwork):
    def __init__(self):
        super().__init__()
        self.perm_index=0



    def eval_regulation_conditions(self):  # this method synthesizes the reg conditions to nuXmv
        arr = self.experiments[0][0][1]  # -change it-
        h = len(self.experiments)
        for i in self.components.values():
            i.find_reg_indices()
            for k in range(len(self.experiments)):
                self.regConds[f"{i.name}{k}"] = self.eval_bool_expression(i,k)


    def eval_bool_expression(self, i,k):

        eval_dict = {}
        for comp,j in i.sources.items():
            eval_dict[j[1]+"#"+j[0]] = eval_dict.get(j[1]+"#"+j[0],"")+comp+str(k)+" "
        exp_arr  = []
        exp = ""
        expressions =[]
        for idx in i.regIndices:
            for reg_cond in idx:
                exp+="("
                reg_lst=reg_cond[0].split("&")+reg_cond[1].split("&")
                try:
                    reg_lst.remove('None')
                except:
                    pass
                for it in reg_lst:
                    it = it.strip().split("#")
                    if it[2]=='A':
                        try:
                            exp+="("+self.build_expression(it[0],eval_dict[it[1]+"#positive"].strip().split(" "))+")"+"&"
                        except:
                            pass
                    elif it[2]=='R':
                        try:
                            exp+="("+self.build_expression(it[0],eval_dict[it[1]+"#negative"].strip().split(" "))+")"+"&"
                        except:
                            pass
                exp=exp[:-1]+")|"

            #exp_arr.append(exp[:-1])
        #return exp_arr
            expressions.append(exp[:-1])
        return expressions

    def build_expression (self,key,components):
        ret = ""
        if key =='A' :
            for i in components:
                ret+=i+" &"
        elif key=="N":
            for i in components:
                ret+="!"+i+" &"
        else:
            for i in components:
                ret+=i+" |"
        return ret[:-1]


    def add_interaction(self, l):
        if l[-1]!='optional':
            l.append('definite')
        self.components[l[1]].add_source(l[0],l[2],l[3],l[4]) #add the interactions
        if l[-1]=='optional':
            self.possible_interactions.append((l[0],l[1],l[2],l[3]))
        else:
            self.definite_interactions.append((l[0],l[1],l[2],l[3]))

    def add_perm(self):
        definite_interactions = self.perm_interactions[self.perm_index]
        for i in self.components.values():
            i.reset()  # reset regulation condition because now some connections are present/not present, the network has changed
        for i in definite_interactions:  # add the new interactions of the new permutation
            self.components[i[1]].add_source(i[0], i[2], i[3], True)


        self.eval_regulation_conditions()  # create the regulation conditions for current permutation
        self.perm_index -= 1  # move to next permutation
        return definite_interactions






