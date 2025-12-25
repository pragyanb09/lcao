import numpy as np
import plotly.graph_objects as go
import webbrowser

a0 = 1.0

x = np.linspace(-6, 6, 40)
y = np.linspace(-6, 6, 40)
z = np.linspace(-6, 6, 40)


X, Y, Z = np.meshgrid(x, y, z)

R = np.sqrt(X**2 + Y**2 + Z**2)

def psi_2pz(r, z):
    return (1 / (4 * np.sqrt(2 * np.pi)) * (1/a0)**(5/2)) * (z/a0) * np.exp(-r/(2*a0))
    
wf = psi_2pz(R, Z)

prob_density = wf**2

x_flat = X.flatten()
y_flat = Y.flatten()
z_flat = Z.flatten()
prob_flat = prob_density.flatten()

fig = go.Figure(data=go.Isosurface(
    x=x_flat,
    y=y_flat,
    z=z_flat,
    value=prob_flat,
    isomin=0.001,
    isomax=0.001,
    surface_count=1,
    opacity=0.5,
    colorscale='Hot',
    caps=dict(x_show=False, y_show=False, z_show=False),
    showscale=False
))

fig.update_layout(
    title='1s Orbital Isosurface',
    scene=dict(
        xaxis_title='X',
        yaxis_title='Y',
        zaxis_title='Z'
    )
)

"""threshold = 0.01
mask = prob_flat > threshold

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
)"""

fig.update_layout(
    scene=dict(
        xaxis=dict(
            showgrid=False,
            showbackground=False,
            showticklabels=False
        ),
        yaxis=dict(
            showgrid=False,
            showbackground=False,
            showticklabels=False
        ),
        zaxis=dict(
            showgrid=False,
            showbackground=False,
            showticklabels=False
        )
    )
)

"""fig.update_layout(
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
)"""

fig.write_html('p_orbital.html', auto_play=True)

webbrowser.open('p_orbital.html')