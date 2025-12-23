import numpy as np
import webbrowser
import plotly.graph_objects as go

x = np.linspace(-8, 8, 30)
y = np.linspace(-8, 8, 30)
z = np.linspace(-8, 8, 30)

X, Y, Z = np.meshgrid(x, y, z)

R = np.sqrt(X**2 + Y**2 + Z**2)

a0 = 1.0
prob_density = np.exp(-R / a0)

#print(X.shape)

x_flat = X.flatten()
y_flat = Y.flatten()
z_flat = Z.flatten()
prob_flat = prob_density.flatten()

fig = go.Figure(data=go.Isosurface(
    x=x_flat,
    y=y_flat,
    z=z_flat,
    value=prob_flat,
    isomin=0.005,
    isomax=0.005,
    surface_count=1,
    opacity=0.4,
    #colorscale='Hot',
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

threshold = 0.01
mask = prob_flat > threshold

"""fig.add_trace(go.Scatter3d(
    x=x_flat[mask],
    y=y_flat[mask],
    z=z_flat[mask],
    mode='markers',
    marker=dict(
        size=2,
        color=prob_flat[mask],
        colorscale='Hot',
        opacity=0.1
    )
))"""

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

fig.write_html('1s_orbital_isosurface.html', auto_play=True)

#fig.show()
webbrowser.open('1s_orbital_isosurface.html')