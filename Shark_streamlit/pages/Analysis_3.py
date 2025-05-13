#Para tablas cruzadas entre Country y Activities
import pandas as pd
import streamlit as st
import seaborn as sns
import matplotlib.pyplot as plt
from utils import set_background
from utils import set_plot_style

st.set_page_config(page_title="Factors That Could Explain Shark Attacks", layout="wide")
st.title("🌍 Factors That Could Explain Shark Attacks")
def set_background():
    st.markdown("""
        <style>
            body {
                background-color: #0b1c2c;
                color: white;
            }
            .stApp {
                background: linear-gradient(180deg, #0b1c2c, #1e3a5f);
                color: white;
            }
            h1, h2, h3, .stTextInput > label, .stSelectbox > label {
                color: #d4f1f9;
            }
            .css-1d391kg { color: white; } /* Para el texto de los widgets */
            .css-ffhzg2 { background-color: rgba(255,255,255,0.05); }
        </style>
    """, unsafe_allow_html=True)

set_background()
set_plot_style(font='Arial', font_size=14)


@st.cache_data
def load_data():
    df = pd.read_csv("data/Shark_attacks_copy_recortado_copia.csv")
    return df

df = load_data()
df_ct = df[['Country', 'Activities']].dropna()

# Obtener top 10 países con más ataques
top_countries = df_ct['Country'].value_counts().head(10).index

# Filtrar datos
df_top = df_ct[df_ct['Country'].isin(top_countries)]

# Crear tabla cruzada
ct_table = pd.crosstab(df_top['Country'], df_top['Activities'])

# Visualizar heatmap centrado
center_col = st.columns([1, 2, 1])[1]
with center_col:
    st.subheader("🔥 Activity heatmap by country (top 10 countries with most attacks)")
    fig, ax = plt.subplots(figsize=(14, 6))
    sns.heatmap(ct_table, annot=True, fmt="d", cmap="Reds", linewidths=0.5, ax=ax)
    ax.set_title("Number of Attacks by Type of Activity", fontsize=16, fontweight='bold')
    plt.xticks(rotation=45, ha='right')
    plt.yticks(rotation=0)
    st.pyplot(fig)