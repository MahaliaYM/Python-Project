import streamlit as st
import base64

# Configurar página
st.set_page_config(page_title="Análisis de Ataques de Tiburones", layout="wide")

# --- Añadir fondo de imagen (fondo del mar) ---
def set_background(image_url):
    st.markdown(
        f"""
        <style>
        .stApp {{
            background-image: url("{image_url}");
            background-attachment: fixed;
            background-size: cover;
        }}
        </style>
        """,
        unsafe_allow_html=True
    )

# Imagen del fondo del mar (puedes cambiar por otra URL si lo deseas)
background_url = "https://media.istockphoto.com/id/948920056/es/foto/gran-tibur%C3%B3n-blanco-submarino-diagonal-foco-en-la-mitad-delantera.jpg?s=612x612&w=0&k=20&c=LTYcQ_Y9whb1oyGY2YXFdNq7nPICNNpWEgOYxhUf0z8="  # fondo marino
set_background(background_url)
#set_background("images/fondo.png")

# --- Contenido de la portada ---
st.markdown("<h1 style='color: white;'>🌊 Análisis de Ataques de Tiburones</h1>", unsafe_allow_html=True)

st.markdown(
    """
    <div style="color: white; font-size: 18px; max-width: 800px;">
        Explora los datos sobre ataques de tiburones, sus tendencias y patrones a lo largo del tiempo..

        Usa el menú lateral para navegar entre las diferentes secciones del análisis.
    </div>
    """,
    unsafe_allow_html=True
)