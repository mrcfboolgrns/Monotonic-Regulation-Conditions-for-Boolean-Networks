

from GUI import *

import platform
import os
import subprocess
import time
class ToSmv_Improved:
    def __init__(self, BoolNet):
        self.BoolNet= BoolNet
        self.experimentNumber=0
        self.reglist = []
        self.solutions = []
        self.log = open("log.txt", "w") #for saving the log of the run
        self.solution_counter = 0
        self.flag = ""
        self.os = platform.system()
        # self.perm_index=0
        #
        # self.BoolNet.perm_interactions[self.perm_index]
        # self.BoolNet.defind=
    # def generate_permutations(self, *arrays):
    #     self.reglist = list(product(*arrays))
    #     # print((self.reglist))

    def mode(self,str):
        self.flag = str

    def num_solutions(self, i):
        self.solution_counter = i

    # def all_regulation_conditions(self): #get all permutations for the possible regulation conditions
    #     temp = []
    #     for i in self.BoolNet.components.values():
    #         # print("fgnaklfagdnkfglgfnklagafnkfg")
    #         temp.append([f"R{j}" for j in i.regulation])
    #     self.generate_permutations(*temp)



    def run_nuxmv(self,input_file,reg): #run the newXmv program with a batch file and get the result
        result = subprocess.run([r'.\RUN.bat', input_file], capture_output=True, text=True)
        # Print the output of the PowerShell command
        self.log.write(f"\n{reg}\n")
        if result.returncode == 0:
            self.log.write(f"\n{result.stdout[1113:]}") #delete all copyright lines and such
        else:
            #self.log.write(f"Error occurred:\n{result.stdout}")
            self.log.write(f"Error occurred:\n{result.stderr}")

        #print(result.stdout.count("true"))
        if result.stdout.count("is false") == len(self.BoolNet.experiments): #if the count of experiments that were true is the same as number of experiments in general then
            #success
            return True
        return False


    def run_nuxmvMAC(self, input_file, reg):
        smv_path = open("Path/nuxmv_path.txt")
        nuxmv_path = smv_path.readline().strip()

        # Ensure the file has the .smv extension
        if not input_file.endswith(".smv"):
            input_file += ".smv"

        # Convert input_file to absolute path
        input_file = os.path.abspath(input_file)
        self.log.write(f"Using input file: {input_file}\n")

        # Wait until the file exists and is non-empty
        timeout = 10  # Max wait time in seconds
        elapsed = 0
        while not (os.path.exists(input_file) and os.path.getsize(input_file) > 0):
            if elapsed >= timeout:
                self.log.write(f"Error: Input file {input_file} not found or empty after waiting!\n")
                return False
            time.sleep(0.5)
            elapsed += 0.5

        # Run nuXmv
        command = f'"{nuxmv_path}" "{input_file}"'
        self.log.write(f"Running command: {command}\n")

        result = subprocess.run(command, shell=True, capture_output=True, text=True)

        self.log.write(f"\n{reg}\n")

        if result.returncode == 0:
            self.log.write(f"\n{result.stdout[1113:]}")
        else:
            self.log.write(f"Error occurred:\n{result.stderr}")

        if result.stdout.count("is false") == len(self.BoolNet.experiments):
            return True  # Suc


    def all_combined(self):
        permutations_h= open('test.txt', 'w')
        while self.BoolNet.perm_index < len(self.BoolNet.perm_interactions): #iterate over all permultations
            l = self.BoolNet.add_perm()
            res = self.python_to_nuxmv()
            if res:
                permutations_h.write(str(l)+"\n")



        permutations_h.close()
        if len(self.solutions) != 0: #if we have solutions then create a solution matrix
            # disp_viable_models.txt_to_mat()
            txt_to_mat()
        # disp_viable_models.disp_experiments(self.BoolNet.experiments)
        disp_experiments(self.BoolNet.experiments)




    def trim(self,input_dict):
        trimmed_dict = {}
        regulation_data={}
        for k in range(len(self.BoolNet.experiments)):
            for i in self.BoolNet.components:
                regulation_data[i+str(k)]=self.BoolNet.components[i].regulation

        for key, value in input_dict.items():
            if key in regulation_data:
                allowed_keys = {f'R{num}' for num in regulation_data[key]}  # Set of allowed R keys
                trimmed_dict[key] = {k: v for k, v in value.items() if k in allowed_keys}
        return trimmed_dict


    def python_to_nuxmv(self): #from python to an smv file
        filename = "model.smv"
        n=len(self.BoolNet.experiments)
        dict1=self.BoolNet.regConds
        dict1 = self.trim(dict1)
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
                    str1+=f"    choice_{var}{i} :{set(self.BoolNet.components[var].regulation)};\n"
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
                    for reg in dict1[f"{i}{k}"]:
                        str1+=f"           choice_{i}{k} = {reg[1:]} : (time{k} < {self.BoolNet.experiments[k][1][0]} ? {dict1[f"{i}{k}"][reg]}:{i}{k});\n"#define the next for each component in exp
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

def process_input_and_write_to_file(input_file, output_file): #for each saved char by nuXmv (like A E F and such), create a final file with these chars lowered
    try:
        if isinstance(input_file, str):
            with open(input_file, "r") as file:
                lines = file.readlines()
        else:
            lines = input_file.readlines()

        output_lines = []
        for line in lines:
            line = line.strip()

            parts = line.split()
            for i in range(len(parts)):
                if any(ch in parts[i] for ch in "AEGFX"):
                    parts[i] = parts[i].lower()

            output_lines.append(" ".join(parts))

        with open(output_file, "w") as file:
            file.write("\n".join(output_lines) + "\n")

    except FileNotFoundError:
        print(f"Error: The file {input_file} was not found.")
    except IOError as e:
        print(f"Error: There was an issue with file reading or writing: {e}")


