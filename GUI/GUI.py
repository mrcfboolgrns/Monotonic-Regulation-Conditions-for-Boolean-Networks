from BoolNet.BoolNetwork import *
import tkinter as tk
from tkinter import ttk
import networkx as nx
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg


class BoolNetworkGUI:
    def __init__(self, root, network):
        self.root = root
        self.network = network
        self.root.title("Boolean Network Topology")

        # Fixed layout for graph
        self.fixed_layout = None

        self.build_gui()

    def build_gui(self):
        # Frames for the layout
        self.frame_left = tk.Frame(self.root, width=200, padx=10, pady=10)
        self.frame_left.pack(side=tk.LEFT, fill=tk.Y)

        self.frame_right = tk.Frame(self.root, padx=10, pady=10)
        self.frame_right.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)

        # List of components
        self.label_components = tk.Label(self.frame_left, text="Components", font=("Arial", 14))
        self.label_components.pack(anchor=tk.W)

        self.listbox_components = tk.Listbox(self.frame_left, height=15, width=25)
        self.listbox_components.pack(anchor=tk.W, pady=5)
        self.populate_components()

        # Buttons for interaction
        self.button_show_both = ttk.Button(self.frame_left, text="Show All Interactions", command=self.show_all_interactions)
        self.button_show_both.pack(anchor=tk.W, pady=5)

        self.button_show_possible = ttk.Button(self.frame_left, text="Show Possible Interactions", command=self.show_possible_interactions)
        self.button_show_possible.pack(anchor=tk.W, pady=5)

        self.button_show_definite = ttk.Button(self.frame_left, text="Show Definite Interactions", command=self.show_definite_interactions)
        self.button_show_definite.pack(anchor=tk.W, pady=5)

        # Canvas for the graph
        self.canvas_frame = tk.Frame(self.frame_right)
        self.canvas_frame.pack(fill=tk.BOTH, expand=True)
        self.fig, self.ax = plt.subplots(figsize=(6, 6))
        self.canvas = FigureCanvasTkAgg(self.fig, self.canvas_frame)
        self.canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)

        # Initialize the fixed layout
        self.initialize_fixed_layout()

        # Initial network rendering
        self.render_network(self.network.definite_interactions,
                            possible_interactions=self.network.possible_interactions, title="All Interactions")

    def initialize_fixed_layout(self):
        """
        Initializes a fixed layout for the graph nodes based on the definite and possible interactions.
        This layout will remain the same across all renderings.
        """
        graph = nx.DiGraph()

        # Add all nodes and edges from both definite and possible interactions
        for src, tgt, _,_ in self.network.definite_interactions + self.network.possible_interactions:
            graph.add_edge(src, tgt)

        # Generate a fixed layout using a consistent seed
        self.fixed_layout = nx.spring_layout(graph, seed=17)

    def populate_components(self):
        for component in self.network.components.keys():
            self.listbox_components.insert(tk.END, component)

    def render_network(self, interactions, possible_interactions=None, title="Network"):
        self.ax.clear()
        graph = nx.DiGraph()

        # Add definite interactions
        for src, tgt, effect,_ in interactions:
            if effect == "positive":
                style = ("green", "solid", "normal")  # Positive definite: solid line with arrowhead
            else:
                style = ("red", "solid", "normal")  # Negative definite: solid line with no arrowhead

            graph.add_edge(src, tgt, color=style[0], style=style[1], arrowstyle=style[2])

        # Add possible interactions
        if possible_interactions:
            for src, tgt, effect,_ in possible_interactions:
                if effect == "positive":
                    style = ("green", (0, (1, 5)), "normal")  # Positive possible: dotted line with arrowhead
                else:
                    style = ("red", (0, (1, 5)), "normal")  # Negative possible: dotted line with no arrowhead

                graph.add_edge(src, tgt, color=style[0], style=style[1], arrowstyle=style[2])

        # Draw nodes
        nx.draw_networkx_nodes(graph, self.fixed_layout, ax=self.ax, node_size=700)

        # Draw edges with styles
        for u, v in graph.edges:
            color = graph[u][v]['color']
            style = graph[u][v]['style']
            arrowstyle = graph[u][v]['arrowstyle']

            nx.draw_networkx_edges(
                graph,
                self.fixed_layout,
                ax=self.ax,
                edgelist=[(u, v)],
                edge_color=color,
                style=style,
                arrowsize=20 if arrowstyle == "normal" else 0,  # Normal arrowhead or no arrowhead
                connectionstyle="arc3,rad=0.2" if (u, v) in graph.edges and (v, u) in graph.edges else "arc3,rad=0",
                # Offset parallel edges
            )
        nx.draw_networkx_labels(graph, self.fixed_layout, ax=self.ax, font_size=10, font_weight="bold")

        self.ax.set_title(title)
        self.canvas.draw()
        # Draw labels
        nx.draw_networkx_labels(graph, self.fixed_layout, ax=self.ax, font_size=10, font_weight="bold")
        self.ax.set_title(title)
        self.canvas.draw()

    def show_possible_interactions(self):
        self.render_network([], possible_interactions=self.network.possible_interactions, title="Possible Interactions")

    def show_definite_interactions(self):
        self.render_network(self.network.definite_interactions, title="Definite Interactions")

    def show_all_interactions(self):
        self.render_network(self.network.definite_interactions, possible_interactions=self.network.possible_interactions, title="All Interactions")

