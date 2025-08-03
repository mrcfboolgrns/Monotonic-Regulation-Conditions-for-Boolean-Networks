import matplotlib.pyplot as plt
import numpy as np
import ast

def disp_experiments(data):
    # Flatten the list of lists into a single list of tuples
    flattened_data = [item for sublist in data for item in sublist]

    # Extract rows and time steps from the data
    rows = sorted(set(key for _, states in flattened_data for key in states.keys()))
    time_steps = [time for time, _ in flattened_data]

    # Initialize grid
    num_rows = len(rows)
    num_columns = len(time_steps)
    grid = np.zeros((num_rows, num_columns))

    # Populate the grid
    for col_idx, (time, states) in enumerate(flattened_data):
        for row_idx, row_label in enumerate(rows):
            state = states.get(row_label, '0')
            if state == '1':
                grid[row_idx, col_idx] = 1

    # Create the figure
    fig, ax = plt.subplots(figsize=(max(6, num_columns), max(4, num_rows)))

    # Draw the grid
    for row in range(num_rows):
        for col in range(num_columns):
            color = 'steelblue' if grid[row, col] == 1 else 'white'
            rect = plt.Rectangle((col, num_rows - row - 1), 1, 1, facecolor=color, edgecolor='black')
            ax.add_patch(rect)

    # Add labels
    for col_idx, time in enumerate(time_steps):
        ax.text(col_idx + 0.5, num_rows + 0.2, time, ha='center', va='bottom', fontsize=9)
    for row_idx, row_label in enumerate(rows):
        ax.text(-0.2, num_rows - row_idx - 0.5, row_label, ha='right', va='center', fontsize=9)

    # Configure the plot
    ax.set_xlim(0, num_columns)
    ax.set_ylim(0, num_rows)
    ax.set_xticks([])
    ax.set_yticks([])
    ax.set_aspect('equal')

    # Add legend
    legend_elements = [
        plt.Line2D([0], [0], color='steelblue', lw=4, label='Active (component)'),
        plt.Line2D([0], [0], color='white', lw=4, label='Inactive')
    ]
    ax.legend(handles=legend_elements, loc='upper right', fontsize=8)

    # Show plot
    plt.title("State Transition Visualization")
    plt.savefig("experiment_matrix")
    # plt.show()


def txt_to_mat1(interactions):
    data = []
    print(f"{interactions} inter7")
    with open("test.txt", "r") as f:
        for line in f:
            print(f"line {line}")
            # Convert string representation of list to actual list
            data.append(ast.literal_eval(line.strip()))
    # Extract unique interactions
    print(f"dataaa {data}")
    interactions = sorted(
        # set(
        #     f"{src} --> {dest}" if interaction_type == "positive" else f"{src} --| {dest}"
        #     for step in data
        #     for src, dest, interaction_type in step
        # )
        set(
            f"{l[0]} --> {l[1]}" if l[2] == "positive" else f"{l[0]} --| {l[1]}"
            for step in data
            for l in step
        )
    )

    # Create the interaction matrix
    matrix = np.zeros((len(interactions), len(data)), dtype=int)
    interaction_to_row = {interaction: idx for idx, interaction in enumerate(interactions)}

    # Fill the matrix based on interaction type
    for col, step in enumerate(data):
        for l in step:
            if l[2] == "positive":
                interaction = f"{l[0]} --> {l[1]}"
                row = interaction_to_row[interaction]
                matrix[row, col] = 1  # Positive interactions
            elif l[2] == "negative":
                interaction = f"{l[0]} --| {l[1]}"
                row = interaction_to_row[interaction]
                matrix[row, col] = -1  # Negative interactions
    # for col, step in enumerate(data):
    #     for src, dest, interaction_type in step:
    #         if interaction_type == "positive":
    #             interaction = f"{src} --> {dest}"
    #             row = interaction_to_row[interaction]
    #             matrix[row, col] = 1  # Positive interactions
    #         elif interaction_type == "negative":
    #             interaction = f"{src} --| {dest}"
    #             row = interaction_to_row[interaction]
    #             matrix[row, col] = -1  # Negative interactions

    # Plot the matrix
    fig, ax = plt.subplots(figsize=(10, 6))

    # Define custom colormap
    cmap = plt.cm.colors.ListedColormap(['darkred', 'white', 'darkgreen'])  # Red for -1, White for 0, Green for 1
    bounds = [-1.5, -0.5, 0.5, 1.5]
    norm = plt.cm.colors.BoundaryNorm(bounds, cmap.N)

    ax.imshow(matrix, cmap=cmap, norm=norm, interpolation='nearest')

    # Add labels for rows and columns
    ax.set_xticks(np.arange(matrix.shape[1]))
    ax.set_yticks(np.arange(matrix.shape[0]))
    ax.set_xticklabels([f"{i + 1}" for i in range(matrix.shape[1])], rotation=0)
    ax.set_yticklabels(interactions)

    # Add gridlines
    ax.set_xticks(np.arange(-0.5, matrix.shape[1]), minor=True)
    ax.set_yticks(np.arange(-0.5, matrix.shape[0]), minor=True)
    ax.grid(which="minor", color="black", linestyle='-', linewidth=0.5)
    ax.tick_params(which="minor", bottom=False, left=False)

    # Save and show the plot
    plt.title("Interaction Matrix")
    plt.tight_layout()
    plt.savefig("interaction_matrix.png", dpi=100)  # Save with high resolution
    # plt.show()

    print("Interaction matrix plot saved as 'interaction_matrix.png'")


def txt_to_mat(all_possible_interactions):
    data = []
    with open("test.txt", "r") as f:
        for line in f:
            data.append(ast.literal_eval(line.strip()))

    # Build full interaction strings from full input list (4-tuples)
    all_interaction_labels = sorted(
        f"{src} --> {dest}" if interaction_type == "positive" else f"{src} --| {dest}"
        for src, dest, interaction_type, _strength in all_possible_interactions if src!=dest
    )

    interaction_to_row = {label: i for i, label in enumerate(all_interaction_labels)}

    # Create matrix with shape [#all_possible_interactions x #steps]
    matrix = np.zeros((len(all_interaction_labels), len(data)), dtype=int)

    # Fill matrix using actual data
    for col, step in enumerate(data):
        for src, dest, interaction_type in step:
            label = f"{src} --> {dest}" if interaction_type == "positive" else f"{src} --| {dest}"
            if label in interaction_to_row:
                row = interaction_to_row[label]
                matrix[row, col] = 1 if interaction_type == "positive" else -1

    # Plotting
    fig, ax = plt.subplots(figsize=(10, 6))
    cmap = plt.cm.colors.ListedColormap(['darkred', 'white', 'darkgreen'])
    bounds = [-1.5, -0.5, 0.5, 1.5]
    norm = plt.cm.colors.BoundaryNorm(bounds, cmap.N)

    ax.imshow(matrix, cmap=cmap, norm=norm, interpolation='nearest')

    ax.set_xticks(np.arange(matrix.shape[1]))
    ax.set_yticks(np.arange(matrix.shape[0]))
    ax.set_xticklabels([f"{i + 1}" for i in range(matrix.shape[1])], rotation=0)
    ax.set_yticklabels(all_interaction_labels)

    ax.set_xticks(np.arange(-0.5, matrix.shape[1]), minor=True)
    ax.set_yticks(np.arange(-0.5, matrix.shape[0]), minor=True)
    ax.grid(which="minor", color="black", linestyle='-', linewidth=0.5)
    ax.tick_params(which="minor", bottom=False, left=False)

    plt.title("Interaction Matrix")
    plt.tight_layout()
    plt.savefig("interaction_matrix.png", dpi=100)
    print("Interaction matrix plot saved as 'interaction_matrix.png'")
