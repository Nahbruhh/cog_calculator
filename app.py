import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
import os

def compute_global_cog(elements):
    total_mass = sum(m for _, _, _, m in elements)
    if total_mass == 0:
        return (None, None, None)
    
    weighted_x = sum(x * m for x, _, _, m in elements)
    weighted_y = sum(y * m for _, y, _, m in elements)
    weighted_z = sum(z * m for _, _, z, m in elements)
    
    return (float(weighted_x / total_mass), float(weighted_y / total_mass), float(weighted_z / total_mass))
st.set_page_config(
    page_title="Global Center of Gravity Calculator",
    page_icon=os.path.join("assets", "logo.png"),
)

st.title("Global Center of Gravity Calculator")
with st.expander("Connect with Me"):
        st.markdown("""
                    **Author**: Copyright (c) **Nguyen Manh Tuan**
    <style>
        .social-buttons img {
            transition: opacity 0.3s;
        }
        .social-buttons img:hover {
            opacity: 0.7;
        }
    </style>
    <div class="social-buttons" style="display: flex; gap: 20px; align-items: center;">
        <a href="https://github.com/Nahbruhh" target="_blank">
            <img src="https://github.githubassets.com/images/modules/logos_page/GitHub-Mark.png" width="40">
        </a>
        <a href="https://www.linkedin.com/in/manh-tuan-nguyen19/" target="_blank">
            <img src="https://upload.wikimedia.org/wikipedia/commons/8/81/LinkedIn_icon.svg" width="30">
        </a>
    </div>
""", unsafe_allow_html=True)
st.write("Enter the element details in the table below:")
st.info("""
Each row represents an element in the system. Enter the X, Y, and Z coordinates for the element's center of gravity along with its mass.
Ensure that the mass is a positive value.
""")





def create_empty_df(n):
    return pd.DataFrame({"X": [0.0] * n, "Y": [0.0] * n, "Z": [0.0] * n, "Mass": [1.0] * n})

def create_random_df(n):
    return pd.DataFrame({
        "X": np.random.uniform(-10, 10, n),
        "Y": np.random.uniform(-10, 10, n),
        "Z": np.random.uniform(-10, 10, n),
        "Mass": np.random.uniform(1, 10, n)
    })

num_elements = st.number_input("Number of elements", min_value=1, step=1, value=3)

if "df" not in st.session_state or len(st.session_state.df) != num_elements:
    st.session_state.df = create_empty_df(num_elements)

if st.button("Fill Random Values"):
    st.session_state.df = create_random_df(num_elements)
    st.rerun()

col1, col2 = st.columns([2, 1])
with col1:
    df = st.data_editor(st.session_state.df, use_container_width=True, num_rows="dynamic")

    if "cog" not in st.session_state:
        st.session_state.cog = (None, None, None)
with col2:
    st.info("Description image")
    st.image("assets/image.png")
unit_length = st.selectbox("Length Unit", ["m", "cm", "ft"], index=0)


if st.button("Compute COG"):
    elements = [tuple(row) for row in df.to_numpy()]
    st.session_state.cog = compute_global_cog(elements)
    cog = st.session_state.cog
    st.info(f"**Global Center of Gravity (COG):** ({cog[0]:.2f} {unit_length}, {cog[1]:.2f} {unit_length}, {cog[2]:.2f} {unit_length})")

if st.button("Visualize COG"):
    cog = st.session_state.get("cog", (None, None, None))
    if cog == (None, None, None):
        st.warning("Please compute the COG first.")
    else:
        st.info(f"**Global Center of Gravity (COG):** ({cog[0]:.2f} {unit_length}, {cog[1]:.2f} {unit_length}, {cog[2]:.2f} {unit_length})")
        fig = go.Figure()
        fig.add_trace(go.Scatter3d(
            x=df["X"], y=df["Y"], z=df["Z"],
            mode='markers',
            marker=dict(size=8, color='blue', opacity=0.7),
            name="Element COGs"
        ))
        
        
        fig.add_trace(go.Scatter3d(
            x=[cog[0]], y=[cog[1]], z=[cog[2]],
            mode='markers',
            marker=dict(size=12, color='red', opacity=1),
            name="Global COG"
        ))
        
        
        fig.update_layout(
            title="Center of Gravity Visualization",
            scene=dict(
                xaxis_title=f"X Coordinate({unit_length})",
                yaxis_title=f"Y Coordinate({unit_length})",
                zaxis_title=f"Z Coordinate({unit_length})"
            ),
            margin=dict(l=0, r=0, b=0, t=40),
           autosize = True
        )
        
        st.plotly_chart(fig)