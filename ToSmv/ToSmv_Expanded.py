

from itertools import product

import platform
import os
import subprocess
import time

from ToSmv.ToSmv_Improved import *
from GUI import *
class ToSmv_Expanded(ToSmv_Improved):
    def __init__(self,BoolNet):
        super().__init__(BoolNet)


    def all_combined(self):
        permutations_h= open('test.txt', 'w')
        while abs(self.BoolNet.perm_index) <= len(self.BoolNet.perm_interactions): #iterate over all permultations
            l = self.BoolNet.add_perm()
            res = self.python_to_nuxmv()
            if res:
                permutations_h.write(str(l)+"\n")
        permutations_h.close()
        if len(self.solutions) != 0: #if we have solutions then create a solution matrix
            txt_to_mat()
        disp_experiments(self.BoolNet.experiments)




    def python_to_nuxmv(self): #from python to an smv file
        filename = "model.smv"
        n=len(self.BoolNet.experiments)
        dict1=self.BoolNet.regConds
        # dict1 = self.trim(dict1)
        #self.experimentNumber=(self.experimentNumber+1)%len(self.BoolNet.experiments)
        with open(filename, "w") as f:
            str1 =""
            str1+="MODULE main\n"+"VAR\n" #add first lines required
            # f.write("MODULE main\n")
            # f.write("VAR\n")
            # f.write(str1)
            for i in range(n):
                for var in self.BoolNet.components: #add all components as boolean
                    str1+=f"    {var}{i} : boolean;\n"
                    if len(dict1[var+str(i)])!=0:
                        str1 += f"    choice_{var}{i} :{set(range(len(dict1[var + str(i)])))};\n"
                    # f.write(f"    {var}{i} : boolean;\n")
                str1+=f"    time{i}: 0..{self.BoolNet.experiments[i][1][0]};\n" #for each of them add the time for their experiment
                # f.write(f"    time{i}: 0..{self.BoolNet.experiments[i][1][0]};\n")

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
                s += f"(time{j} = 0)&" #init each time to 0
                j += 1
            # str1 += f"(time{j} = 0)&"
            str1 += s[:-1] + ";" #remove last & char from the file
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
            # reg = self.reglist[regidx]  ####################change back
            # print(reg)
            str2=""
            for k in range(n):
                str1+=f"    next(time{k}) := (time{k} < {self.BoolNet.experiments[k][1][0]} ? time{k}+1 : time{k});\n" #difine the next behavior for each timer
                # f.write(f"    next(time{k}) := (time{k} < {self.BoolNet.experiments[k][1][0]} ? time{k}+1 : time{k});\n")
                j=0
                for i in self.BoolNet.components.keys():
                    # f.write(f"    next({i}{k}) := {dict1[i+str(k)][reg[j]]};\n")
                    if len(dict1[f"{i}{k}"])>1:
                        str1+=f"    next(choice_{i}{k}) := choice_{i}{k};\n"
                    str1+=f"    next({i}{k}) := case\n"
                    idx=0
                    for reg in (dict1[f"{i}{k}"]):
                        str1+=f"           choice_{i}{k} = {idx} : (time{k} < {self.BoolNet.experiments[k][1][0]} ? {reg}:{i}{k});\n"#define the next for each component in exp
                        idx+=1

                        # print(f"           choice_{i}{k} = {reg[1:]} : (time{k} < {self.BoolNet.experiments[k][1][0]} ? {dict1[f"{i}{k}"][reg]}:{i}{k});\n")
                    str1+=f"           TRUE: {i}{k};\n"
                    str1+="    esac;\n"
                    j+=1
            for exp in self.BoolNet.experiments:
                # f.write(f"LTLSPEC F (Experiment{self.experimentNumber} & time{self.experimentNumber} <= {exp[1][0]})\n")
                if self.flag =='ALL':
                    str1+=f"LTLSPEC F (Experiment{self.experimentNumber} & time{self.experimentNumber} <= {exp[1][0]})\n" #maybe ctlspec, define the exp to reach the experiment
                else:
                    str1+=f"CTLSPEC !EF (Experiment{self.experimentNumber} & time{self.experimentNumber} <= {exp[1][0]})\n" #maybe ctlspec, define the exp to reach the experiment

                self.experimentNumber += 1 #iterate over experiment number
            self.experimentNumber = 0 #reset

            f.write(str1)
        if(self.os=="Windows"):
            if self.run_nuxmv("model", reg):  # run the nuXmv and if return true append it to solution matrix
                self.solutions.append(reg)
                return True

        if(self.os=="Darwin"):
            if self.run_nuxmvMAC("model",reg):#run the nuXmv and if return true append it to solution matrix
                self.solutions.append(reg)
                return True
        else:
            return False


