import numpy as np
import plotly.graph_objects as go

a0 = 1.0

atom_A = np.array([-1,0,0])
atom_B = np.array([1,0,0])

x = np.linspace(-5, 5, 40)
y = np.linspace(-5, 5, 40)
z = np.linspace(-5, 5, 40)

X, Y, Z = np.meshgrid(x, y, z)

def psi_1s(r):
    """1s orbital wavefunction"""
    return (1/np.sqrt(np.pi * a0**3)) * np.exp(-r/a0)
    
def distance_from_orbital(X, Y, Z, orbital_position):
    dx = X - orbital_position[0]
    dy = Y - orbital_position[1]
    dz = Z - orbital_position[2]
    return np.sqrt(dx**2 + dy**2 + dz**2)
    
r_a = distance_from_orbital(X, Y, Z, atom_A)
r_b = distance_from_orbital(X, Y, Z, atom_B)

wf_a = psi_1s(r_a)
wf_b = psi_1s(r_b)

wf_bonding = wf_a + wf_b
wf_antibonding = wf_a - wf_b

prob_bonding = wf_bonding**2
prob_antibonding = wf_antibonding**2

x_flat = X.flatten()
y_flat = Y.flatten()
z_flat = Z.flatten()
prob_bonding_flat = prob_bonding.flatten()
prob_antibonding_flat = prob_antibonding.flatten()

fig = go.Figure(data=go.Isosurface(
    x=x_flat,
    y=y_flat,
    z=z_flat,
    value=prob_bonding_flat,
    isomin=0.01,
    isomax=0.1,
    opacity=0.5,
    colorscale="Blues", 
    caps=dict(x_show=False, y_show=False, z_show=False),
    showscale=False
))

fig.add_trace(go.Scatter3d(
    x=[atom_A[0], atom_B[0]],
    y=[atom_A[1], atom_B[1]],
    z=[atom_A[2], atom_B[2]],
    mode='markers',
    marker=dict(size=8, color='red'),
    name='Nuclei'
))

fig.update_layout(
    title="Bonding Orbital",
    scene=dict(
        xaxis=dict(showgrid=False, showbackground=False, showticklabels=False),
        yaxis=dict(showgrid=False, showbackground=False, showticklabels=False),
        zaxis=dict(showgrid=False, showbackground=False, showticklabels=False)
    )
)

frames = []

for angle in range (0, 360, 5):
    frames.append(go.Frame(
        layout=dict(
            scene=dict(
                camera=dict(
                    eye=dict(
                        x=2*np.cos(np.radians(angle)),
                        y=2*np.sin(np.radians(angle)),
                        z=1.5
                    )
                )
            )
        )
    ))
    
fig.frames = frames

fig.update_layout(
    scene_camera=dict(
        eye=dict(x=2, y=0, z=1.5)
    ),
    updatemenus=[dict(
        type="buttons",
        showactive=False,
        y=1,
        x=0.8,
        buttons=[dict(label="Play", method="animate", args=[None, {"frame": {"duration": 50, "redraw": True}, "fromcurrent": True, "mode": "immediate"}])]
    )]
)

fig.show()

fig2 = go.Figure(data=go.Isosurface(
    x=x_flat,
    y=y_flat,
    z=z_flat,
    value=prob_antibonding_flat,
    isomin=0.01,
    isomax=0.01,
    opacity=0.5,
    colorscale="Reds", 
    caps=dict(x_show=False, y_show=False, z_show=False),
    showscale=False
))

fig2.add_trace(go.Scatter3d(
    x=[atom_A[0], atom_B[0]],
    y=[atom_A[1], atom_B[1]],
    z=[atom_A[2], atom_B[2]],
    mode='markers',
    marker=dict(size=8, color='red'),
    name='Nuclei'
))

fig2.update_layout(
    title="Antibonding Orbital",
    scene=dict(
        xaxis=dict(showgrid=False, showbackground=False, showticklabels=False),
        yaxis=dict(showgrid=False, showbackground=False, showticklabels=False),
        zaxis=dict(showgrid=False, showbackground=False, showticklabels=False)
    )
)

frames2 = []

for angle in range (0, 360, 5):
    frames2.append(go.Frame(
        layout=dict(
            scene=dict(
                camera=dict(
                    eye=dict(
                        x=2*np.cos(np.radians(angle)),
                        y=2*np.sin(np.radians(angle)),
                        z=1.5
                    )
                )
            )
        )
    ))
    
fig2.frames = frames2

fig2.update_layout(
    scene_camera=dict(
        eye=dict(x=2, y=0, z=1.5)
    ),
    updatemenus=[dict(
        type="buttons",
        showactive=False,
        y=1,
        x=0.8,
        buttons=[dict(label="Play", method="animate", args=[None, {"frame": {"duration": 50, "redraw": True}, "fromcurrent": True, "mode": "immediate"}])]
    )]
)

fig2.show()
