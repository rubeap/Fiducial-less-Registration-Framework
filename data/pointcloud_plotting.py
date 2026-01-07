import matplotlib.pyplot as plt
import numpy as np
from mpl_toolkits.mplot3d import Axes3D


def plot_pointcloud(row_subclouds, title):
    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')

    colors = ['red', 'green', 'blue', 'orange', 'purple', 'cyan']

    for i, sub_df in enumerate(row_subclouds):
        ax.scatter(
            sub_df['X'], sub_df['Y'], sub_df['Z'],
            color=colors[i % len(colors)],
            label=f'Offset {i}', s=10
        )

        # Plot the first point of each subcloud in black (larger)
        if not sub_df.empty:
            p = sub_df.iloc[0]
            ax.scatter(
                p['X'], p['Y'], p['Z'],
                color='black', s=40, marker='o',
                edgecolors='white', linewidths=0.5
            )

    # ax.set_xlabel('X')
    # ax.set_ylabel('Y')
    # ax.set_zlabel('Z')
    ax.set_xlim(0.126, 0.287)
    ax.set_ylim(-0.05, 0.05)
    ax.set_zlim(0, 0.139)

    ax.legend()
    ax.set_title(title)
    plt.tight_layout()


def plot_pointcloud_with_lines(row_subclouds, lines, title):
    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')

    colors = ['red', 'green', 'blue', 'orange', 'purple', 'cyan']
    plotted_anything = False  # Flag to check if something was plotted

    for i, (sub_df, (centroid, direction)) in enumerate(zip(row_subclouds, lines)):
        # if i == 0:
        if i != 999:
            # Plot points
            ax.scatter(
                sub_df['X'], sub_df['Y'], sub_df['Z'],
                color=colors[i % len(colors)],
                label=f'Offset {i}', s=10
            )

            # Generate line points
            t = np.linspace(-50, 50, 100)
            x_line = centroid[0] + t * direction[0]
            y_line = centroid[1] + t * direction[1]
            z_line = centroid[2] + t * direction[2]
            ax.plot(x_line, y_line, z_line, color=colors[i % len(colors)], linewidth=2)

            plotted_anything = True

    if plotted_anything:
        # ax.set_xlabel('X')
        # ax.set_ylabel('Y')
        # ax.set_zlabel('Z')
        ax.set_xlim(0.126, 0.287)
        ax.set_ylim(-0.05, 0.05)
        ax.set_zlim(0, 0.139)

        ax.legend()
        ax.set_title(title)
        plt.tight_layout()
    else:
        print("Index 15 was not found in the data.")


def plot_pointcloud_with_lines_and_vectors(row_subclouds, lines, line_vectors_df, title):
    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')

    colors = ['red', 'green', 'blue', 'orange', 'purple', 'cyan']

    for i, (sub_df, (centroid, direction)) in enumerate(zip(row_subclouds, lines)):
        color = colors[i % len(colors)]

        # Plot row points
        ax.scatter(
            sub_df['X'], sub_df['Y'], sub_df['Z'],
            color=color, label=f'Offset {i}', s=10
        )

        # Plot fitted line
        t = np.linspace(-50, 50, 100)
        x_line = centroid[0] + t * direction[0]
        y_line = centroid[1] + t * direction[1]
        z_line = centroid[2] + t * direction[2]
        ax.plot(x_line, y_line, z_line, color=color, linewidth=2)

        # Extract e1, e2, e3 from line_vectors_df
        row = line_vectors_df.iloc[i]
        cx, cy, cz = row[['cx', 'cy', 'cz']]
        e1 = row[['e1x', 'e1y', 'e1z']].to_numpy()
        e2 = row[['e2x', 'e2y', 'e2z']].to_numpy()
        e3 = row[['e3x', 'e3y', 'e3z']].to_numpy()

        # Plot centroid point
        ax.scatter(cx, cy, cz, c='black', marker='o', s=30)

        # Plot vectors as arrows
        ax.quiver(cx, cy, cz, *e1, color='black', length=15, normalize=True)
        ax.quiver(cx, cy, cz, *e2, color='gray', length=15, normalize=True)
        ax.quiver(cx, cy, cz, *e3, color='yellow', length=15, normalize=True)

    # ax.set_xlabel('X')
    # ax.set_ylabel('Y')
    # ax.set_zlabel('Z')

    ax.set_xlim(0.126, 0.287)
    ax.set_ylim(-0.05, 0.05)
    ax.set_zlim(0, 0.139)

    ax.set_title(title)
    ax.legend()
    plt.tight_layout()


def plot_two_pointclouds(row_subclouds_1, row_subclouds_2, title, label_1='CAM', label_2='TVS'):
    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')

    colors = ['red', 'green', 'blue', 'orange', 'purple', 'cyan']

    for i, (df1, df2) in enumerate(zip(row_subclouds_1, row_subclouds_2)):
        color = colors[i % len(colors)]

        # Cloud 1 (e.g., CAM): filled circles
        ax.scatter(
            df1['X'], df1['Y'], df1['Z'],
            color=color, label=f'{label_1} Offset {i}', s=10, marker='o'
        )

        # Cloud 2 (e.g., TVS): hollow circles
        ax.scatter(
            df2['X'], df2['Y'], df2['Z'],
            edgecolors=color, facecolors='none',
            label=f'{label_2} Offset {i}', s=30, marker='o'
        )

    # ax.set_xlabel('X')
    # ax.set_ylabel('Y')
    # ax.set_zlabel('Z')
    ax.set_xlim(0.126, 0.287)
    ax.set_ylim(-0.05, 0.05)
    ax.set_zlim(0, 0.139)

    ax.set_title(title)
    ax.legend()
    plt.tight_layout()
