import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from utils import set_background
from utils import set_plot_style

st.set_page_config(page_title="Shark Attack Temporal Trends", layout="wide")
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
            label, .css-1cpxqw2 { 
                color: white !important;
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
st.title("📈 Shark Attack Temporal Trends")
#set_background("images/fondo_mar.jpg")

@st.cache_data
def load_data():
    df = pd.read_csv("data/Shark_attacks_copy_recortado_copia.csv")
    return df

df = load_data()

# Validación de columna 'Years'
if "Years" not in df.columns:
    st.error("La columna 'Years' no existe en el dataset.")
else:
    # Limitar filtro de años de 1700 a 2025 para la primera gráfica
    year_range = st.slider(
        "Select the year range for the first chart:",
        min_value=1940,
        max_value=2017,
        value=(1940, 2017)
    )

    # Filtrar por años seleccionados para la primera gráfica
    df_filtered = df[(df["Years"] >= year_range[0]) & (df["Years"] <= year_range[1])]
    
    # Validación de columnas
    if "Months" not in df.columns:
        st.error("La columna 'Months' no existe en el dataset.")
    else:
        # Eliminar filas con valores nulos en 'Years' o 'Months'
        df_filtered = df_filtered.dropna(subset=["Years", "Months"])

        # Asegurar tipo correcto
        df_filtered["Years"] = df_filtered["Years"].astype(int)
        df_filtered["Months"] = df_filtered["Months"].astype(int)

        # Agrupar por año
        yearly_counts = df_filtered["Years"].value_counts().sort_index()

        # Mostrar gráfico de ataques por año (más ancho y atractivo)
    fig, ax = plt.subplots(figsize=(12, 6))  # Aumentamos el tamaño
    sns.set_palette("Blues")  # Elegimos una paleta de colores relacionada con el mar

    # Línea más suave con sombreado debajo
    sns.lineplot(x=yearly_counts.index, y=yearly_counts.values, ax=ax, linewidth=2.5, marker='o', linestyle='-', color='#1f77b4')

    # Forzar eje x a mostrar solo enteros
    from matplotlib.ticker import MaxNLocator
    ax.xaxis.set_major_locator(MaxNLocator(integer=True))

    # Mejorar los títulos y etiquetas
    ax.set_title("Shark attack frequency by year", fontsize=16, fontweight='bold', color='#333333')
    ax.set_xlabel("Year", fontsize=14, color='#555555')
    ax.set_ylabel("Number of attacks", fontsize=14, color='#555555')
    ax.grid(True, linestyle='--', alpha=0.5)

    # Personalizar la apariencia del eje
    for label in (ax.get_xticklabels() + ax.get_yticklabels()):
        label.set_fontsize(12)
        label.set_color('#444444')


    centered_col = st.columns([1, 2, 1])[1]
    with centered_col:
        st.pyplot(fig)  # Mostrar la gráfica de ataques por año



        # ----------------------------- Gráfica fija de Cuatrimestres (2000-2025) -----------------------------

        # Filtrar solo los datos entre 2000 y 2017 para la gráfica de cuatrimestres
        df_quarter = df[(df["Years"] >= 2000) & (df["Years"] <= 2017)]

        # Crear una columna de cuatrimestre
        df_quarter["quarter"] = df_quarter["Months"].apply(lambda x: "Q1" if 1 <= x <= 4 else "Q2" if 5 <= x <= 8 else "Q3" if 9 <= x <= 12 else "Q4")
        df_quarter["period"] = df_quarter["Years"].astype(str) + "-" + df_quarter["quarter"]


        # Asegurar que 'Years' es int antes de agrupar
        df_quarter["Years"] = df_quarter["Years"].astype(int)

        # Agrupar por periodo (año-cuatrimestre)
        period_counts = df_quarter.groupby(["Years", "quarter"]).size().unstack(fill_value=0)



        # Agrupar por periodo (año-cuatrimestre)
        #period_counts = df_quarter.groupby(["Years", "quarter"]).size().unstack(fill_value=0)

        # Mostrar gráfico de ataques por cuatrimestre, agrupado por año
        fig_quarter, ax_quarter = plt.subplots(figsize=(14, 6))  # Aumentamos el tamaño
        sns.set_palette("Reds")  # Usamos una paleta cálida, similar al peligro

        # Gráfico de barras agrupadas para ataques por cuatrimestre
        period_counts.plot(kind='bar', stacked=False, ax=ax_quarter, width=0.8)  # Aumentamos el ancho de las barras

        # Mejorar los títulos y etiquetas
        ax_quarter.set_title("Shark attacks by quarter (2000-2017)", fontsize=16, fontweight='bold', color='#333333')
        ax_quarter.set_xlabel("Quarter", fontsize=14, color='#555555')
        ax_quarter.set_ylabel("Number of attacks", fontsize=14, color='#555555')
        ax_quarter.grid(True, linestyle='--', alpha=0.5)

        # Rotar etiquetas del eje X para mejorar la legibilidad
        plt.xticks(rotation=45, fontsize=12, color='#444444')

        # Personalizar la apariencia del eje
        for label in (ax_quarter.get_xticklabels() + ax_quarter.get_yticklabels()):
            label.set_fontsize(12)
            label.set_color('#444444')

        with centered_col:
            st.pyplot(fig_quarter)  # Mostrar la gráfica de ataques por cuatrimestre

