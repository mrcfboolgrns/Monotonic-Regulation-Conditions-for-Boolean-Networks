import os
import networkx as nx
import matplotlib.pyplot as plt
import sys
import subprocess

from BoolNet.BoolNetwork import BoolNetwork
from BoolNet.BoolNetwork_Expanded import BoolNetwork_Expanded
from BoolNet.BoolNetwork_Expanded_Huristic import BoolNetwork_Expanded_Huristic
from ToSmv.ToSmv_Expanded import ToSmv_Expanded
from ToSmv.ToSmv_Expanded_Huristic import ToSmv_Expanded_Huristic
from ToSmv.ToSmv_Improved_Optional import ToSmv_Improved_Optional
from ToSmv.ToSmv_Improved import ToSmv_Improved

from GUI.gui_comps import parse_network

def start_simulation(filename, mode, max_solutions):

    if not os.path.isfile(filename):
        print(f"Error: '{filename}' is not a valid file. Please select a file to start the simulation.")
        return
    
    if max_solutions <= 0:
        print("Error: Max solutions must be a positive integer.")
        return
    
    if mode not in ["vanilla", "optional", "expanded", "expanded_huristic"]:
        print("Error: Invalid mode selected. Please choose from 'vanilla', 'optional', 'expanded', or 'expanded_huristic'.")
        return

    print(f"Starting simulation with: {filename} in {mode} mode, max_solutions={max_solutions}")
    net = None
    match mode:
        case "vanilla":
            net = BoolNetwork()
        case "optional":
            net = BoolNetwork()
        case "expanded":
            net = BoolNetwork_Expanded()
        case "expanded_huristic":
            net = BoolNetwork_Expanded_Huristic()

    parse_network(filename, net)
    net.perm_interactions = net.generate_permutations()
    net.printall()
    net.print_interactions()

    if mode == "vanilla":
        smv = ToSmv_Improved(net)
    elif mode == "optional":
        smv = ToSmv_Improved_Optional(net)
    elif mode == "expanded_huristic":
        smv = ToSmv_Expanded_Huristic(net)
    else:
        smv = ToSmv_Expanded(net)

    '''
    Here we are supposed to have the interaction with the simulator.
    Instead of the following section.
    '''
    smv.num_solutions(max_solutions)
    smv.mode("CTL")
    smv.all_combined()

    '''Still working on all_combined'''
    
    python_executable = sys.executable
    script_path = os.path.abspath(__file__)
    subprocess.Popen([python_executable, script_path, "--show-matrix"])

    # disp mat
    # show_interaction_matrix()

    # messagebox.showinfo("Success", "Simulation completed.")