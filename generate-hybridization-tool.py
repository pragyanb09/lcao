import re
import numpy as np
import plotly.graph_objects as go
import json

a0 = 1.0

x = np.linspace(-25, 25, 50)  
y = np.linspace(-25, 25, 50)
z = np.linspace(-25, 25, 50)
X, Y, Z = np.meshgrid(x, y, z)
R = np.sqrt(X**2 + Y**2 + Z**2)

def psi_2s(r):
    return (1/np.sqrt(np.pi)) * (1/a0)**(3/2) * np.exp(-r/a0)
    
def psi_2px(r, x):
    return (1 / (4 * np.sqrt(2 * np.pi)) * (1/a0)**(5/2)) * (x/a0) * np.exp(-r/(2*a0))
def psi_2py(r, y):
    return (1 / (4 * np.sqrt(2 * np.pi)) * (1/a0)**(5/2)) * (y/a0) * np.exp(-r/(2*a0))
    
def psi_2pz(r, z):
    return (1 / (4 * np.sqrt(2 * np.pi)) * (1/a0)**(5/2)) * (z/a0) * np.exp(-r/(2*a0))
    
def psi_3dxy(r, x, y):
    return (1 / (81 * np.sqrt(np.pi)) * (1/a0)**(7/2)) * (x * y) / (a0**2) * np.exp(-r/(3*a0))
    
def psi_3dz2(x, y, z, r):
    return (1 / (81 * np.sqrt(6 * np.pi)) * (1/a0)**(7/2)) * ((2*z**2 - x**2 - y**2) / (a0**2)) * np.exp(-r/(3*a0))
    
def psi_3dx2y2(x, y, r):
    return (1 / (81 * np.sqrt(np.pi)) * (1/a0)**(7/2)) * ((x**2 - y**2) / (a0**2)) * np.exp(-r/(3*a0))

s = psi_2s(R)
px = psi_2px(R, X)
py = psi_2py(R, Y)
pz = psi_2pz(R, Z)
dxy = psi_3dxy(R, X, Y)
dz2 = psi_3dz2(X, Y, Z, R)
dx2y2 = psi_3dx2y2(X, Y, R)


def calculate_hybridization(hybrid_type):
    """calculate the probabilty distribution function
    given the hybrid type"""
    
    hybrids = []
    
    if hybrid_type == "sp":
        sp = (1 / np.sqrt(2)) * (s + pz)
        hybrids = [sp**2]
        
    elif hybrid_type == "sp2":
        sp2 = (1/np.sqrt(3)) * (s + np.sqrt(2) * px)
        hybrids = [sp2**2]
        
    elif hybrid_type == "sp3":
        sp3 = (1/2) * (s + px + py + pz)
        hybrids = [sp3**2]
        
    elif hybrid_type == "sp3d":
        sp3d = (1/np.sqrt(5)) * (s + px + py + pz + dz2)
        hybrids = [sp3d**2]
        
    elif hybrid_type == "sp3d2":
        sp3d2 = (1/np.sqrt(6)) * (s + px + py + pz + dz2 + dx2y2)
        hybrids = [sp3d2**2]
    
    return hybrids

hybridization_data = {}

period2 = ["sp", "sp2", "sp3"]
period3 = ["sp", "sp2", "sp3", "sp3d", "sp3d2"]

for hybrid_type in period3:
    hybrids = calculate_hybridization(hybrid_type)
    
    orbital_data = []
    
    for i, hybrid in enumerate(hybrids):
        orbital_data.append({
            'x': X.flatten().tolist(),
            'y': Y.flatten().tolist(),
            'z': Z.flatten().tolist(),
            'value': hybrid.flatten().tolist()
        })

    hybridization_data[hybrid_type] = orbital_data
    
    