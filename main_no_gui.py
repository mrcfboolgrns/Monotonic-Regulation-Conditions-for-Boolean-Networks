from GUI import BoolNetworkGUI
from GUI.gui_comps import *

import sys


def main():
    if len(sys.argv) > 1 and sys.argv[1] == "--show-matrix":
        show_interaction_matrix()
        return

    topology = "C OR (A AND B).txt"
    if sys.argv[2] is not None:
        mode= sys.argv[2]
    else:
        mode= "vanilla"
    max_solutions_var = sys.argv[3]
    mode = tk.StringVar(value="vanilla")
    max_solutions = 50
    nuxmv_path = "//madrid.eng.biu.ac.il/e2019/gerbery1/My Documents/nuXmv-2.1.0-win64/bin/nuXmv.exe"




    def open(file):
        match mode:
            case "vanilla":
                net = BoolNetwork()
            case "optional":
                net = BoolNetwork()
            case "expanded":
                net = BoolNetwork_Expanded()
            case "expanded_huristic":
                net = BoolNetwork_Expanded_Huristic()

        parse_network(file, net)

    previews_dir = 'previews'
    if not os.path.exists(previews_dir):
        os.makedirs(previews_dir)

    files = [f for f in os.listdir('.') if f.endswith('.txt')]
    files2 = [os.path.join('Networks', k) for k in os.listdir('Networks') if k.endswith('.txt')]
    print(files2)
    files += files2
    col_count = 3
    row = 0
    col = 0

    for file in files:
        try:
            net = BoolNetwork()
            parse_network(file, net)
            preview_path = os.path.join(previews_dir, f"preview_{file.split(os.path.sep)[-1]}.png")
            if not render_network_preview(net, preview_path, file):
                continue

            img = Image.open(preview_path)
            img.thumbnail((150, 150))
            tk_img = ImageTk.PhotoImage(img)

            open(file)


            label_frame = tk.Frame(frame)
            label_frame.grid(row=row + 1, column=col, padx=5, pady=5)
            tk.Label(label_frame, text=file, font=("Arial", 10)).pack(side=tk.LEFT)
            tk.Radiobutton(label_frame, variable=selected_file, value=file, background=root.cget('bg')).pack(
                side=tk.RIGHT)

            col += 1
            if col >= col_count:
                col = 0
                row += 2

        except Exception as e:
            print(f"Failed to render {file}: {e}")

    start_button = tk.Button(
        root,
        text="Start Simulation",
        command=lambda: start_simulation(selected_file.get(), mode.get(), root, max_solutions_var,
                                         nuxmv_path_var.get()))


if __name__ == "__main__":
    main()
