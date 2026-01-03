import re
import numpy as np
import plotly.graph_objects as go
import json

a0 = 1.0

x = np.linspace(-10, 10, 15)  
y = np.linspace(-10, 10, 30)
z = np.linspace(-10, 10, 30)
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

original_orbitals = {
    's': {'x': X.flatten().tolist(), 'y': Y.flatten().tolist(), 'z': Z.flatten().tolist(), 'value': (s**2).flatten().tolist()},
    'px': {'x': X.flatten().tolist(), 'y': Y.flatten().tolist(), 'z': Z.flatten().tolist(), 'value': (px**2).flatten().tolist()},
    'py': {'x': X.flatten().tolist(), 'y': Y.flatten().tolist(), 'z': Z.flatten().tolist(), 'value': (py**2).flatten().tolist()},
    'pz': {'x': X.flatten().tolist(), 'y': Y.flatten().tolist(), 'z': Z.flatten().tolist(), 'value': (pz**2).flatten().tolist()},
    'dxy': {'x': X.flatten().tolist(), 'y': Y.flatten().tolist(), 'z': Z.flatten().tolist(), 'value': (dxy**2).flatten().tolist()},
    'dz2': {'x': X.flatten().tolist(), 'y': Y.flatten().tolist(), 'z': Z.flatten().tolist(), 'value': (dz2**2).flatten().tolist()},
    'dx2y2': {'x': X.flatten().tolist(), 'y': Y.flatten().tolist(), 'z': Z.flatten().tolist(), 'value': (dx2y2**2).flatten().tolist()}
}

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
    
# Create the HTML template
html_template = """
<!DOCTYPE html>
<html>
<head>
    <title>Interactive Hybridization Explorer</title>
    <script src="https://cdn.plot.ly/plotly-latest.min.js"></script>
    <style>
        body {
            font-family: Arial, sans-serif;
            max-width: 1200px;
            margin: 0 auto;
            padding: 20px;
            background-color: #f5f5f5;
        }
        .controls {
            background: white;
            padding: 20px;
            border-radius: 8px;
            margin-bottom: 20px;
            box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        }
        select {
            padding: 10px;
            font-size: 16px;
            margin: 0 10px;
            border-radius: 4px;
            border: 2px solid #3498db;
        }
        label {
            font-weight: bold;
            margin-right: 5px;
        }
        #plot {
            background: white;
            border-radius: 8px;
            box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        }
        h1 {
            color: #2c3e50;
        }
        .info {
            background: #e8f4f8;
            padding: 15px;
            border-radius: 4px;
            margin-top: 20px;
            border-left: 4px solid #3498db;
        }
    </style>
</head>
<body>
    <h1>Interactive Hybridization Explorer</h1>
    
    <div class="controls">
        <label>Period:</label>
        <select id="periodSelect" onchange="updateHybridOptions()">
            <option value="period2">Period 2 (C, N, O, F)</option>
            <option value="period3">Period 3+ (P, S, Cl, etc.)</option>
        </select>
        
        <label>Hybridization:</label>
        <select id="hybridSelect" onchange="updateVisualization()">
            <option value="sp">sp (linear)</option>
            <option value="sp2">sp² (trigonal planar)</option>
            <option value="sp3">sp³ (tetrahedral)</option>
        </select>
    </div>
    
    <div id="plot"></div>
    
    <div class="info" id="info"></div>
    
    <script>
        // Embedded data
        const data = HYBRIDIZATION_DATA_PLACEHOLDER;
        
        const period2Options = [
            {value: "sp", text: "sp (linear)"},
            {value: "sp2", text: "sp² (trigonal planar)"},
            {value: "sp3", text: "sp³ (tetrahedral)"}
        ];
        
        const period3Options = [
            {value: "sp", text: "sp (linear)"},
            {value: "sp2", text: "sp² (trigonal planar)"},
            {value: "sp3", text: "sp³ (tetrahedral)"},
            {value: "sp3d", text: "sp³d (trigonal bipyramidal)"},
            {value: "sp3d2", text: "sp³d² (octahedral)"}
        ];
        
        function updateHybridOptions() {
            const period = document.getElementById('periodSelect').value;
            const hybridSelect = document.getElementById('hybridSelect');
            
            hybridSelect.innerHTML = '';
            const options = period === 'period2' ? period2Options : period3Options;
            
            options.forEach(opt => {
                const option = document.createElement('option');
                option.value = opt.value;
                option.text = opt.text;
                hybridSelect.appendChild(option);
            });
            
            updateVisualization();
        }
        
        function updateVisualization() {
            const hybridType = document.getElementById('hybridSelect').value;
            const hybrids = data.hybrids[hybridType];
            const originals = data.originals;
            
            // Determine which original orbitals to show based on hybrid type
            const orbitalsToShow = {
                'sp': ['s', 'pz'],
                'sp2': ['s', 'px', 'py'],
                'sp3': ['s', 'px', 'py', 'pz'],
                'sp3d': ['s', 'px', 'py', 'pz', 'dz2'],
                'sp3d2': ['s', 'px', 'py', 'pz', 'dz2', 'dx2y2']
            };
            
            const traces = [];
            
            // First, add the ORIGINAL orbitals (lighter, more transparent)
            const originalColors = {
                's': 'Greys',
                'px': 'Blues', 
                'py': 'Reds',
                'pz': 'Greens',
                'dxy': 'Purples',
                'dz2': 'Oranges',
                'dx2y2': 'YlOrRd'
            };
            
            orbitalsToShow[hybridType].forEach(orbitalName => {
                const orbital = originals[orbitalName];
                traces.push({
                    type: 'isosurface',
                    x: orbital.x,
                    y: orbital.y,
                    z: orbital.z,
                    value: orbital.value,
                    isomin: 0.0001,
                    isomax: 0.0001,
                    colorscale: originalColors[orbitalName],
                    opacity: 0.2,  // Very transparent
                    caps: {x: {show: false}, y: {show: false}, z: {show: false}},
                    showscale: false,
                    name: orbitalName
                });
            });
            
            // Then add the HYBRID orbitals (more opaque, brighter)
            const hybridColors = ['Plasma', 'Viridis', 'Cividis', 'Inferno'];
            
            hybrids.forEach((hybrid, i) => {
                traces.push({
                    type: 'isosurface',
                    x: hybrid.x,
                    y: hybrid.y,
                    z: hybrid.z,
                    value: hybrid.value,
                    isomin: 0.0001,
                    isomax: 0.0001,
                    colorscale: hybridColors[i % hybridColors.length],
                    opacity: 0.7,  // More opaque
                    caps: {x: {show: false}, y: {show: false}, z: {show: false}},
                    showscale: false,
                    name: 'Hybrid ' + (i+1)
                });
            });
            
            // Add nucleus
            traces.push({
                type: 'scatter3d',
                x: [0],
                y: [0],
                z: [0],
                mode: 'markers',
                marker: {size: 10, color: 'black'},
                name: 'Nucleus'
            });
            
            const layout = {
                scene: {
                    xaxis: {showgrid: false, showbackground: false, showticklabels: false},
                    yaxis: {showgrid: false, showbackground: false, showticklabels: false},
                    zaxis: {showgrid: false, showbackground: false, showticklabels: false},
                    camera: {eye: {x: 1.5, y: 1.5, z: 1.2}}
                },
                showlegend: false,
                margin: {l: 0, r: 0, t: 0, b: 0}
            };
            
            Plotly.newPlot('plot', traces, layout);
            
            // Update info
            const info = {
                'sp': 'Combining s and pz → Two sp hybrid orbitals (linear, 180°)',
                'sp2': 'Combining s, px, py → Three sp² hybrid orbitals (trigonal planar, 120°)',
                'sp3': 'Combining s, px, py, pz → Four sp³ hybrid orbitals (tetrahedral, 109.5°)',
                'sp3d': 'Combining s, p, and d orbitals → Five sp³d hybrid orbitals (trigonal bipyramidal)',
                'sp3d2': 'Combining s, p, and d orbitals → Six sp³d² hybrid orbitals (octahedral)'
            };
            document.getElementById('info').innerHTML = `<strong>${hybridType}:</strong> ${info[hybridType]}`;
        }
        
        // Initial visualization
        updateVisualization();
    </script>
</body>
</html>
"""

# Replace placeholder with actual data
# Create combined data object
all_data = {
    'hybrids': hybridization_data,
    'originals': original_orbitals
}

html_content = html_template.replace(
    'HYBRIDIZATION_DATA_PLACEHOLDER',
    json.dumps(all_data)
)

# Write to file
with open('hybridization_builder.html', 'w') as f:
    f.write(html_content)
