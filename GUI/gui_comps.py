import os
import tkinter as tk
from tkinter import messagebox, filedialog
from PIL import Image, ImageTk
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

CONFIG_FILE = "Path/nuxmv_path.txt"

def save_nuxmv_path(path):
    with open(CONFIG_FILE, "w") as f:
        f.write(path.strip())

def load_nuxmv_path():
    if os.path.exists(CONFIG_FILE):
        with open(CONFIG_FILE, "r") as f:
            return f.read().strip()
    return ""

def render_network_preview(net, output_path, file_name):
    G = nx.DiGraph()
    for comp in net.components:
        G.add_node(comp)
    for interaction in net.definite_interactions + net.possible_interactions:
        src, tgt, _, _ = interaction
        G.add_edge(src, tgt)

    if G.number_of_nodes() == 0 or G.number_of_edges() == 0:
        return False

    plt.figure(figsize=(2, 2))
    nx.draw(G, with_labels=True, node_color='lightblue', edge_color='gray', node_size=500, font_size=8)
    plt.title(file_name, fontsize=12)
    plt.tight_layout()
    plt.savefig(output_path)
    plt.close()
    return True

def parse_network(file_path, net):
    # file_path = os.path.basename(file_path)
    with open(file_path, "r") as input_file:
        while True:
            line = input_file.readline()
            if not line:
                break
            line = line.strip()
            if line == "" or line == "end":
                continue

            header = "".join(line.split())

            if header.startswith("component{"):
                while True:
                    line = input_file.readline()
                    if not line or line.strip() == "}":
                        break
                    parts = line.strip().split()
                    if len(parts) >= 2:
                        net.add_component(parts[0], parts[-1])

            elif header.startswith("interaction{"):
                while True:
                    line = input_file.readline()
                    if not line or line.strip() == "}":
                        break
                    parts = line.strip().split()
                    if len(parts) >= 3:
                        net.add_interaction(parts)

            elif header.startswith("condition{"):
                while True:
                    line = input_file.readline()
                    if not line or line.strip() == "}":
                        break
                    parts = line.strip().split()
                    if len(parts) >= 2:
                        net.add_condition(parts[:-1], parts[-1])

            elif header.startswith("expression{"):
                while True:
                    line = input_file.readline()
                    if not line or line.strip() == "}":
                        break
                    parts = line.strip().split()
                    if len(parts) == 2:
                        net.add_expression(parts[0], parts[1])

            elif header.startswith("experiment{"):
                tokens = []
                while True:
                    tokens = []
                    line = input_file.readline()
                    if not line:
                        break
                    stripped = line.strip()
                    if stripped == "}":
                        break
                    tokens.extend(stripped.split())
                    if tokens:
                        net.add_experiment(tokens)

def show_interaction_matrix():
    window = tk.Toplevel()
    window.title("Interaction Matrix")
    image_path = "interaction_matrix.png"

    try:
        pil_img = Image.open(image_path)

        width, height = pil_img.size
        pil_img = pil_img.resize((width, height), Image.LANCZOS)

        tk_img = ImageTk.PhotoImage(pil_img)
        label = tk.Label(window, image=tk_img)
        label.pack()
        label.image = tk_img
    except Exception as e:
        messagebox.showerror("Error", f"Failed to load interaction matrix: {e}")
        window.destroy()

def start_simulation(filename, mode, root, max_solutions_var, nuxmv_path):
    if not filename:
        messagebox.showerror("Error", "Please select a file to start the simulation.")
        return

    if not os.path.isfile(nuxmv_path):
        messagebox.showerror("Error", "Please select a valid NuXmv executable path.")
        return

    try:
        max_solutions = int(max_solutions_var.get())
    except ValueError:
        messagebox.showerror("Invalid input", "Max solutions must be an integer.")
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

    smv.num_solutions(max_solutions)
    smv.mode("CTL")
    smv.all_combined()

    python_executable = sys.executable
    script_path = os.path.abspath(__file__)
    subprocess.Popen([python_executable, script_path, "--show-matrix"])

    # disp mat
    show_interaction_matrix()

    messagebox.showinfo("Success", "Simulation completed.")