import os
import networkx as nx
import matplotlib.pyplot as plt
import sys
import subprocess

# from BoolNet.BoolNetwork import BoolNetwork
# from BoolNet.BoolNetwork_Expanded import BoolNetwork_Expanded
# from BoolNet.BoolNetwork_Expanded_Huristic import BoolNetwork_Expanded_Huristic
# from ToSmv.ToSmv_Expanded import ToSmv_Expanded
# from ToSmv.ToSmv_Expanded_Huristic import ToSmv_Expanded_Huristic
# from ToSmv.ToSmv_Improved_Optional import ToSmv_Improved_Optional
# from ToSmv.ToSmv_Improved import ToSmv_Improved
# import testingZ3
import utilsZ3
import copy
import Regulation.Regulation_Expansion as reg_exp

# from GUI.gui_comps import parse_network

def start_simulation(filename, mode, max_solutions):

    if not os.path.isfile(filename):
        print(f"Error: '{filename}' is not a valid file. Please select a file to start the simulation.")
        return
    
    if not filename.endswith('.bnet'):
        print(f"Error: '{filename}' is not a valid .bnet file. Please select a valid file to start the simulation.")
        return
    
    if max_solutions <= 0:
        print("Error: Max solutions must be a positive integer.")
        return

    print(f"Starting simulation with: {filename} in {mode} mode, max_solutions={max_solutions}")
    '''
    Here we are supposed to have the interaction with the simulator.
    Instead of the following section.
    '''
    # Read filename and extract the Boolean formula for the target component
    # split second line by comma and extract the right-hand side (the Boolean formula)
    with open(filename, 'r') as f:
        content = f.readlines()
        target_component, formula = content[1].strip().split(',')
        acceptors, repressors = utilsZ3.extract_variables_mono(formula)
        variables = copy.deepcopy(acceptors)
        variables.update(repressors)
        
        output = reg_exp.startmatrix(None, None, target_component=target_component, formula=formula, variables=variables)

        print("Simulation Output:")
        for row in output:
            print(row)
        # Convert input_expr to Z3 Boolean expression
        # expr = utilsZ3.parse_expression(formula, variables)


        # a = testingZ3.check_WS(formula)
        # target_dictionary = {
        #     "WA": a.get("WA"),
        #     "SA": a.get("SA"),
        #     "WR": a.get("WR"),
        #     "SR": a.get("SR")
        # }
        
    