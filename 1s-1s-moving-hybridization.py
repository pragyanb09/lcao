import webbrowser

import numpy as np
import plotly.graph_objects as go

a0 = 1.0

atom_A = np.array([-1, 0, 0])
atom_B = np.array([1, 0, 0])

x = np.linspace(-6, 6, 40)
y = np.linspace(-4, 4, 40)
z = np.linspace(-4, 4, 40)

X, Y, Z = np.meshgrid(x, y, z)


def psi_1s(r):
    """1s orbital wavefunction"""
    return (1 / np.sqrt(np.pi * a0**3)) * np.exp(-r / a0)


def distance_from_orbital(X, Y, Z, orbital_position):
    dx = X - orbital_position[0]
    dy = Y - orbital_position[1]
    dz = Z - orbital_position[2]
    return np.sqrt(dx**2 + dy**2 + dz**2)


def calc_bonding_orbital(sep_dist):
    """calculate bonding orbital for two atoms separated by
    certain distance
    sep_dist: separation distance between atoms"""

    atom_A = np.array([-sep_dist / 2, 0, 0])
    atom_B = np.array([sep_dist / 2, 0, 0])

    r_a = distance_from_orbital(X, Y, Z, atom_A)
    r_b = distance_from_orbital(X, Y, Z, atom_B)

    wf_a = psi_1s(r_a)
    wf_b = psi_1s(r_b)

    wf_bond = wf_a + wf_b
    prob_bond = wf_bond**2

    return prob_bond, atom_A, atom_B


frames = []

x_flat = X.flatten()
y_flat = Y.flatten()
z_flat = Z.flatten()

seps = np.linspace(6, 2, 30)  # 30 frames btwn 6 and 2

for i, sep in enumerate(seps):
    prob, atom_A, atom_B = calc_bonding_orbital(sep)
    prob_flat = prob.flatten()

    frame = go.Frame(
        data=[
            go.Isosurface(
                x=x_flat,
                y=y_flat,
                z=z_flat,
                value=prob_flat,
                isomin=0.001,
                isomax=0.001,
                opacity=0.5,
                colorscale="Blues",
                caps=dict(x_show=False, y_show=False, z_show=False),
                showscale=False,
            ),
            go.Scatter3d(
                x=[atom_A[0], atom_B[0]],
                y=[atom_A[1], atom_B[1]],
                z=[atom_A[2], atom_B[2]],
                mode="markers",
                marker=dict(size=10, color="red"),
                name="Nuclei",
            ),
        ]
    )

    frames.append(frame)

prob_init, a_init, b_init = calc_bonding_orbital(seps[0])
prob_init_flat = prob_init.flatten()

fig = go.Figure(
    data=[
        go.Isosurface(
            x=x_flat,
            y=y_flat,
            z=z_flat,
            value=prob_init_flat,
            isomin=0.001,
            isomax=0.001,
            opacity=0.5,
            colorscale="Blues",
            caps=dict(x_show=False, y_show=False, z_show=False),
            showscale=False,
        ),
        go.Scatter3d(
            x=[a_init[0], b_init[0]],
            y=[a_init[1], b_init[1]],
            z=[a_init[2], b_init[2]],
            mode="markers",
            marker=dict(size=8, color="red"),
            name="Nuclei",
        ),
    ],
    frames=frames,
)

fig.update_layout(
    scene=dict(
        xaxis=dict(showgrid=False, showbackground=False, showticklabels=False),
        yaxis=dict(showgrid=False, showbackground=False, showticklabels=False),
        zaxis=dict(showgrid=False, showbackground=False, showticklabels=False),
        camera=dict(eye=dict(x=2, y=3, z=1)),
    ),
    updatemenus=[
        dict(
            type="buttons",
            showactive=False,
            y=1,
            x=0.8,
            buttons=[
                dict(
                    label="play",
                    method="animate",
                    args=[
                        None,
                        {
                            "frame": {"duration": 100, "redraw": True},
                            "fromcurrent": True,
                            "mode": "immediate",
                        },
                    ],
                )
            ],
        )
    ],
)

fig.write_html("1s-1s-moving-hybridization.html", auto_play=True)
webbrowser.open("1s-1s-moving-hybridization.html")
