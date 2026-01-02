import numpy as np
import plotly.graph_objects as go
import webbrowser

a0 = 1.0

x = np.linspace(-20, 20, 50)
y = np.linspace(-20, 20, 50)
z = np.linspace(-20, 20, 50)


X, Y, Z = np.meshgrid(x, y, z)

R = np.sqrt(X**2 + Y**2 + Z**2)

def psi_3dx2y2(x, y, r):
    return (1 / (81 * np.sqrt(np.pi)) * (1/a0)**(7/2)) * ((x**2 - y**2) / (a0**2))* np.exp(-r/(3*a0))
    
wf = psi_3dx2y2(X, Y, R)

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
    isomin=0.00001,
    isomax=0.00001,
    surface_count=1,
    opacity=0.6,
    colorscale='Viridis',
    caps=dict(x_show=False, y_show=False, z_show=False),
    showscale=False
))

fig.update_layout(
    title='d Orbital Isosurface',
    scene=dict(
        xaxis_title='X',
        yaxis_title='Y',
        zaxis_title='Z'
    )
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


fig.write_html('d_orbital.html', auto_play=True)

webbrowser.open('d_orbital.html')