import traceback

from BoolNet.BoolNetwork import *

class BoolNetwork_Expanded_Huristic(BoolNetwork):
    def __init__(self):
        super().__init__()



    def eval_regulation_conditions(self):  # this method synthesizes the reg conditions to nuXmv
        arr = self.experiments[0][0][1]  # -change it-
        h = len(self.experiments)
        for i in self.components.values():
            i.find_reg_indices()
            for k in range(len(self.experiments)):
                self.regConds[f"{i.name}{k}"] = self.eval_bool_expression(i,k)


    # def trueOrFalse(self, exp):
    #     true_counter = exp.count("TRUE")
    #     edge_counter = len(exp.replace(" ","").split("|"))
    #     if true_counter==edge_counter:

        # ((edge_b_d_positive ? b1:False)  | (edge_c_d_positive ? c1:TRUE) & a0)



    def eval_bool_expression(self, i,k):

        eval_dict = {}
        for comp,j in i.sources.items():
            eval_dict[j[1]+"#"+j[0]] = eval_dict.get(j[1]+"#"+j[0],"")+comp+str(k)+" "


        exp_arr  = []
        exp = ""
        expressions =[]
        #[[('E#strong#A | E#weak#A', 'E#weak#R')], [('E#strong#A | E#weak#A', 'E#weak#R')],[('E#strong#A | A#weak#A', 'A#weak#R')]]
        for idx in i.regIndices:   #idx = [('E#strong#A | E#weak#A', 'E#weak#R')]
            exp=""
            #  n e a | e e a
            # E E E
            # E N N | n e n |
            #  n n n -> e | e | e
            for reg_cond in idx: #reg_cond= ('E#strong#A | E#weak#A', 'E#weak#R')
                # exp = ""
                # exp+="("##########################################################################################################################
                reg_lsts = [reg_cond[0].split("|"), reg_cond[1].split("|")]
                temp = ""
                try:
                    reg_lsts.remove(['None'])
                except:
                    pass
                for lst in reg_lsts: #lst = ['E#strong#A ', ' A#weak#A']
                    exp += "("  ##########################################################################################################################

                    for reg in lst: #reg
                        reg_lst = reg.split("&")


                        # reg_lst=reg_cond[0].split("&")+reg_cond[1].split("&")
                        # c= all activators and exist repressors
                        # not all repressors
                        try:
                            reg_lst.remove('None')
                        except:
                            pass
                        for it in reg_lst:
                            it = it.strip().split("#")
                            if it[2]=='A':
                                try:
                                    if not it[0] =="N":
                                        exp+="("+self.build_expression(it[0],eval_dict[it[1]+"#positive"].strip().split(" "),i,k, 1)+")"+"&"
                                except Exception as e:
                                    traceback.print_exc()
                            elif it[2]=='R':
                                try:
                                    exp+="("+self.build_expression(it[0],eval_dict[it[1]+"#negative"].strip().split(" "),i,k, 0)+")"+"&"
                                except Exception as e:
                                    traceback.print_exc()
                        exp=exp[:-1]
                        exp = exp + " | "

                    # exp = exp[:-1]
                    # exp = exp + ") | "
                    exp=exp[:-3]
                    exp=exp+") & "
            exp = exp[:-3]
            exp = exp+") | "

            exp = exp[:-4]
            exp=exp.replace("&))","")
            exp=exp.replace("&)",")")
            expressions.append(exp)
            # exp=exp[:-1]+")|"
    #     exp=exp[:-3]
    #
    #     #exp_arr.append(exp[:-1])
    # #return exp_arr
    #     expressions.append(exp)##########################################################################################################################

        return expressions
    #def eval_bool_expression1(self, i,k):
        # print(f"dffdafdafdsfdas{i.regIndices}")
        # print(f"dffdafdafdsfdas{i.sources}")
        # eval_dict = {}
        # for comp,j in i.sources.items():
        #     eval_dict[j[1]+"#"+j[0]] = eval_dict.get(j[1]+"#"+j[0],"")+comp+str(k)+" "
        #
        #
        # print(f"eval_dict={eval_dict}")
        # exp_arr  = []
        # exp = ""
        # expressions =[]
        # for idx in i.regIndices:   #regIndices = [[('N#strong#A & N#strong2#A & N#weak#A', 'N#k#R')| ('N#strong#A & N#strong2#A & E#weak#A', 'A#k#R')], [('N#strong#A & N#strong2#A & N#weak#A', 'E#k#R'), ('N#strong#A & N#strong2#A & E#weak#A', 'A#k#R')]]
        #     exp=""
        #     for reg_cond in idx:
        #         # exp = ""
        #         exp+="("##########################################################################################################################
        #         reg_lst=reg_cond[0].split("&")+reg_cond[1].split("&")
        #         try:
        #             reg_lst.remove('None')
        #         except:
        #             pass
        #         print(f"x and y {reg_lst}")
        #         for it in reg_lst:
        #             it = it.strip().split("#")
        #             print(f"itit {it}")
        #             if it[2]=='A':
        #                 try:
        #                     if not it[0] =="N":
        #                         exp+="("+self.build_expression(it[0],eval_dict[it[1]+"#positive"].strip().split(" "),i,k, 1)+")"+"&"
        #                 except Exception as e:
        #                     traceback.print_exc()
        #             elif it[2]=='R':
        #                 try:
        #                     exp+="("+self.build_expression(it[0],eval_dict[it[1]+"#negative"].strip().split(" "),i,k, 0)+")"+"&"
        #                 except Exception as e:
        #                     traceback.print_exc()
        #             print(f"it111 {it}")
        #
        #         exp = exp[:-1]
        #         exp = exp+") | "
        #         print(f'expppppp {exp[:-1]}')
        #         # exp=exp[:-1]+")|"
        #     exp=exp[:-3]
        #
        #     #exp_arr.append(exp[:-1])
        # #return exp_arr
        #     expressions.append(exp)##########################################################################################################################
        # print(expressions)
        #
        # return expressions


    #remmember to add negative for Repressors
    def build_expression (self,key,components,node,k,PosNeg):
        ret = ""
        expr = "TRUE" if PosNeg else "FALSE"
        exclamation  = "" if PosNeg else "!"
        opts = node.opt_sources
        print(f"key = {key}, components = {components}, node = {node.sources}, {node.regIndices},{node.name}, k = {k}")
        print(f"opts={opts}")
        ret += f"({exclamation}("

        if key =='A' :
            for i in components:
                i = i[:-1]
                if i in opts: ##########################################################################################################################
                    flag = node.sources[i][0]
                    #ret+=f"{exclamation}(edge_{i}_{node.name}_{flag} ? {i}{k}:TRUE) &"##########################################################################################################################
                    ret+=f"(edge_{i}_{node.name}_{flag} ? {i}{k}:TRUE) &"##########################################################################################################################
                else:
                    ret+=i+str(k)+" &"
        elif key=="N":
            return ""
            # for i in components:
            #     i = i[:-1]
            #     if i in opts:
            #         flag = node.sources[i][0]
            #         ret+=f"!(edge_{i}_{node.name}_{flag} ? {i}{k}:FALSE) &"##########################################################################################################################
            #     else:
            #         ret+="!"+i+str(k)+" &"
        else: #exist
            for i in components:
                i = i[:-1] #remove 0 from A0
                if i in opts:
                    flag = node.sources[i][0]
                    #ret+=f"(edge_{i}_{node.name}_{flag} ? {i}{k}:FALSE) |"##########################################################################################################################
                    ret+=f"(edge_{i}_{node.name}_{flag} ? {i}{k}:FALSE) |"##########################################################################################################################
                else:
                    ret += i+str(k) + "|"
            # ret=ret[:-1]
            # ##########################################################################################################################
            # print(f"{ret.count("FALSE")} ITTT")
            # # if ret.count("FALSE")==1:
            # #     ret=ret.replace("FALSE","TRUE")
            # if ret.count("FALSE") == len(components): #only optionals in ret
            #     ret+="&("
            #     for i in opts:
            #         flag = node.sources[i][0]
            #         ret+=f"!edge_{i}_{node.name}_{flag} & "
            #     ret = ret[:-3]
            #     ret+="?TRUE:FALSE)"
            ##########################################################################################################################
        ret=ret[:-1]
        ret += "))"

        return ret




    def add_interaction(self, l):
        # if l[-1]!='True':##########################################################################################################################
        #     l.append('False')
        self.components[l[1]].add_source(l[0],l[2],l[3],l[4]) #add the interactions
        if l[-1]=='True': ##########################################################################################################################
            self.possible_interactions.append((l[0],l[1],l[2],l[3]))
        else:
            self.definite_interactions.append((l[0],l[1],l[2],l[3]))

    def add_perm(self):
        definite_interactions = self.perm_interactions[-1]


        self.eval_regulation_conditions()  # create the regulation conditions for current permutation

        return definite_interactions










#
#
# import traceback
#
# from BoolNetwork import *
#
# class BoolNetwork_Expanded_Huristic(BoolNetwork):
#     def __init__(self):
#         super().__init__()
#         print("here111")
#
#
#
#     def eval_regulation_conditions(self):  # this method synthesizes the reg conditions to nuXmv
#         arr = self.experiments[0][0][1]  # -change it-
#         h = len(self.experiments)
#         for i in self.components.values():
#             print(f"{i.name}")
#             i.find_reg_indices()
#             for k in range(len(self.experiments)):
#                 self.regConds[f"{i.name}{k}"] = self.eval_bool_expression(i,k)
#
#
#     def eval_bool_expression(self, i,k):
#         print(f"dffdafdafdsfdas{i.regIndices}")
#         print(f"dffdafdafdsfdas{i.sources}")
#         eval_dict = {}
#         for comp,j in i.sources.items():
#             eval_dict[j[1]+"#"+j[0]] = eval_dict.get(j[1]+"#"+j[0],"")+comp+str(k)+" "
#
#
#         print(f"eval_dict={eval_dict}")
#         exp_arr  = []
#         exp = ""
#         expressions =[]
#         for idx in i.regIndices:   #regIndices = [[('N#strong#A & N#strong2#A & N#weak#A', 'N#k#R')| ('N#strong#A & N#strong2#A & E#weak#A', 'A#k#R')], [('N#strong#A & N#strong2#A & N#weak#A', 'E#k#R'), ('N#strong#A & N#strong2#A & E#weak#A', 'A#k#R')]]
#             exp=""
#             for reg_cond in idx:
#                 # exp = ""
#                 exp+="("##########################################################################################################################
#                 reg_lst=reg_cond[0].split("&")+reg_cond[1].split("&")
#                 try:
#                     reg_lst.remove('None')
#                 except:
#                     pass
#                 print(f"x and y {reg_lst}")
#                 for it in reg_lst:
#                     it = it.strip().split("#")
#                     print(f"{it}")
#                     if it[2]=='A':
#                         try:
#                             if not it[0] =="N":
#                                 exp+="("+self.build_expression(it[0],eval_dict[it[1]+"#positive"].strip().split(" "),i,k, 1)+")"+"&"
#                         except Exception as e:
#                             traceback.print_exc()
#                     elif it[2]=='R':
#                         try:
#                             exp+="("+self.build_expression(it[0],eval_dict[it[1]+"#negative"].strip().split(" "),i,k, 0)+")"+"&"
#                         except Exception as e:
#                             traceback.print_exc()
#                 exp = exp[:-1]
#                 exp = exp+") | "
#                 print(f'expppppp {exp[:-1]}')
#                 # exp=exp[:-1]+")|"
#             exp=exp[:-3]
#
#             #exp_arr.append(exp[:-1])
#         #return exp_arr
#             expressions.append(exp)##########################################################################################################################
#         print(expressions)
#
#         return expressions
#
#
#     #remmember to add negative for Repressors
#     def build_expression (self,key,components,node,k,PosNeg):
#         ret = ""
#         expr = "TRUE" if PosNeg else "FALSE"
#         exclemation  = "" if PosNeg else "!"
#
#         opts = node.opt_sources
#         print(f"key = {key}, components = {components}, node = {node.sources}, {node.regIndices},{node.name}, k = {k}")
#         print(f"opts={opts}")
#         if key =='A' :
#             for i in components:
#                 i = i[:-1]
#                 if i in opts: ##########################################################################################################################
#                     flag = node.sources[i][0]
#                     ret+=f"(edge_{i}_{node.name}_{flag} ? {i}{k}:TRUE) &"##########################################################################################################################
#                 else:
#                     ret+=i+str(k)+" &"
#         elif key=="N":
#             return ""
#             # for i in components:
#             #     i = i[:-1]
#             #     if i in opts:
#             #         flag = node.sources[i][0]
#             #         ret+=f"!(edge_{i}_{node.name}_{flag} ? {i}{k}:FALSE) &"##########################################################################################################################
#             #     else:
#             #         ret+="!"+i+str(k)+" &"
#         else: #exist
#             for i in components:
#                 i = i[:-1] #remove 0 from A0
#                 if i in opts:
#                     flag = node.sources[i][0]
#                     ret+=f"(edge_{i}_{node.name}_{flag} ? {i}{k}:FALSE) |"##########################################################################################################################
#                 else:
#                     ret += i+str(k) + "|"
#         print(f"ret {ret}")
#         return ret[:-1]
#
#
#
#
#     def add_interaction(self, l):
#         # if l[-1]!='True':##########################################################################################################################
#         #     l.append('False')
#         self.components[l[1]].add_source(l[0],l[2],l[3],l[4]) #add the interactions
#         print(f"llllllll {l}")
#         if l[-1]=='True': ##########################################################################################################################
#             print(l[3])
#             self.possible_interactions.append((l[0],l[1],l[2],l[3]))
#         else:
#             self.definite_interactions.append((l[0],l[1],l[2],l[3]))
#
#     def add_perm(self):
#         print(f"opt1 {self.possible_interactions}")
#         definite_interactions = self.perm_interactions[-1]
#         # for i in definite_interactions:  # add the new interactions of the new permutation
#         #     self.components[i[1]].add_source(i[0], i[2], i[3], True)
#         for i in self.components.values():
#             #     if i.sources == {}:####if no activators then add yourself as one.
#             #         i.sources = {i.name: ("positive", False)}
#             print(f"{i.name}: {i.sources}")
#         self.eval_regulation_conditions()  # create the regulation conditions for current permutation
#         print(f"opt2 {self.possible_interactions}")
#
#         return definite_interactions








