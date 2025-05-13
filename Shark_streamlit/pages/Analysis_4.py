
#------------------------------------------------------------------------------------
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from utils import set_background
from utils import set_plot_style


st.set_page_config(layout="wide")

def set_background():
    st.markdown("""
        <style>
            .main {
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
            .css-1d391kg { color: white; }
            .css-ffhzg2 { background-color: rgba(255,255,255,0.05); }
        </style>
    """, unsafe_allow_html=True)

set_background()
set_plot_style(font='Arial', font_size=14)

# Título principal alineado a la izquierda
st.title("💥 Shark Attack Analysis")

# Cargar datos
@st.cache_data
def load_data():
    return pd.read_csv("data/Shark_attacks_copy_recortado_copia.csv")

df = load_data()

# -------------------------------
# 1️⃣ Top especies de tiburones
# -------------------------------
center_col = st.columns([1, 2, 1])[1]
with center_col:
    st.markdown("### 🦈 Shark Species Most Frequently Involved in Attacks")
    df_species = df[['Species_Shark']].dropna()
    df_species = df_species[
        (df_species['Species_Shark'].str.strip().str.lower() != 'unknown') &
        (df_species['Species_Shark'].str.strip().str.lower() != 'shark')
    ]
    top_species = df_species['Species_Shark'].value_counts().head(5)
    fig, ax = plt.subplots(figsize=(12, 5))
    sns.barplot(
        x=top_species.values,
        y=top_species.index,
        palette="Blues_r",
        ax=ax
    )
    ax.set_title("Top 5 Shark Species Involved", fontsize=16, fontweight='bold')
    ax.set_xlabel("Number of Attacks")
    ax.set_ylabel("Shark Species")
    ax.grid(True, linestyle='--', alpha=0.3)
    st.pyplot(fig)

# -------------------------------
# 2️⃣ Mortalidad por especie
# -------------------------------

center_col = st.columns([1, 2, 1])[1]
with center_col:
    st.markdown("### ⚰️ Mortality in Attacks by Shark Species")
    df_filtered = df[['Species_Shark', 'Fatal']].dropna()
    df_filtered = df_filtered[
        (df_filtered['Species_Shark'].str.strip().str.lower() != 'unknown') &
        (df_filtered['Species_Shark'].str.strip().str.lower() != 'shark')
    ]
    top_species = df_filtered['Species_Shark'].value_counts().head(5).index
    df_top = df_filtered[df_filtered['Species_Shark'].isin(top_species)].copy()
    df_top['Fatal'] = df_top['Fatal'].str.upper().replace({'Y': 'Mortal', 'N': 'No Mortal'})
    fatal_counts = df_top.groupby(['Species_Shark', 'Fatal']).size().unstack(fill_value=0)
    fig, ax = plt.subplots(figsize=(12, 5))
    fatal_counts[['No Mortal', 'Mortal']].plot(
        kind='bar',
        stacked=True,
        color=['skyblue', 'salmon'],
        ax=ax
    )
    ax.set_title("Fatal and Non-Fatal Attacks by Species", fontsize=16, fontweight='bold')
    ax.set_xlabel("Shark Species")
    ax.set_ylabel("Number of Attacks")
    ax.legend(title="Type of Attack")
    ax.grid(axis='y', linestyle='--', alpha=0.5)

    # Rotar las etiquetas del eje X a 45 grados
    plt.xticks(rotation=45)

    st.pyplot(fig)


# -------------------------------
# 3️⃣ Heatmap Actividades vs Especie
# -------------------------------

center_col2 = st.columns([1, 2, 1])[1]
with center_col2:
    st.markdown("### 🔍 Relationship Between Activities and Shark Species")
    df_heatmap = df[['Activities', 'Species_Shark']].dropna()
    df_heatmap = df_heatmap[
        (df_heatmap['Species_Shark'].str.strip().str.lower() != 'unknown') &
        (df_heatmap['Species_Shark'].str.strip().str.lower() != 'shark')
    ]
    top_species_heat = df_heatmap['Species_Shark'].value_counts().head(5).index
    top_activities = df_heatmap['Activities'].value_counts().head(5).index
    df_heatmap_filtered = df_heatmap[
        df_heatmap['Species_Shark'].isin(top_species_heat) &
        df_heatmap['Activities'].isin(top_activities)
    ]
    heatmap_data = pd.crosstab(df_heatmap_filtered['Activities'], df_heatmap_filtered['Species_Shark'])
    
    fig, ax = plt.subplots(figsize=(10, 6))
    sns.heatmap(
        heatmap_data,
        annot=True,
        fmt="d",
        cmap="Blues",
        linewidths=0.5,
        linecolor='gray',
        cbar=True,
        ax=ax
    )
    ax.set_title("Attack Frequency by Activity and Species", fontsize=16, fontweight='bold')
    ax.set_xlabel("Shark Species")
    ax.set_ylabel("Victim's Activity")
    ax.set_xticklabels(ax.get_xticklabels(), rotation=45, ha='right')  # 👈 Rotación agregada aquí
    st.pyplot(fig)
