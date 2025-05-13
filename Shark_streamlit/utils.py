import streamlit as st
import base64
import matplotlib.pyplot as plt
import seaborn as sns

def set_background(image_path):
    # Leer y codificar la imagen en base64
    with open(image_path, "rb") as image_file:
        encoded = base64.b64encode(image_file.read()).decode()

    # Inyectar CSS con el fondo
    background_style = f"""
    <style>
    .stApp {{
        background-image: url("data:image/jpg;base64,{encoded}");
        background-size: cover;
        background-repeat: no-repeat;
        background-attachment: fixed;
    }}
    </style>
    """
    st.markdown(background_style, unsafe_allow_html=True)

def set_plot_style(font='sans-serif', font_size=12):
    plt.rcParams.update({
        'font.family': font,
        'font.size': font_size,
        'axes.titlesize': font_size + 2,
        'axes.labelsize': font_size,
        'xtick.labelsize': font_size - 1,
        'ytick.labelsize': font_size - 1,
        'legend.fontsize': font_size - 1,
        'figure.titlesize': font_size + 4
    })
    sns.set_style("whitegrid")