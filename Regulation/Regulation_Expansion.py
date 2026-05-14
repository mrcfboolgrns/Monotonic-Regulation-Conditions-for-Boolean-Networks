import pandas as pd
import numpy as np
import itertools


import queue

def generate_perms(mat, blank:list):
    matlist = []
    binary_strings = [''.join(bits) for bits in itertools.product('01', repeat=len(blank))]
    for str in binary_strings:
        temp = mat.copy()
        for i,tup in enumerate(blank):
            temp.at[tup[0],tup[1]] = int(str[i])

        if is_legal(temp):
            matlist.append(temp)
    return matlist
    # if (len(blank) == 0):
    #     self.matrices.append(mat.copy(deep=True))
    #     return
    # temp = blank.pop()
    # i,j = temp[0],temp[1]
    # mat.at[i,j] = 0
    # self.generate_perms(mat,blank)
    # mat.at[i,j] = 1
    # self.generate_perms(mat,blank)


def is_legal(mat):
    counter = 0
    maxOnes = 0

    n,m = mat.shape
    if mat.at[n-1,0]==0:
        return False
    # for i in range(n):
    #     j=0

    add = True
    for i in range(n):#down
        flag = False
        for j in range(m): #left to right
            if(flag and mat.at[i,j]==1):
                add = False

            if(mat.at[i,j] ==1):
                pass
            else:
                flag = True
    for j in range(m):
        flag = False
        for i in range(n):
            if (flag and mat.at[i, j] == 0):
                add = False

            if (mat.at[i, j] == 1):
                flag =True

    return add


def create(n,m):
    ret = pd.DataFrame(0, [i for i in range(3**n)], [i for i in range(3**m)])
    return ret




def run_matrix(n,m,act,rep):
    matrix = create(n,m)
    n,m = matrix.shape
    i=j=0
    blank = []
    blank_mat=[[] for i in range(n)]
    last=()

    flag = False
    while i<n and j<m:
        print(matrix)
        out=(input(f"Run Experiment for (i,j)={act[i],rep[j]}: "))
        if out=='1':
            flag = False
            for k1 in range(i,n):
                for k2 in range(j+1):
                    try:
                        blank.remove((k1,k2))
                        blank_mat[k1].remove(k2)
                    except ValueError:
                        pass
                    matrix.at[k1,k2]=1
            j+=1
        elif out=='0':
            if flag and len(last)==2:
                i,j = last[0]+1,last[1]
                last = ()
                flag=False
            else:
                i+=1
        elif out=="-":
            if not flag:
                last = (i,j)
            flag = True
            blank_mat[i].append(j)
            blank.append((i,j))
            matrix.at[i, j] = ord('-')
            if j<m-1:
                j+=1
            else:
                j = blank_mat[i][0]
                i+=1

    return clear_blank(matrix,blank)


def clear_right_and_up(df):
    df = df.copy()
    rows, cols = df.shape

    zero_positions = [(r, c) for r in range(rows) for c in range(cols) if df.iat[r, c] == 0]

    for r, c in zero_positions:
        df.iloc[r, c:] = 0
        df.iloc[:r+1, c] = 0

    return df

def clear_blank(mat, blank):
    n,m = mat.shape
    temp = blank.copy()
    for x in temp:
        i,j = x[0],x[1]
        if i+1<n and (mat.iloc[i+1:,j]==0).any():# mat.at[i+1,j]==0:
            blank.remove((i,j))
            mat.at[i,j] = 0


    return mat,blank




def run_matrix1(n,m,act,rep):
    matrix = create(n,m)
    n,m = matrix.shape
    i=j=0
    while i<=n-1 and j<=m-1:
        out=int(input(f"Run Experiment for (i,j)={act[i],rep[j]}: "))
        if out==1:
            for k in range(i,n):
                matrix.at[k,j]=1
            j+=1
        else:
            i+=1
    return matrix

def mark_islands(df):
    visited = np.zeros_like(df, dtype=bool)
    rows, cols = df.shape
    labeled_df = df.copy()

    def is_valid_rectangle(r1, c1, r2, c2):
        return df.iloc[r1:r2 + 1, c1:c2 + 1].eq(1).all().all()


    for r in range(rows):
        for c in range(cols):
            if df.iloc[r, c] == 1 and not visited[r, c]:
                # Expand right and down to find the maximum rectangular region
                r2, c2 = r, c
                while r2 + 1 < rows and df.iloc[r2 + 1, c] == 1:
                    r2 += 1
                while c2 + 1 < cols and df.iloc[r, c2 + 1] == 1:
                    c2 += 1

                # Check if the selected area forms a valid rectangle
                if is_valid_rectangle(r, c, r2, c2):
                    # Mark the region as visited
                    visited[r:r2 + 1, c:c2 + 1] = True
                    # Change only the top-rightmost cell to 10
                    labeled_df.iloc[r, c2] = -1
    return labeled_df




def helper(n,flag,arr):
    base_values = ['N', 'E', 'A']
    combinations = list(itertools.product(base_values, repeat=n))
    if(len(arr)!=0):
        dictA = [' & '.join([f'{x}#{arr[i]}#{flag}' for i, x in enumerate(combination)]) for combination in combinations]
    else:
        return ['None']
    return dictA




def startmatrix(arrn, arrm):
    arrn = list(arrn)
    arrm = list(arrm)
    ind_list = []

    if len(arrn) > 1:
        user_input = input("the activator groups are " + str(arrn) + " Enter your preferred order, separated by commas: ")
        priority = user_input.split(',')
        arrn = sorted(arrn, key=lambda x: priority.index(x) if x in priority else len(priority))
    if len(arrm) > 1:
        user_input = input("the repressor groups are " + str(arrm) + " Enter your preferred order, separated by commas: ")
        priority = user_input.split(',')
        arrm = sorted(arrm, key=lambda x: priority.index(x) if x in priority else len(priority))


    if len(arrn) == 0 and len(arrm) == 0:
        return []

    n, m = len(arrn), len(arrm)
    act = helper(n, 'A', arrn)
    rep = helper(m, 'R', arrm)
    mat, blank = run_matrix(n, m, act, rep)
    matlist = generate_perms(mat, blank)

    for mat1 in matlist:
        df = mark_islands(mat1)
        df.index = act
        df.columns = rep
        indices = df[df == -1].stack().index.tolist()

        # --- PROCESS THE INDICES ---
        combined = []
        for i in range(len(indices)):
            base_expr, target = indices[i]
            if "N#" in base_expr:
                # Look for other expressions with the same target that share non-N prefix
                others = []
                for j in range(i + 1, len(indices)):
                    expr2, target2 = indices[j]
                    if target2 == target and expr2.split("#")[0] == base_expr.split("#")[0]:
                        if "N#" not in expr2:
                            others.append(expr2)

                if others:
                    # Combine with OR
                    full_expr = base_expr + " | " + " | ".join(others)
                    combined.append((full_expr, target))
                else:
                    combined.append((base_expr, target))
            else:
                # If not N#, just add
                combined.append((base_expr, target))

        # Remove duplicates and wrap in list for consistency with your original format
        combined = list(dict.fromkeys(combined))
        ind_list.append(combined)
    return noToExist(ind_list)



def noToExist(ind_list):
    ind_list1 = []
    for inx in ind_list:
        inx = list(inx[0])
        temps = []
        for i in range(2):
            reg_lst = inx[i].replace(" ","").split("&")
            starts_n = ["E" + q[1:] for q in reg_lst if q.startswith("N") and q != "None"]
            temp = ""
            for s in starts_n:
                temp += f"{s} | "

            for s in reg_lst:
                if not s.startswith("N") or s == "None":
                    temp += f"{s} & "
            temp = temp[:-3]
            temps.append(temp)
        ind_list1.append([tuple(temps)])

    return ind_list1



if __name__ == '__main__':
    n  = 2
    m = 2
    mat,blank = run_matrix(n,m,range(9),range(9))
    print(mat, blank)


    matlist = generate_perms(mat,blank)

    for m1 in matlist:
        print(m1)
        print("\n")
        print("\n")

    # df = mark_islands(mat)
    # print(df)
    #
    # indices = df[df == -1].stack().index.tolist()
    # print(indices)
