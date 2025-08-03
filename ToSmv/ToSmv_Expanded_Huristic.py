import re



from  ToSmv.ToSmv_Improved_Optional import *
class ToSmv_Expanded_Huristic(ToSmv_Improved_Optional):
    def __init__(self,BoolNetwork_Expanded_Huristic):
        super().__init__(BoolNetwork_Expanded_Huristic)




    def all_combined(self):
        permutations_h= open('test.txt', 'w')
        l = self.BoolNet.add_perm()
        res = self.python_to_nuxmv()
        def_int = [(i[0],i[1],i[2]) for i in self.BoolNet.definite_interactions]
        for result in self.result:
            res_int = def_int.copy()

            for edge in result:
                if edge[-1]=="1":
                    continue
                edge_parts = edge.split("_")
                res_int.append((edge_parts[2],edge_parts[3],edge_parts[4][:-4]))
            permutations_h.write(str(res_int)+"\n")
        permutations_h.close()

        if len(self.solutions) != 0: #if we have solutions then create a solution matrix
            print(self.BoolNet.possible_interactions+self.BoolNet.definite_interactions)
            disp_viable_models.txt_to_mat(self.BoolNet.possible_interactions+self.BoolNet.definite_interactions)

        disp_viable_models.disp_experiments(self.BoolNet.experiments)



    def python_to_nuxmv(self): #from python to an smv file
        filename = "model_optional.smv"

        n=len(self.BoolNet.experiments)
        dict1=self.BoolNet.regConds
        #self.experimentNumber=(self.experimentNumber+1)%len(self.BoolNet.experiments)
        definite_edges = self.BoolNet.definite_interactions
        optional_edges = self.BoolNet.possible_interactions


        targets = []

        for edge in definite_edges:
            targets.append(edge[1])
        add_fate = self.BoolNet.components.keys() - targets

        fate_dict={}


        with (open(filename, "w") as f):
            str1 =""
            str1+="MODULE main\n"+"VAR\n" #add first lines required
            # f.write("MODULE main\n")
            # f.write("VAR\n")
            # f.write(str1)
            for i in range(n):
                for var in self.BoolNet.components: #add all components as boolean
                    str1+=f"    {var}{i} : boolean;\n"
                    #str1+=f"    choice_{var}{i} :{set(self.BoolNet.components[var].regulation)};\n"
                    # setD=set(range(len(dict1[f"{var}{i}"])))
                    # if setD!=set():
                    #     str1+=f"    choice_{var}{i} :{set(range(len(dict1[f"{var}{i}"])))};\n"   ######

                    # f.write(f"    {var}{i} : boolean;\n")
                for var in add_fate:
                    #str1 += f"    fate_{var}{i} : boolean;\n"
                    fate_dict[f"{var}{i}"]=[]

                str1+=f"    time{i}: 0..{self.BoolNet.experiments[i][1][0]};\n" #for each of them add the time for their experiment
                # f.write(f"    time{i}: 0..{self.BoolNet.experiments[i][1][0]};\n")
            for var in self.BoolNet.components:
                setD = set(range(len(dict1[f"{var}{i}"])))
                if setD != set():
                    str1 += f"    choice_{var} :{set(range(len(dict1[f"{var}0"])))};\n"######
            for opt in optional_edges:

                str1 += f"    edge_{opt[0]}_{opt[1]}_{opt[2]} : boolean;\n"
                #str1 += f"    edge_{opt[0]}_{opt[1]} : boolean;\n"
                ##########################################################################################################################
                # str1+=  f"    choice_edge_exp{i}_{opt[0]}{i}_{opt[1]}{i}_{opt[2]} : {{0,1}};\n"
                str1+=  f"    choice_edge_{opt[0]}_{opt[1]}_{opt[2]} : {{0,1}};\n"
                # if opt[1] in add_fate:
                #     fate_dict[f"{opt[1]}"].append(f'choice_edge_{opt[0]}_{opt[1]}_{opt[2]}')
                    # fate_dict[f"{opt[1]}{i}"].append(f'choice_edge_exp{i}_{opt[0]}{i}_{opt[1]}{i}_{opt[2]}')


            str1+=f"\nINIT\n"+"    "
            # f.write(f"\nINIT\n")
            # f.write("    ")
            s=""
            j=0
            for exp in self.BoolNet.experiments:
                for var in exp[0][1].keys():
                    # print(f"ppppp {var}")
                    s+=f"({var}{j} = {str(bool(int(exp[0][1][var]))).upper()})&" #for each experiment initialize the variables with 0=FALSE,1=TRUE
                # s += f"({i}{j} = {str(bool(int(exp[0])).upper()})&"
                # print(f"dfsam,df;saml;fdkasnmdfas{exp}")
                # print(f"dsafdasfgdasadfgsafgdsagfsdagfsdagfsdgafsdafdgsdfsam,df;saml;fdkasnmdfas{exp[0]}")
                s += f"(time{j} = 0) & " #init each time to 0    ##########################################################################################################################
                j += 1
            for opt in optional_edges:
                s+=f"(edge_{opt[0]}_{opt[1]}_{opt[2]} = (choice_edge_{opt[0]}_{opt[1]}_{opt[2]} = 0 ? TRUE : FALSE)) & "
                #s+=f"(edge_{opt[0]}_{opt[1]} = (choice_edge_{opt[0]}_{opt[1]}_{opt[2]} = 0 ? TRUE : FALSE)) & "
                ##########################################################################################################################
                # s+=f"(edge_{opt[0]}{i}_{opt[1]}{i}_{opt[2]} = (choice_edge_exp{i}_{opt[0]}{i}_{opt[1]}{i}_{opt[2]} = 0 ? TRUE : FALSE)) & "


            # str1 += f"(time{j} = 0)&"
            str1 += s[:-3] + ";" #remove last & char from the file
            # print(f"dddddd {s}")

            # for j in range(n):
            #     exp = self.BoolNet.experiments[j]
            #     print(exp)
            #     for i in exp[j][1].keys():
            #         s+= f"({i}{j} = {str(bool(int(exp[j][1][i]))).upper()})&"
            #         print(s)
            #         # str1 += f"({i}{j} = {str(bool(int(exp[j][1][i]))).upper()})&"
            #
            #     s+= f"(time{j} = 0)&"
            #     # str1 += f"(time{j} = 0)&"
            # str1+=s[:-1]+";"
            # f.write(s[:-1]+";")
            str1+="\nDEFINE\n"
            # f.write("\nDEFINE\n")

            for exp in self.BoolNet.experiments:
                str1+=f"    Experiment{self.experimentNumber} :=" #write the experiment + its number
                # f.write(f"    Experiment{self.experimentNumber} :=")
                keys = list(exp[1][1].keys()) #get the values of the components
                for index, i in enumerate(keys):
                    if index == len(keys) - 1: #for last component in exp
                        str1+=f"({i}{self.experimentNumber} = {str(bool(int(exp[1][1][i]))).upper()});" #write the a(exp_num)=TRUE, etc
                        # f.write(f"({i}{self.experimentNumber} = {str(bool(int(exp[1][1][i]))).upper()});")
                    else:
                        str1+=f"({i}{self.experimentNumber} = {str(bool(int(exp[1][1][i]))).upper()})&"
                        # f.write(f"({i}{self.experimentNumber} = {str(bool(int(exp[1][1][i]))).upper()})&")
                str1+="\n"
                self.experimentNumber += 1
            self.experimentNumber = 0

            # f.write("\nASSIGN\n")
            str1+="\nASSIGN\n"

            # for fate in fate_dict.keys():
            #     str1 += f"    next(fate_{fate}) := case\n"
            #     str1 += f"           "
            #     for reg in fate_dict[fate]:
            #         str1 += f"{reg} = 1 & "
            #
            #     str1 = str1[:-3] +f":{fate};\n"
            #
            #
            #     str1+="           TRUE:TRUE;\n"
            #     str1+="    esac;\n"

            # reg = self.reglist[regidx]  ####################change back
            # print(reg)
            str2=""

            for opt in optional_edges:
                str1 += f"    next(choice_edge_{opt[0]}_{opt[1]}_{opt[2]}) := choice_edge_{opt[0]}_{opt[1]}_{opt[2]};\n"
                str1 += f"    next(edge_{opt[0]}_{opt[1]}_{opt[2]}) := edge_{opt[0]}_{opt[1]}_{opt[2]};\n"
                #str1 += f"    next(edge_{opt[0]}_{opt[1]}) := edge_{opt[0]}_{opt[1]};\n"
                ##########################################################################################################################


                    # str1 += f"    next(edge_{opt[0]}{k}_{opt[1]}{k}_{opt[2]}) := case\n"
                    # str1 += f"       choice_edge_exp_{opt[0]}{k}_{opt[1]}{k}_{opt[2]} = 0 :TRUE;\n"
                    # str1 += f"       choice_edge_exp_{opt[0]}{k}_{opt[1]}{k}_{opt[2]} = 1 :FALSE;\n"
                    # str1 += f"       TRUE:edge_{opt[0]}{k}_{opt[1]}{k}_{opt[2]};\n"
                    # str1 += f"    esac;\n"

            for k in range(n):

                str1+=f"    next(time{k}) := (time{k} < {self.BoolNet.experiments[k][1][0]} ? time{k}+1 : time{k});\n" #difine the next behavior for each timer
                # f.write(f"    next(time{k}) := (time{k} < {self.BoolNet.experiments[k][1][0]} ? time{k}+1 : time{k});\n")
                j=0
                for i in self.BoolNet.components.keys():
                    # f.write(f"    next({i}{k}) := {dict1[i+str(k)][reg[j]]};\n")
                    # if len(dict1[f"{i}{k}"])>1:
                    #     str1+=f"    next(choice_{i}{k}) := choice_{i}{k};\n" ######

                    if not self.BoolNet.components[i].def_sources and not self.BoolNet.components[i].opt_sources:
                        str1+=f"    next({i}{k}) := {i}{k};\n"
                        j+=1
                        continue
                    else:
                        str1+=f"    next({i}{k}) := case\n"
                    indx=0
                    for reg in dict1[f"{i}{k}"]:

                        if (re.fullmatch(r"[()]*", reg) or re.fullmatch(r"[)]*", reg) or re.fullmatch(r"[(]*", reg)):
                            continue
                        # str1+=f"           choice_{i}{k} = {reg[1:]} : (time{k} < {self.BoolNet.experiments[k][1][0]} ? {dict1[f"{i}{k}"][reg]}:{i}{k});\n"#define the next for each component in exp
                        # str1 += f"           choice_{i}{k} = {indx} : (time{k} < {self.BoolNet.experiments[k][1][0]} ?\n               case\n"
                        str1 += f"           choice_{i} = {indx} : (time{k} < {self.BoolNet.experiments[k][1][0]} ?\n               case\n"
                        str1  += f"                  "


                        def_srcs = [x for x in self.BoolNet.components[i].def_sources if x in reg]
                        opt_srcs = [x for x in self.BoolNet.components[i].opt_sources if x in reg]
                        if not def_srcs and opt_srcs: #no def sources
                            for opt_src in opt_srcs:
                                for opt_edge in optional_edges:
                                    if opt_edge[0]==opt_src and opt_edge[1]==i:
                                        str1+=f"!edge_{opt_src}_{i}_{opt_edge[2]} & "
                                        #str1+=f"!edge_{opt_src}_{i} & " #########################################################
                                        break
                            str1 = str1[:-3] + f" : FALSE;\n";
                            #str1 = str1[:-3] + f" : {i}{k};\n";
                            str1 += f"                  "
                        def_flag=False
                        add_str = ""
                        # for def_src in self.BoolNet.components[i].def_sources:
                        #     if def_src in reg:
                        #         add_str = ""
                        #         break
                        #     else:
                        #         opt_reg = [o for o in self.BoolNet.components[i].opt_sources if o in reg]
                        #         print(f"opt_reg {opt_reg}")

                        str1+=f"TRUE: {(reg)};\n"
                        str1+=f"               esac : {i}{k});\n"
                        indx+=1
                         ######################
                    str1+=f"               TRUE: {i}{k};\n"
                    str1+=f"           esac;\n"

                        # print(f"PRINT           choice_{i}{k} = {reg[1:]} : (time{k} < {self.BoolNet.experiments[k][1][0]} ? {dict1[f"{i}{k}"][reg]}:{i}{k});\n")
                        # print(f"           choice_{i}{k} = {reg[1:]} : (time{k} < {self.BoolNet.experiments[k][1][0]} ? {dict1[f"{i}{k}"][reg]}:{i}{k});\n")
                    # str1+=f"           TRUE: {i}{k};\n"
                    # str1+="    esac;\n"
                    j+=1
            # for fate in fate_dict.keys():
            #     str1 += f"    next(fate_{fate}) := case\n"
            #     str1 += f"           "
            #     for reg in fate_dict[fate]:
            #         str1 += f"{reg} = 1 & "
            #
            #     str1 = str1[:-3] +f":{fate};\n"
            #
            #
            #     str1+="           TRUE:TRUE;\n"
            #     str1+="    esac;\n"
            for i in self.BoolNet.components.keys():
                # f.write(f"    next({i}{k}) := {dict1[i+str(k)][reg[j]]};\n")
                if len(dict1[f"{i}{k}"]) > 1:
                    str1 += f"    next(choice_{i}) := choice_{i};\n"
            expstr=""
            for exp in self.BoolNet.experiments:
                expstr += f"Experiment{self.experimentNumber}"+ " & " + f"time{self.experimentNumber} = {exp[1][0]}"+" & "
                self.experimentNumber += 1
            self.experimentNumber = 0 #reset
            expstr = expstr[:-3]

                # f.write(f"LTLSPEC F (Experiment{self.experimentNumber} & time{self.experimentNumber} <= {exp[1][0]})\n")
            if self.flag =='ALL':
                str1+=f"LTLSPEC F (Experiment{self.experimentNumber} & time{self.experimentNumber} = {exp[1][0]})\n" #maybe ctlspec, define the exp to reach the experiment
            else:
                str1+=f"LTLSPEC !F ({expstr});\n" #maybe ctlspec, define the exp to reach the experiment
                # str1+=f"CTLSPEC !EF ({expstr});\n" #maybe ctlspec, define the exp to reach the experiment

            self.experimentNumber = 0 #reset

            f.write(str1)
        if(self.os=="Windows"):
            if self.run_nuxmv_interactive("model_optional", expstr):  # run the nuXmv and if return true append it to solution matrix
                self.solutions.append(reg)
                return True

        if(self.os=="Darwin"):
            if self.run_nuxmv_interactive("model_optional.smv", expstr):#run the nuXmv and if return true append it to solution matrix
                self.solutions.append(reg)
                return True
        else:
            return False
#
# import re
#
# import BoolNetwork_Expanded_Huristic
# import disp_viable_models
# from itertools import product
#
# import platform
# import os
# import subprocess
# import time
#
# from ToSmv_Improved import *
# from  ToSmv_Improved_Optional import *
# class ToSmv_Expanded_Huristic(ToSmv_Improved_Optional):
#     def __init__(self,BoolNetwork_Expanded_Huristic):
#         super().__init__(BoolNetwork_Expanded_Huristic)
#
#
#     # def all_combined(self):
#     #     permutations_h = open('test.txt', 'w')
#     #     reg = self.BoolNet.eval_regulation_conditions_optional()
#     #     print(f"reg43rewqreqw: {reg}")
#     #     res = self.python_to_nuxmv()
#     #     if res:
#     #         permutations_h.write(str(res) + "\n")
#
#
#     def all_combined(self):
#         permutations_h= open('test.txt', 'w')
#         l = self.BoolNet.add_perm()
#         res = self.python_to_nuxmv()
#         def_int = [(i[0],i[1],i[2]) for i in self.BoolNet.definite_interactions]
#         print(self.result)
#         for result in self.result:
#             res_int = def_int.copy()
#             print("1")
#             print(res_int)
#             print(def_int)
#             for edge in result:
#                 print("2")
#                 print(edge)
#                 if edge[-1]=="1":
#                     continue
#                 print("3")
#                 edge_parts = edge.split("_")
#                 res_int.append((edge_parts[2],edge_parts[3],edge_parts[4][:-4]))
#             permutations_h.write(str(res_int)+"\n")
#         permutations_h.close()
#
#         if len(self.solutions) != 0: #if we have solutions then create a solution matrix
#             print("here1010")
#             disp_viable_models.txt_to_mat(self.BoolNet.possible_interactions+self.BoolNet.definite_interactions)
#         print("here1011")
#
#         disp_viable_models.disp_experiments(self.BoolNet.experiments)
#         print(self.solutions)
#         print(len(self.solutions))
#
#
#     def python_to_nuxmv(self): #from python to an smv file
#         filename = "model_optional.smv"
#
#         n=len(self.BoolNet.experiments)
#         dict1=self.BoolNet.regConds
#         print(f"mmmmmmm {dict1}")
#         #self.experimentNumber=(self.experimentNumber+1)%len(self.BoolNet.experiments)
#         definite_edges = self.BoolNet.definite_interactions
#         optional_edges = self.BoolNet.possible_interactions
#         print(f"optional_edges: {optional_edges}")
#         print(f"definite111: {self.BoolNet.definite_interactions}")
#         print(f"def_edges: {definite_edges}")
#
#         targets = []
#
#         for edge in definite_edges:
#             targets.append(edge[1])
#         add_fate = self.BoolNet.components.keys() - targets
#         print(f"add_fate: {add_fate}")
#
#         fate_dict={}
#
#
#         with (open(filename, "w") as f):
#             str1 =""
#             str1+="MODULE main\n"+"VAR\n" #add first lines required
#             # f.write("MODULE main\n")
#             # f.write("VAR\n")
#             # f.write(str1)
#             for i in range(n):
#                 for var in self.BoolNet.components: #add all components as boolean
#                     print(f"{var} boolnet var ")
#                     str1+=f"    {var}{i} : boolean;\n"
#                     #str1+=f"    choice_{var}{i} :{set(self.BoolNet.components[var].regulation)};\n"
#                     setD=set(range(len(dict1[f"{var}{i}"])))
#                     if setD!=set():
#                         str1+=f"    choice_{var}{i} :{set(range(len(dict1[f"{var}{i}"])))};\n"   ######
#
#                     # f.write(f"    {var}{i} : boolean;\n")
#                 for var in add_fate:
#                     #str1 += f"    fate_{var}{i} : boolean;\n"
#                     fate_dict[f"{var}{i}"]=[]
#
#                 str1+=f"    time{i}: 0..{self.BoolNet.experiments[i][1][0]};\n" #for each of them add the time for their experiment
#                 # f.write(f"    time{i}: 0..{self.BoolNet.experiments[i][1][0]};\n")
#             # for var in self.BoolNet.components:
#             #     setD = set(range(len(dict1[f"{var}{i}"])))
#             #     if setD != set():
#             #         str1 += f"    choice_{var} :{set(range(len(dict1[f"{var}0"])))};\n"######
#             for opt in optional_edges:
#
#                 str1 += f"    edge_{opt[0]}_{opt[1]}_{opt[2]} : boolean;\n"
#                 #str1 += f"    edge_{opt[0]}_{opt[1]} : boolean;\n"
#                 ##########################################################################################################################
#                 # str1+=  f"    choice_edge_exp{i}_{opt[0]}{i}_{opt[1]}{i}_{opt[2]} : {{0,1}};\n"
#                 str1+=  f"    choice_edge_{opt[0]}_{opt[1]}_{opt[2]} : {{0,1}};\n"
#                 # if opt[1] in add_fate:
#                 #     fate_dict[f"{opt[1]}"].append(f'choice_edge_{opt[0]}_{opt[1]}_{opt[2]}')
#                     # fate_dict[f"{opt[1]}{i}"].append(f'choice_edge_exp{i}_{opt[0]}{i}_{opt[1]}{i}_{opt[2]}')
#
#
#             str1+=f"\nINIT\n"+"    "
#             # f.write(f"\nINIT\n")
#             # f.write("    ")
#             s=""
#             j=0
#             for exp in self.BoolNet.experiments:
#                 for var in exp[0][1].keys():
#                     # print(f"ppppp {var}")
#                     s+=f"({var}{j} = {str(bool(int(exp[0][1][var]))).upper()})&" #for each experiment initialize the variables with 0=FALSE,1=TRUE
#                 # s += f"({i}{j} = {str(bool(int(exp[0])).upper()})&"
#                 # print(f"dfsam,df;saml;fdkasnmdfas{exp}")
#                 # print(f"dsafdasfgdasadfgsafgdsagfsdagfsdagfsdgafsdafdgsdfsam,df;saml;fdkasnmdfas{exp[0]}")
#                 s += f"(time{j} = 0) & " #init each time to 0    ##########################################################################################################################
#                 j += 1
#             for opt in optional_edges:
#                 s+=f"(edge_{opt[0]}_{opt[1]}_{opt[2]} = (choice_edge_{opt[0]}_{opt[1]}_{opt[2]} = 0 ? TRUE : FALSE)) & "
#                 #s+=f"(edge_{opt[0]}_{opt[1]} = (choice_edge_{opt[0]}_{opt[1]}_{opt[2]} = 0 ? TRUE : FALSE)) & "
#                 ##########################################################################################################################
#                 # s+=f"(edge_{opt[0]}{i}_{opt[1]}{i}_{opt[2]} = (choice_edge_exp{i}_{opt[0]}{i}_{opt[1]}{i}_{opt[2]} = 0 ? TRUE : FALSE)) & "
#
#
#             # str1 += f"(time{j} = 0)&"
#             str1 += s[:-3] + ";" #remove last & char from the file
#             # print(f"dddddd {s}")
#
#             # for j in range(n):
#             #     exp = self.BoolNet.experiments[j]
#             #     print(exp)
#             #     for i in exp[j][1].keys():
#             #         s+= f"({i}{j} = {str(bool(int(exp[j][1][i]))).upper()})&"
#             #         print(s)
#             #         # str1 += f"({i}{j} = {str(bool(int(exp[j][1][i]))).upper()})&"
#             #
#             #     s+= f"(time{j} = 0)&"
#             #     # str1 += f"(time{j} = 0)&"
#             # str1+=s[:-1]+";"
#             # f.write(s[:-1]+";")
#             str1+="\nDEFINE\n"
#             # f.write("\nDEFINE\n")
#
#             for exp in self.BoolNet.experiments:
#                 str1+=f"    Experiment{self.experimentNumber} :=" #write the experiment + its number
#                 # f.write(f"    Experiment{self.experimentNumber} :=")
#                 keys = list(exp[1][1].keys()) #get the values of the components
#                 for index, i in enumerate(keys):
#                     if index == len(keys) - 1: #for last component in exp
#                         str1+=f"({i}{self.experimentNumber} = {str(bool(int(exp[1][1][i]))).upper()});" #write the a(exp_num)=TRUE, etc
#                         # f.write(f"({i}{self.experimentNumber} = {str(bool(int(exp[1][1][i]))).upper()});")
#                     else:
#                         str1+=f"({i}{self.experimentNumber} = {str(bool(int(exp[1][1][i]))).upper()})&"
#                         # f.write(f"({i}{self.experimentNumber} = {str(bool(int(exp[1][1][i]))).upper()})&")
#                 str1+="\n"
#                 self.experimentNumber += 1
#             self.experimentNumber = 0
#
#             # f.write("\nASSIGN\n")
#             str1+="\nASSIGN\n"
#
#             # for fate in fate_dict.keys():
#             #     str1 += f"    next(fate_{fate}) := case\n"
#             #     str1 += f"           "
#             #     for reg in fate_dict[fate]:
#             #         str1 += f"{reg} = 1 & "
#             #
#             #     str1 = str1[:-3] +f":{fate};\n"
#             #
#             #
#             #     str1+="           TRUE:TRUE;\n"
#             #     str1+="    esac;\n"
#
#             # reg = self.reglist[regidx]  ####################change back
#             # print(reg)
#             str2=""
#
#             for opt in optional_edges:
#                 str1 += f"    next(choice_edge_{opt[0]}_{opt[1]}_{opt[2]}) := choice_edge_{opt[0]}_{opt[1]}_{opt[2]};\n"
#                 str1 += f"    next(edge_{opt[0]}_{opt[1]}_{opt[2]}) := edge_{opt[0]}_{opt[1]}_{opt[2]};\n"
#                 #str1 += f"    next(edge_{opt[0]}_{opt[1]}) := edge_{opt[0]}_{opt[1]};\n"
#                 ##########################################################################################################################
#
#
#                     # str1 += f"    next(edge_{opt[0]}{k}_{opt[1]}{k}_{opt[2]}) := case\n"
#                     # str1 += f"       choice_edge_exp_{opt[0]}{k}_{opt[1]}{k}_{opt[2]} = 0 :TRUE;\n"
#                     # str1 += f"       choice_edge_exp_{opt[0]}{k}_{opt[1]}{k}_{opt[2]} = 1 :FALSE;\n"
#                     # str1 += f"       TRUE:edge_{opt[0]}{k}_{opt[1]}{k}_{opt[2]};\n"
#                     # str1 += f"    esac;\n"
#
#             for k in range(n):
#
#                 str1+=f"    next(time{k}) := (time{k} < {self.BoolNet.experiments[k][1][0]} ? time{k}+1 : time{k});\n" #difine the next behavior for each timer
#                 # f.write(f"    next(time{k}) := (time{k} < {self.BoolNet.experiments[k][1][0]} ? time{k}+1 : time{k});\n")
#                 j=0
#                 for i in self.BoolNet.components.keys():
#                     # f.write(f"    next({i}{k}) := {dict1[i+str(k)][reg[j]]};\n")
#                     if len(dict1[f"{i}{k}"])>1:
#                         str1+=f"    next(choice_{i}{k}) := choice_{i}{k};\n" ######
#                     print(f" optt {i} {self.BoolNet.components[i].opt_sources}")
#                     print(f" deff {i} {self.BoolNet.components[i].def_sources}")
#                     if not self.BoolNet.components[i].def_sources and not self.BoolNet.components[i].opt_sources:
#                         str1+=f"    next({i}{k}) := {i}{k};\n"
#                         j+=1
#                         continue
#                     else:
#                         str1+=f"    next({i}{k}) := case\n"
#                     indx=0
#                     for reg in dict1[f"{i}{k}"]:
#                         print(f"reg {reg}")
#                         if (re.fullmatch(r"[()]*", reg) or re.fullmatch(r"[)]*", reg) or re.fullmatch(r"[(]*", reg)):
#                             print("cont")
#                             continue
#                         # str1+=f"           choice_{i}{k} = {reg[1:]} : (time{k} < {self.BoolNet.experiments[k][1][0]} ? {dict1[f"{i}{k}"][reg]}:{i}{k});\n"#define the next for each component in exp
#                         str1 += f"           choice_{i}{k} = {indx} : (time{k} < {self.BoolNet.experiments[k][1][0]} ?\n               case\n"
#                         str1  += f"                  "
#                         print(f"i {i}")
#                         print(f"def {self.BoolNet.components[i].def_sources}")
#                         print(f"opt {self.BoolNet.components[i].opt_sources}")
#
#                         def_srcs = [x for x in self.BoolNet.components[i].def_sources if x in reg]
#                         opt_srcs = [x for x in self.BoolNet.components[i].opt_sources if x in reg]
#                         if not def_srcs and opt_srcs: #no def sources
#                             for opt_src in opt_srcs:
#                                 print(f"opt_src {opt_src}")
#                                 for opt_edge in optional_edges:
#                                     print(f"opt_edge {opt_edge}")
#                                     print(i)
#                                     if opt_edge[0]==opt_src and opt_edge[1]==i:
#                                         str1+=f"!edge_{opt_src}_{i}_{opt_edge[2]} & "
#                                         #str1+=f"!edge_{opt_src}_{i} & " #########################################################
#                                         break
#                             str1 = str1[:-3] + f" : FALSE;\n";
#                             #str1 = str1[:-3] + f" : {i}{k};\n";
#                             str1 += f"                  "
#                         print(f"dict111111{dict1[f"{i}{k}"]}")
#                         def_flag=False
#                         add_str = ""
#                         # for def_src in self.BoolNet.components[i].def_sources:
#                         #     if def_src in reg:
#                         #         add_str = ""
#                         #         break
#                         #     else:
#                         #         opt_reg = [o for o in self.BoolNet.components[i].opt_sources if o in reg]
#                         #         print(f"opt_reg {opt_reg}")
#
#                         str1+=f"TRUE: {reg};\n"
#                         str1+=f"               esac : {i}{k});\n"
#                         indx+=1
#                     str1+=f"               TRUE: {i}{k};\n"
#                     str1+=f"           esac;\n"
#
#                         # print(f"PRINT           choice_{i}{k} = {reg[1:]} : (time{k} < {self.BoolNet.experiments[k][1][0]} ? {dict1[f"{i}{k}"][reg]}:{i}{k});\n")
#                         # print(f"           choice_{i}{k} = {reg[1:]} : (time{k} < {self.BoolNet.experiments[k][1][0]} ? {dict1[f"{i}{k}"][reg]}:{i}{k});\n")
#                     # str1+=f"           TRUE: {i}{k};\n"
#                     # str1+="    esac;\n"
#                     j+=1
#             # for fate in fate_dict.keys():
#             #     str1 += f"    next(fate_{fate}) := case\n"
#             #     str1 += f"           "
#             #     for reg in fate_dict[fate]:
#             #         str1 += f"{reg} = 1 & "
#             #
#             #     str1 = str1[:-3] +f":{fate};\n"
#             #
#             #
#             #     str1+="           TRUE:TRUE;\n"
#             #     str1+="    esac;\n"
#             # for i in self.BoolNet.components.keys():
#             #     # f.write(f"    next({i}{k}) := {dict1[i+str(k)][reg[j]]};\n")
#             #     if len(dict1[f"{i}{k}"]) > 1:
#             #         str1 += f"    next(choice_{i}) := choice_{i};\n"
#             expstr=""
#             for exp in self.BoolNet.experiments:
#                 print(f"exp {exp}")
#                 expstr += f"Experiment{self.experimentNumber}"+ " & " + f"time{self.experimentNumber} = {exp[1][0]}"+" & "
#                 self.experimentNumber += 1
#             self.experimentNumber = 0 #reset
#             expstr = expstr[:-3]
#
#                 # f.write(f"LTLSPEC F (Experiment{self.experimentNumber} & time{self.experimentNumber} <= {exp[1][0]})\n")
#             if self.flag =='ALL':
#                 str1+=f"LTLSPEC F (Experiment{self.experimentNumber} & time{self.experimentNumber} = {exp[1][0]})\n" #maybe ctlspec, define the exp to reach the experiment
#             else:
#                 str1+=f"CTLSPEC !EF ({expstr});\n" #maybe ctlspec, define the exp to reach the experiment
#
#             self.experimentNumber = 0 #reset
#
#             f.write(str1)
#         if(self.os=="Windows"):
#             if self.run_nuxmv_interactive("model_optional", reg):  # run the nuXmv and if return true append it to solution matrix
#                 self.solutions.append(reg)
#                 return True
#
#         if(self.os=="Darwin"):
#             if self.run_nuxmv_interactive("model_optional.smv", expstr):#run the nuXmv and if return true append it to solution matrix
#                 self.solutions.append(reg)
#                 return True
#         else:
#             return False

