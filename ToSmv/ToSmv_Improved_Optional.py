import queue
from queue import Queue
import subprocess
import os
import threading
from queue import Queue, Empty
import time
from GUI import *
from ToSmv.ToSmv_Improved import *
from BoolNet.BoolNetwork_Optional import *
from Regulation import *
#add_property -c " !EF (Experiment0 & time0 <= 10 & !(choice_edge_exp_A0_B0_positive = 0))"
#read_model;flatten_hierarchy;encode_variables;build_model;check_ctlspec
#check_property -c -p "!EF (Experiment0 & time0 <= 10 & (choice_edge_exp_B0_X0_positive = 1))"
class ToSmv_Improved_Optional(ToSmv_Improved):
    def __init__(self, BoolNet):
        super().__init__(BoolNet)
        self.result = []


    def all_combined(self):
        permutations_h= open('test.txt', 'w')
        reg = self.BoolNet.eval_regulation_conditions_optional()
        res = self.python_to_nuxmv()
        def_int = [(i[0],i[1],i[2]) for i in self.BoolNet.definite_interactions]

        for result in self.result:
            res_int = def_int.copy()

            for edge in result:
                if edge[-1] == "1":
                    continue
                edge_parts = edge.split("_")
                res_int.append((edge_parts[2], edge_parts[3], edge_parts[4][:-4]))
            permutations_h.write(str(res_int) + "\n")

        permutations_h.close()
        #if len(res_int)!=0:
        if len(self.result) != 0: #if we have solutions then create a solution matrix
            pass
        txt_to_mat(self.BoolNet.possible_interactions+self.BoolNet.definite_interactions)



        disp_experiments(self.BoolNet.experiments)


    def python_to_nuxmv(self): #from python to an smv file
        filename = "model_optional.smv"

        n=len(self.BoolNet.experiments)
        dict1=self.BoolNet.regConds
        dict1 = self.trim(dict1)
        exps = self.BoolNet.experiments


        # for comp in dict1.keys():
        #     temp = ""
        #     if comp[:-1] not in exps[int(comp[-1])][1][1].keys():
        #         continue
        #     if exps[int(comp[-1])][1][1][comp[:-1]]=="1":
        #         for reg in dict1[comp]:
        #             temp+=f"({dict1[comp][reg]}) | "
        #     else:
        #         for reg in dict1[comp]:
        #             temp+=f"({dict1[comp][reg]}) & "
        #     if len(dict1[comp])!=0:
        #         temp=temp[:-3]
        #
        #
        #     dict1[comp].clear()
        #     dict1[comp]["R0"]=temp


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
                    #str1+=f"    choice_{var}{i} :{set(self.BoolNet.components[var].regulation)};\n" #####
                    # f.write(f"    {var}{i} : boolean;\n")
                for var in add_fate:
                    #str1 += f"    fate_{var}{i} : boolean;\n"
                    fate_dict[f"{var}{i}"]=[]

                str1+=f"    time{i}: 0..{self.BoolNet.experiments[i][1][0]};\n" #for each of them add the time for their experiment
                # f.write(f"    time{i}: 0..{self.BoolNet.experiments[i][1][0]};\n")
            for var in self.BoolNet.components:
                str1 += f"    choice_{var} :{set(self.BoolNet.components[var].regulation)};\n" ######

            for opt in optional_edges:

                str1 += f"    edge_{opt[0]}_{opt[1]}_{opt[2]} : boolean;\n"
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
                s += f"(time{j} = 0) & " #init each time to 0
                j += 1
            for opt in optional_edges:
                s+=f"(edge_{opt[0]}_{opt[1]}_{opt[2]} = (choice_edge_{opt[0]}_{opt[1]}_{opt[2]} = 0 ? TRUE : FALSE)) & "
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

                    # str1 += f"    next(edge_{opt[0]}{k}_{opt[1]}{k}_{opt[2]}) := case\n"
                    # str1 += f"       choice_edge_exp_{opt[0]}{k}_{opt[1]}{k}_{opt[2]} = 0 :TRUE;\n"
                    # str1 += f"       choice_edge_exp_{opt[0]}{k}_{opt[1]}{k}_{opt[2]} = 1 :FALSE;\n"
                    # str1 += f"       TRUE:edge_{opt[0]}{k}_{opt[1]}{k}_{opt[2]};\n"
                    # str1 += f"    esac;\n"
            for i in self.BoolNet.components.keys():#####
                if len(dict1[f"{i}0"]) > 1:
                    str1 += f"    next(choice_{i}) := choice_{i};\n"
            for k in range(n):

                str1+=f"    next(time{k}) := (time{k} < {self.BoolNet.experiments[k][1][0]} ? time{k}+1 : time{k});\n" #difine the next behavior for each timer
                # f.write(f"    next(time{k}) := (time{k} < {self.BoolNet.experiments[k][1][0]} ? time{k}+1 : time{k});\n")
                j=0
                for i in self.BoolNet.components.keys():
                    # if len(dict1[f"{i}{k}"])>1:
                    #     str1+=f"    next(choice_{i}{k}) := choice_{i}{k};\n" #####

                    if not self.BoolNet.components[i].def_sources and not self.BoolNet.components[i].opt_sources:
                        str1+=f"    next({i}{k}) := {i}{k};\n"
                        j+=1
                        continue
                    else:
                        str1+=f"    next({i}{k}) := case\n"
                    for reg in dict1[f"{i}{k}"]:
                        # str1+=f"           choice_{i}{k} = {reg[1:]} : (time{k} < {self.BoolNet.experiments[k][1][0]} ? {dict1[f"{i}{k}"][reg]}:{i}{k});\n"#define the next for each component in exp
                        str1 += f"           choice_{i} = {reg[1:]} : (time{k} < {self.BoolNet.experiments[k][1][0]} ?\n               case\n" ##### k removed
                        str1  += f"                  "

                        if not self.BoolNet.components[i].def_sources and self.BoolNet.components[i].opt_sources: #no def sources
                            for opt_src in self.BoolNet.components[i].opt_sources:

                                for opt_edge in optional_edges:
                                    if opt_edge[0]==opt_src and opt_edge[1]==i:
                                        str1+=f"!edge_{opt_src}_{i}_{opt_edge[2]} & "
                                        break

                            str1 = str1[:-3] + f" : FALSE;\n"; #####
                            #str1 = str1[:-3] + f" : {i}{k};\n"; #####
                            #str1 = str1[:-3] + f" : {i}{k};\n";
                            str1 += f"                  "
                        str1+=f"TRUE: {(dict1[f"{i}{k}"][reg])};\n"
                        str1+=f"               esac : {i}{k});\n"
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




    def python_to_nuxmv1(self): #from python to an smv file
        filename = "model_optional.smv"

        n=len(self.BoolNet.experiments)
        dict1=self.BoolNet.regConds
        dict1 = self.trim(dict1)
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
                    #str1+=f"    choice_{var}{i} :{set(self.BoolNet.components[var].regulation)};\n" #####
                    # f.write(f"    {var}{i} : boolean;\n")
                for var in add_fate:
                    #str1 += f"    fate_{var}{i} : boolean;\n"
                    fate_dict[f"{var}{i}"]=[]

                str1+=f"    time{i}: 0..{self.BoolNet.experiments[i][1][0]};\n" #for each of them add the time for their experiment
                # f.write(f"    time{i}: 0..{self.BoolNet.experiments[i][1][0]};\n")
            for var in self.BoolNet.components:
                str1 += f"    choice_{var} :{set(self.BoolNet.components[var].regulation)};\n" ######

            for opt in optional_edges:

                str1 += f"    edge_{opt[0]}_{opt[1]}_{opt[2]} : boolean;\n"
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
                s += f"(time{j} = 0) & " #init each time to 0
                j += 1
            for opt in optional_edges:
                s+=f"(edge_{opt[0]}_{opt[1]}_{opt[2]} = (choice_edge_{opt[0]}_{opt[1]}_{opt[2]} = 0 ? TRUE : FALSE)) & "
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

                    # str1 += f"    next(edge_{opt[0]}{k}_{opt[1]}{k}_{opt[2]}) := case\n"
                    # str1 += f"       choice_edge_exp_{opt[0]}{k}_{opt[1]}{k}_{opt[2]} = 0 :TRUE;\n"
                    # str1 += f"       choice_edge_exp_{opt[0]}{k}_{opt[1]}{k}_{opt[2]} = 1 :FALSE;\n"
                    # str1 += f"       TRUE:edge_{opt[0]}{k}_{opt[1]}{k}_{opt[2]};\n"
                    # str1 += f"    esac;\n"
            for i in self.BoolNet.components.keys():#####
                if len(dict1[f"{i}0"]) > 1:
                    str1 += f"    next(choice_{i}) := choice_{i};\n"
            for k in range(n):

                str1+=f"    next(time{k}) := (time{k} < {self.BoolNet.experiments[k][1][0]} ? time{k}+1 : time{k});\n" #difine the next behavior for each timer
                # f.write(f"    next(time{k}) := (time{k} < {self.BoolNet.experiments[k][1][0]} ? time{k}+1 : time{k});\n")
                j=0
                for i in self.BoolNet.components.keys():
                    # if len(dict1[f"{i}{k}"])>1:
                    #     str1+=f"    next(choice_{i}{k}) := choice_{i}{k};\n" #####

                    if not self.BoolNet.components[i].def_sources and not self.BoolNet.components[i].opt_sources:
                        str1+=f"    next({i}{k}) := {i}{k};\n"
                        j+=1
                        continue
                    else:
                        str1+=f"    next({i}{k}) := case\n"
                    for reg in dict1[f"{i}{k}"]:
                        # str1+=f"           choice_{i}{k} = {reg[1:]} : (time{k} < {self.BoolNet.experiments[k][1][0]} ? {dict1[f"{i}{k}"][reg]}:{i}{k});\n"#define the next for each component in exp
                        str1 += f"           choice_{i} = {reg[1:]} : (time{k} < {self.BoolNet.experiments[k][1][0]} ?\n               case\n" ##### k removed
                        str1  += f"                  "

                        if not self.BoolNet.components[i].def_sources and self.BoolNet.components[i].opt_sources: #no def sources
                            for opt_src in self.BoolNet.components[i].opt_sources:
                                for opt_edge in optional_edges:
                                    if opt_edge[0]==opt_src and opt_edge[1]==i:
                                        str1+=f"!edge_{opt_src}_{i}_{opt_edge[2]} & "
                                        break

                            str1 = str1[:-3] + f" : FALSE;\n"; #####
                            #str1 = str1[:-3] + f" : {i}{k};\n"; #####
                            #str1 = str1[:-3] + f" : {i}{k};\n";
                            str1 += f"                  "
                        str1+=f"TRUE: {dict1[f"{i}{k}"][reg]};\n"
                        str1+=f"               esac : {i}{k});\n"
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
                str1+=f"CTLSPEC !EF ({expstr});\n" #maybe ctlspec, define the exp to reach the experiment

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


    def run_nuxmv_opt1(self,input_file,reg): #run the newXmv program with a batch file and get the self.result
        self.result = subprocess.run([r'.\RUN_opt.bat', input_file], capture_output=True, text=True)
        # Print the output of the PowerShell command
        self.log.write(f"\n{reg}\n")
        if self.result.returncode == 0:
            self.log.write(f"\n{self.result.stdout[1113:]}") #delete all copyright lines and such
        else:
            #self.log.write(f"Error occurred:\n{self.result.stdout}")
            self.log.write(f"Error occurred:\n{self.result.stderr}")

        #print(self.result.stdout.count("true"))
        if self.result.stdout.count("is false") == len(self.BoolNet.experiments): #if the count of experiments that were true is the same as number of experiments in general then
            #success
            return True
        return False



        return output.count("is false") == len(self.BoolNet.experiments)

    # self.result = []

    def enqueue_output(self,out, queue):
        for line in iter(out.readline, ''):
            queue.put(line)
        out.close()

    def run_nuxmv_interactive(self,input_file, expstr):
        counter = 0
        def read_until_prompt(cmd,timeout=3):
            output = []
            last_line_time = time.time()

            while True:
                try:
                    line = q.get(timeout=0.2)
                    # print(f"dsanlkkfd {repr(line)}")
                    # output += line
                    output.append(line)
                    last_line_time = time.time()

                    if "nuXmv >" in line or "nuXmv>" in line or line.strip().endswith("nuXmv>"):
                        break

                except queue.Empty:
                    if  cmd!="show_traces" and time.time() - last_line_time > timeout:
                        print("Prompt timeout reached, assuming prompt shown")
                        break
            return output

        # Path to nuXmv
        smv_path = open("Path/nuxmv_path.txt")
        nuxmv_executable = smv_path.readline().strip()

        # Ensure valid path to input .smv file
        if not input_file.endswith(".smv"):
            input_file += ".smv"
        input_file = os.path.abspath(input_file)

        # Start nuXmv process in interactive mode
        proc = subprocess.Popen(
            [nuxmv_executable, "-int", input_file],
            stdin=subprocess.PIPE,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            text=True,
            bufsize=10
        )

        # Setup threaded reader for stdout
        q = Queue()
        t = threading.Thread(target=self.enqueue_output, args=(proc.stdout, q))
        t.daemon = True
        t.start()

        print("Waiting for nuXmv to start...")
        read_until_prompt("start")

        # List of commands to run
        # commands = ["read_model", "flatten_hierarchy", "encode_variables", "build_model", "check_ctlspec","show_traces"]
        commands = ["read_model;flatten_hierarchy;encode_variables;build_model","go_bmc","check_ltlspec_bmc -k 30","show_traces"]
        # commands = ["read_model;flatten_hierarchy;encode_variables;build_model","check_ltlspec","show_traces"]
        for cmd in commands:
            print(f"\nRunning command: {repr(cmd)}")
            proc.stdin.write(cmd + "\n")
            proc.stdin.flush()

            output = read_until_prompt(cmd)
            print(f"Output for {cmd}:\n{output}")

        edges = [i.strip() for i in output if i.strip().startswith("choice_edge_")]
        if (len(edges) > 0 or len(self.BoolNet.possible_interactions)==0):
            self.result.append(edges)


        stringos = ""
        while len(edges) > 0:
            # time.sleep(1)
            for idx in self.result:
                stringos += "("
                for edge in idx:
                    stringos += edge + " & "
                stringos = stringos[:-3]
                stringos += ") | "

            stringos = stringos[:-3]

            curcommand = f"check_ltlspec_bmc -k 30 -p \"!F ({expstr} & !({stringos}) )\""
            proc.stdin.write(curcommand + "\n")
            output = read_until_prompt("output")
            # proc.stdin.write("show_traces"+"\n")
            # output = read_until_prompt()
            print(f"Output for {curcommand}:\n{output}")
            for line in output:
                print(line)
            stringos = ""
            edges = [i.strip() for i in output if i.strip().startswith("choice_edge_")]
            if(len(edges) > 0):
                 # counter+=1
                 self.result.append(edges)
                 self.result = list(set(tuple(x) for x in self.result))
                 counter=len(self.result)

                 if (len(self.result) >= self.solution_counter):
                     break


        # Exit cleanly
        proc.stdin.write("quit\n")
        proc.stdin.flush()
        proc.wait()
        self.result2 = list(set(tuple(x) for x in self.result))

        self.result=self.result2
        return proc.returncode == 0

