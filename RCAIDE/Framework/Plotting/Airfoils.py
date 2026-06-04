import plotly.graph_objects as go
import numpy as np


def plot_airfoil(airfoil, show_markers=False, show_camber=False):
    """
    Plots the Airfoil class geometry using Plotly.
    Enforces a 1:1 aspect ratio so the thickness and camber are visually accurate.
    """
    # Plotly expects standard numpy arrays, so we safely cast the JAX arrays
    x_up = np.asarray(airfoil.x_upper_surface)
    y_up = np.asarray(airfoil.y_upper_surface)

    x_low = np.asarray(airfoil.x_lower_surface)
    y_low = np.asarray(airfoil.y_lower_surface)

    mode = 'lines+markers' if show_markers else 'lines'

    fig = go.Figure()

    # Upper Surface
    fig.add_trace(go.Scatter(
        x=x_up,
        y=y_up,
        mode=mode,
        name='Upper Surface',
        line=dict(color='blue', width=2),
        marker=dict(size=4)
    ))

    # Lower Surface
    fig.add_trace(go.Scatter(
        x=x_low,
        y=y_low,
        mode=mode,
        name='Lower Surface',
        line=dict(color='red', width=2),
        marker=dict(size=4)
    ))

    # Camber Line
    if show_camber:
        # Note: Using x_lower_surface per your request, though if the array sizes
        # differ, you might need to interpolate or use airfoil.x_coordinates
        camber_y = np.asarray(airfoil.camber)
        fig.add_trace(go.Scatter(
            x=x_low,
            y=camber_y,
            mode=mode,
            name='Camber Line',
            line=dict(color='green', width=2, dash='dash'),
            marker=dict(size=4, symbol='cross')
        ))

    # Layout: The 1:1 aspect ratio is mandatory for airfoil visualization
    fig.update_layout(
        title=f"Airfoil Geometry Inspection: {airfoil.tag}",
        xaxis_title="x/c",
        yaxis_title="y/c",
        yaxis=dict(
            scaleanchor="x",
            scaleratio=1,
            zeroline=True,
            zerolinecolor='lightgrey'
        ),
        xaxis=dict(
            zeroline=True,
            zerolinecolor='lightgrey'
        ),
        hovermode="x unified",
        template="plotly_white",
        legend=dict(yanchor="top", y=0.99, xanchor="right", x=0.99)
    )

    fig.show()