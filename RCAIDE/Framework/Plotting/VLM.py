import numpy as np
import jax.numpy as jnp
import plotly.graph_objects as go

def plot_vlm_panels(VD, panel_values=None, title="VLM Panelization"):
    """
    Plots a 3D interactive mesh of the VLM panels with an optional heatmap.
    If no panel_values are provided, displays light grey panels with black edges.
    """
    panel_vertices = np.asarray(VD.panel_vertices)

    if panel_values is not None:
        panel_values = np.asarray(panel_values)

    x, y, z = [], [], []
    i_idx, j_idx, k_idx = [], [], []
    facecolor_intensities = []
    
    # Lists to hold the wireframe boundary lines
    edge_x, edge_y, edge_z = [], [], []

    v_count = 0
    # Iterate through each panel to build the vertex, triangle, and edge arrays
    for idx, panel in enumerate(panel_vertices):
        # Flatten the coordinates for the Mesh3d
        x.extend(panel[:, 0])
        y.extend(panel[:, 1])
        z.extend(panel[:, 2])

        # Split the quad into Triangle 1 (Vertices 0, 1, 2)
        i_idx.append(v_count)
        j_idx.append(v_count + 1)
        k_idx.append(v_count + 2)

        # Split the quad into Triangle 2 (Vertices 0, 2, 3)
        i_idx.append(v_count)
        j_idx.append(v_count + 2)
        k_idx.append(v_count + 3)

        if panel_values is not None:
            # Both triangles making up this panel get the same intensity value
            facecolor_intensities.extend([panel_values[idx], panel_values[idx]])

        # Build the black boundary lines (close the loop by returning to vertex 0)
        # Adding None at the end breaks the line before the next panel begins
        edge_x.extend([panel[0, 0], panel[1, 0], panel[2, 0], panel[3, 0], panel[0, 0], None])
        edge_y.extend([panel[0, 1], panel[1, 1], panel[2, 1], panel[3, 1], panel[0, 1], None])
        edge_z.extend([panel[0, 2], panel[1, 2], panel[2, 2], panel[3, 2], panel[0, 2], None])

        # Increment vertex counter by 4 for the next panel
        v_count += 4

    # Build the 3D Mesh
    mesh_trace = go.Mesh3d(
        x=x, y=y, z=z,
        i=i_idx, j=j_idx, k=k_idx,
        intensity=facecolor_intensities if panel_values is not None else None,
        intensitymode='cell',
        colorscale='Plasma',  
        color='lightgrey',  # Fallback color changed to light grey
        showscale=panel_values is not None,
        flatshading=True,
        name='VLM Mesh',
        hovertemplate='Value: %{intensity:.5f}<extra></extra>' if panel_values is not None else None
    )
    
    data = [mesh_trace]

    # If no values are passed, overlay the black wireframe
    if panel_values is None:
        edge_trace = go.Scatter3d(
            x=edge_x, y=edge_y, z=edge_z,
            mode='lines',
            line=dict(color='black', width=2),
            name='Panel Edges',
            hoverinfo='skip'  # Don't clutter the hover box with line coordinates
        )
        data.append(edge_trace)

    fig = go.Figure(data=data)

    # Define the isometric camera
    isometric_camera = dict(
        up=dict(x=0, y=0, z=1),  
        center=dict(x=0, y=0, z=0),  
        eye=dict(x=1.5, y=-1.5, z=1.5),  
        projection=dict(type='orthographic')  
    )

    # Apply the styling and camera to the layout
    fig.update_layout(
        title=title,
        template='plotly_white',  
        scene=dict(
            aspectmode='data',  
            camera=isometric_camera,
            xaxis=dict(title='X (Streamwise)', showbackground=False),
            yaxis=dict(title='Y (Spanwise)', showbackground=False),
            zaxis=dict(title='Z (Vertical)', showbackground=False)
        ),
        margin=dict(l=0, r=0, b=0, t=40)
    )

    return fig