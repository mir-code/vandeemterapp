import streamlit as st
import numpy as np
import plotly.graph_objects as go
import plotly.express as px

# --- Streamlit App Setup ---
st.set_page_config(
    page_title="Visualisierung der Van-Deemter-Gleichung",
    layout="wide",
    initial_sidebar_state="expanded"
)

st.title("🔬 Visualisierung der Van-Deemter-Gleichung")
st.markdown("""
_Ein interaktives Werkzeug zur Untersuchung der Faktoren, die die chromatographische Effizienz beeinflussen._
""")

# --- Sidebar Controls ---
st.sidebar.header("Parameter anpassen")
st.sidebar.markdown("Verwende die Schieberegler, um die Koeffizienten der Van-Deemter-Gleichung zu ändern.")

# Sliders for the Van Deemter coefficients
A = st.sidebar.slider(
    'A: Eddy-Diffusion',
    min_value=0.0, max_value=2.0, value=0.5, step=0.01,
    help="Die Eddy-Diffusion ist unabhängig von der Flussrate. Ein höherer Wert erhöht H bei allen Flussraten."
)
B = st.sidebar.slider(
    'B: Longitudinale Diffusion',
    min_value=0.0, max_value=1.0, value=0.1, step=0.01,
    help="Die longitudinale Diffusion ist umgekehrt proportional zur Flussrate. Dieser Term dominiert bei niedrigen Flussraten."
)
C = st.sidebar.slider(
    'C: Massentransfer',
    min_value=0.0, max_value=0.1, value=0.01, step=0.001,
    help="Der Massentransfer ist direkt proportional zur Flussrate. Dieser Term dominiert bei hohen Flussraten."
)

# Slider for the current flow rate
current_u = st.sidebar.slider(
    'u: Lineare Flussrate (cm/s)',
    min_value=1, max_value=200, value=50, step=1,
    help="Die lineare Flussrate der mobilen Phase."
)

# --- Van Deemter Equation Logic ---
def van_deemter(u, A, B, C):
    """Calculates plate height (H) based on the Van Deemter equation."""
    return A + B / u + C * u

# Create a range of flow rates for plotting
u_values = np.linspace(1, 200, 400)
H_values = van_deemter(u_values, A, B, C)

# Find the optimal flow rate (u_opt) and minimum plate height (H_min)
H_min = np.min(H_values)
u_opt = u_values[np.argmin(H_values)]

# Calculate the plate height for the user's selected flow rate
H_current = van_deemter(current_u, A, B, C)

# --- Plotting the Curve with Plotly ---
fig = go.Figure()

# Plot the main Van Deemter curve
fig.add_trace(go.Scatter(
    x=u_values,
    y=H_values,
    mode='lines',
    name=f'H = {A} + {B}/u + {C}*u',
    line=dict(color='#4f46e5', width=2)
))

# Highlight the optimal point (minimum H)
fig.add_trace(go.Scatter(
    x=[u_opt],
    y=[H_min],
    mode='markers',
    marker=dict(color='red', size=12, symbol='circle'),
    name=f'Optimal: u={u_opt:.2f}, H={H_min:.2f}'
))

# Highlight the user's selected flow rate
fig.add_trace(go.Scatter(
    x=[current_u],
    y=[H_current],
    mode='markers',
    marker=dict(color='blue', size=12, symbol='circle'),
    name=f'Ausgewählt: u={current_u:.2f}, H={H_current:.2f}'
))

# Update plot layout
fig.update_layout(
    title_text="Van-Deemter-Diagramm",
    title_font_size=20,
    xaxis_title="Lineare Flussrate (u)",
    yaxis_title="Bodenhöhe (H)",
    xaxis=dict(gridcolor='#e5e7eb'),
    yaxis=dict(gridcolor='#e5e7eb'),
    hovermode='closest'
)

# axes label sizes
fig.update_xaxes(tickfont=dict(size=18), title_font=dict(size=20))
fig.update_yaxes(tickfont=dict(size=18), title_font=dict(size=20))

# Display the plot in Streamlit
st.plotly_chart(fig, use_container_width=True)

# --- Display Results ---
st.subheader("Wichtige Erkenntnisse")
st.info(f"""
- **Van-Deemter-Gleichung:** $H = A + B/u + C \cdot u$
- **Optimale Flussrate ($u_{{opt}}$):** Die Flussrate, bei der die chromatographische Effizienz maximiert (die Bodenhöhe minimiert) wird.
- **Aktuelle Parameter:**
    - Eddy-Diffusion (A): **{A}**
    - Longitudinale Diffusion (B): **{B}**
    - Massentransfer (C): **{C}**
- **Optimale Werte aus dem Diagramm:**
    - Optimale Flussrate: **{u_opt:.2f}**
    - Minimale Bodenhöhe: **{H_min:.2f}**
- **Ausgewählter Punkt:**
    - Lineare Flussrate: **{current_u}**
    - Berechnete Bodenhöhe: **{H_current:.2f}**
""")