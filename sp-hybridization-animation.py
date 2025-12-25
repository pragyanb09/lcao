import numpy as np
import webbrowser
import plotly.graph_objects as go

x = np.linspace(-8, 8, 30)
y = np.linspace(-8, 8, 30)
z = np.linspace(-8, 8, 30)

X, Y, Z = np.meshgrid(x, y, z)

R = np.sqrt(X**2 + Y**2 + Z**2)

a0 = 1.0

def psi_1s(r):
    return (1/np.sqrt(np.pi * a0**3)) * np.exp(-r/a0)
    
def psi_2pz(r, z):
    return (1 / (4 * np.sqrt(2 * np.pi)) * (1/a0)**(5/2)) * (z/a0) * np.exp(-r/(2*a0))
    
wf_s = psi_1s(R) #1s orbital wave function
wf_pz = psi_2pz(R, Z) #2pz orbital wave function

def calc_sp_orbital(t):
    """when t = 0: completely separate
    when t = 1: completely hybridized
    because like linear combination of two orbitals (addition
    and adding partials)"""
    
    norm_const = 1/np.sqrt(2)
    
    if t == 0:
        orb1 = wf_s ** 2
        orb2 = wf_pz ** 2
        
    else:
        wf_sp1 = norm_const * (wf_s + t * wf_pz)
        wf_sp2 = norm_const * (wf_s - t * wf_pz)
        
        orb1 = wf_sp1 ** 2
        orb2 = wf_sp2 ** 2
        
    return orb1, orb2

x_flat = X.flatten()
y_flat = Y.flatten()
z_flat = Z.flatten()

mix_vals = np.linspace(0, 1, 30)

frames = []

for i, t in enumerate(mix_vals):
    orb1, orb2 = calc_sp_orbital(t)
    
    prob1_flat = orb1.flatten()
    prob2_flat = orb2.flatten()
    
    frame = go.Frame(
        data=[
            go.Isosurface(
                x=x_flat - 7,
                y=y_flat,
                z=z_flat,
                value=prob1_flat,
                isomin=0.0001,
                isomax=0.0001,
                surface_count=1,
                opacity=0.5,
                colorscale='Blues',
                caps=dict(x_show=False, y_show=False, z_show=False),
                showscale=False
            ),
            
            go.Isosurface(
                x=x_flat + 7,
                y=y_flat,
                z=z_flat,
                value=prob2_flat,
                isomin=0.0001,
                isomax=0.0001,
                surface_count=1,
                opacity=0.5,
                colorscale='Reds',
                caps=dict(x_show=False, y_show=False, z_show=False),
                showscale=False
            )
        ],
        
        name=str(i)
    )
    
    frames.append(frame)