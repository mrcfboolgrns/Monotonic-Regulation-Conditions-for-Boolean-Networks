import os
import testingZ3

path = 'biodivine-boolean-models/models'  # the BBM dataset is downloaded
os.chdir(path)
countM, countT, countS, countWS = 0, 0, 0, 0
fm, fs, fws = 0, 0, 0
tempm, temps, tempWS = 0, 0, 0
nonmono, WS, nonWS = [], [], []
for i in range(245):
    dire = os.listdir()[i]
    if os.path.isdir(dire):
        os.chdir(dire)
        for file in os.listdir():
            if file.endswith('.bnet'):
                tempm, tempS, tempWS = 1, 1, 1
                with open(file, 'rb') as f:
                    content = f.readlines()  # Decode from bytes to string
                    for line in content[1:]:
                        line = line.decode('utf-8')
                        # Splitting by comma and extracting the right-hand side (the Boolean formula)
                        if ',' in line:
                            target, formula = line.strip().split(',', 1)
                            countT += 1
                            if testingZ3.check_mono(formula):
                                countM += 1
                                if testingZ3.check_symmetry(formula):
                                    countS += 1
                                else:
                                    tempS = 0
                                    res = testingZ3.check_WS(formula)
                                    if not res:
                                        nonWS.append([formula, f"from the dir:{dire}"])
                                        tempWS = 0
                                    else:
                                        WS.append([res, formula, f"from the dir:{dire}"])
                                        countWS += 1
                            else:
                                nonmono.append([formula, f"from the dir:{dire}"])
                                tempm,tempS,tempWS = 0,0,0

                            # a, b, c, d = is_monotonic_cnf(formula)
                            # if a and d is not None:
                            #     countM += 1
                            # else:
                            #     nonmono.append(formula)
                    if tempWS == 1 and tempS ==0:
                        print(dire)
                    f.close()
                    os.chdir("..")
                    os.chdir("..")
                    os.chdir("..")
                    os.chdir(path)
                    fm, fs, fws = fm + tempm, fs + tempS, fws + tempWS
os.chdir("..")
os.chdir("..")
lines = [f"Total: {countT} ", f"Monotonic: {countM} ", f"not mono: {nonmono},", f"symmetric: {countS} ",
         f"WS: {countWS}", f"M_models: {fm} ", f"S_models: {fs},", f"nonWS: {nonWS}",f"WS_models: {fws},"]
with open(f"outputws_models.txt", "w") as file:
    # Write each line to the file
    file.writelines("\n".join(lines))
