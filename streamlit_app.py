import streamlit as st
import numpy as np

# Define sizing functions
def calculate_diameter(nc_type, wavelength):
    if nc_type == "CdSe":
        return 1.6122e-9 * wavelength**4 - 2.6575e-6 * wavelength**3 + 1.6242e-3 * wavelength**2 - 0.4277 * wavelength + 41.57
    elif nc_type == "CdS":
        return(-6.6521e-8) * wavelength**3 + (1.9557e-4) * wavelength**2 - 0.092352 * wavelength + 13.29
    elif nc_type == "CdTe":
        return (9.8127e-7) * wavelength**3 - (1.7147e-3) * wavelength**2 + 1.0064 * wavelength - 194.84
    else:
        return None

# Extinction coefficient function
def calculate_extinction_coefficient(nc_type, diameter):
    if nc_type == "CdSe":
        return 5857 * diameter**2.65
    elif nc_type == "CdS":
        return 21536 * diameter**2.3
    elif nc_type == "CdTe":
        return 10043 * diameter**2.12
    else:
        return None

# Beer-Lambert concentration
def calculate_concentration(absorbance, extinction_coeff, path_length):
    if absorbance is None or extinction_coeff is None or path_length is None:
        return None
    try:
        return absorbance / (extinction_coeff * path_length)
    except ZeroDivisionError:
        return None

# --- Streamlit GUI ---
st.title("Quantum Dot Size & Concentration Calculator")

# Input for NC Type
nc_type = st.selectbox("Select Nanocrystal Type:", ["CdSe", "CdS", "CdTe"])

# Input for absorption peak
wavelength = st.number_input("First Absorption Peak Wavelength (nm):", min_value=300.0, max_value=1000.0, step=0.1)

# Calculate size
if wavelength:
    diameter = calculate_diameter(nc_type, wavelength)
    st.write(f"**Calculated Diameter:** {diameter:.2f} nm")

# Extinction coefficient
if 'diameter' in locals() and diameter is not None:
    extinction_coeff = calculate_extinction_coefficient(nc_type, diameter)
    st.write(f"**Extinction Coefficient:** {extinction_coeff:,.2e} M⁻¹cm⁻¹")

# Optional: Concentration calculation
st.subheader("Optional: Calculate Molar Concentration")

absorbance = st.number_input("Absorbance at first excitonic peak:", min_value=0.0, step=0.01)
path_length = st.number_input("Path Length (cm):", value=1.0, min_value=0.0, step=0.01)

if absorbance and path_length and extinction_coeff:
    concentration = calculate_concentration(absorbance, extinction_coeff, path_length)
    if concentration:
        st.write(f"**Calculated Concentration:** {concentration:.2e} M")
else:
    st.write("Fill absorbance and path length to compute concentration.")


footer_html = """<div style='text-align: center;'>
  <p>Developed by Melvin Lim for Quantum Leap</p>
</div>"""
st.markdown(footer_html, unsafe_allow_html=True)