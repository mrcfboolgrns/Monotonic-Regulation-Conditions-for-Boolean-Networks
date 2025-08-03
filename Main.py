import os
import tkinter as tk
from tkinter import filedialog
from PIL import Image, ImageTk

from GUI import BoolNetworkGUI
from GUI.gui_comps import *

import sys

def main():
    if len(sys.argv) > 1 and sys.argv[1] == "--show-matrix":
        show_interaction_matrix()
        return

    root = tk.Tk()
    root.title("Select a Network by Topology")
    frame = tk.Frame(root)
    frame.pack(padx=10, pady=10)

    mode = tk.StringVar(value="vanilla")
    max_solutions_var = tk.StringVar(value="50")
    nuxmv_path_var = tk.StringVar(value=load_nuxmv_path())

    def browse_nuxmv_path():
        path = filedialog.askopenfilename(
            title="Select NuXmv Executable",
            filetypes=[("Executable Files", "*.exe" if os.name == "nt" else "*")],
        )
        if path:
            nuxmv_path_var.set(path)
            save_nuxmv_path(path)

    nuxmv_frame = tk.Frame(root)
    nuxmv_frame.pack(pady=5)

    tk.Label(nuxmv_frame, text="NuXmv Path:").pack(side=tk.LEFT)
    tk.Entry(nuxmv_frame, textvariable=nuxmv_path_var, width=50).pack(side=tk.LEFT, padx=5)
    tk.Button(nuxmv_frame, text="Browse", command=browse_nuxmv_path).pack(side=tk.LEFT)

    mode_frame = tk.Frame(root)
    mode_frame.pack(pady=10)

    tk.Label(mode_frame, text="Select Mode:").pack(side=tk.LEFT)
    tk.Radiobutton(mode_frame, text="Rein", variable=mode, value="optional").pack(side=tk.LEFT)
    tk.Radiobutton(mode_frame, text="Expanded (Matrix)", variable=mode, value="expanded_huristic").pack(side=tk.LEFT)

    vcmd = (root.register(lambda P: str.isdigit(P) or P == ""), '%P')
    tk.Label(mode_frame, text="Max solutions:").pack(side=tk.LEFT, padx=(10, 0))
    tk.Entry(mode_frame, textvariable=max_solutions_var, validate="key", validatecommand=vcmd, width=6).pack(side=tk.LEFT)

    selected_file = tk.StringVar()

    def open_gui(file):
        match mode.get():
            case "vanilla":
                net = BoolNetwork()
            case "optional":
                net = BoolNetwork()
            case "expanded":
                net = BoolNetwork_Expanded()
            case "expanded_huristic":
                net = BoolNetwork_Expanded_Huristic()

        parse_network(file, net)
        graph_root = tk.Tk()
        app = BoolNetworkGUI(graph_root, net)
        graph_root.mainloop()

    previews_dir = 'previews'
    if not os.path.exists(previews_dir):
        os.makedirs(previews_dir)

    files = [f for f in os.listdir('.') if f.endswith('.txt')]
    files2 = [os.path.join('Networks', k) for k in os.listdir('Networks') if k.endswith('.txt')]
    print(files2)
    files+=files2
    col_count = 3
    row = 0
    col = 0

    for file in files:
        try:
            net = BoolNetwork()
            parse_network(file, net)
            preview_path = os.path.join(previews_dir, f"preview_{file.split("/")[-1]}.png")
            if not render_network_preview(net, preview_path, file):
                continue

            img = Image.open(preview_path)
            img.thumbnail((150, 150))
            tk_img = ImageTk.PhotoImage(img)

            btn = tk.Button(frame, image=tk_img, command=lambda f=file: open_gui(f))
            btn.image = tk_img
            btn.grid(row=row, column=col, padx=5, pady=5)

            label_frame = tk.Frame(frame)
            label_frame.grid(row=row + 1, column=col, padx=5, pady=5)
            tk.Label(label_frame, text=file, font=("Arial", 10)).pack(side=tk.LEFT)
            tk.Radiobutton(label_frame, variable=selected_file, value=file, background=root.cget('bg')).pack(side=tk.RIGHT)

            col += 1
            if col >= col_count:
                col = 0
                row += 2

        except Exception as e:
            print(f"Failed to render {file}: {e}")

    start_button = tk.Button(
        root,
        text="Start Simulation",
        command=lambda: start_simulation(selected_file.get(), mode.get(), root, max_solutions_var, nuxmv_path_var.get())
    )
    start_button.pack(pady=10)

    root.mainloop()

if __name__ == "__main__":
    main()
