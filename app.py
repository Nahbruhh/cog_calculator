import streamlit as st
import pandas as pd
import numpy as np

def compute_global_cog(elements):
    """
    Compute the global center of gravity (COG) for multiple elements.
    :param elements: List of tuples (x, y, z, mass)
    :return: (X_COG, Y_COG, Z_COG)
    """
    total_mass = sum(m for _, _, _, m in elements)
    if total_mass == 0:
        return (None, None, None)
    
    weighted_x = sum(x * m for x, _, _, m in elements)
    weighted_y = sum(y * m for _, y, _, m in elements)
    weighted_z = sum(z * m for _, _, z, m in elements)
    
    return (weighted_x / total_mass, weighted_y / total_mass, weighted_z / total_mass)

st.title("Global Center of Gravity Calculator")

st.write("Enter the element details in the table below:")
st.info("""
Each row represents an element in the system. Enter the X, Y, and Z coordinates for the element's center of gravity along with its mass.
 Ensure that the mass is a positive value.
 """)

num_elements = st.number_input("Number of elements", min_value=1, step=1, value=3)

def create_empty_df(n):
    return pd.DataFrame({"X": [0.0] * n, "Y": [0.0] * n, "Z": [0.0] * n, "Mass": [1.0] * n})

if "df" not in st.session_state or len(st.session_state.df) != num_elements:
    st.session_state.df = create_empty_df(num_elements)

df = st.data_editor(st.session_state.df, use_container_width=True, num_rows="dynamic")

if st.button("Compute COG"):
    elements = [tuple(row) for row in df.to_numpy()]
    cog = compute_global_cog(elements)
    st.info(f"**Global Center of Gravity (COG):** ({cog[0]:.2f}, {cog[1]:.2f}, {cog[2]:.2f})")
