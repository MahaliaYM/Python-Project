import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from utils import set_background
from utils import set_plot_style

st.set_page_config(page_title="Geographic Incidence of Shark Attacks", layout="wide")
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



st.title("🌍 Geographic Incidence of Shark Attacks")

@st.cache_data
def load_data():
    df = pd.read_csv("data/Shark_attacks_copy_recortado_copia.csv")
    return df

df = load_data()

# Limpiar columnas relevantes
df_geo = df[['Country', 'Region', 'Location']].dropna()
df_geo = df_geo[df_geo['Country'].str.lower() != 'unknown']

# ------------------ Bloque 1: Países con más ataques ------------------
center_col = st.columns([1, 2, 1])[1]

with center_col:
    st.subheader("🏴‍☠️ Countries with the Highest Number of Attacks")
    
    top_countries = df_geo['Country'].value_counts().head(10)

    fig1, ax1 = plt.subplots(figsize=(14, 6))
    sns.barplot(x=top_countries.values, y=top_countries.index, palette="Reds_r", ax=ax1)
    ax1.set_title("Top 10 countries with the most shark attacks", fontsize=16, fontweight='bold')
    ax1.set_xlabel("Number of attacks", fontsize=14)
    ax1.set_ylabel("Country", fontsize=14)
    ax1.grid(True, linestyle='--', alpha=0.3)
    
    st.pyplot(fig1)



# ------------------ Bloque 2: Regiones por país ------------------
df_country = None
center_col = st.columns([1, 2, 1])[1]

with center_col:
    st.subheader("🔍 Details by Country")
    
    selected_country = st.selectbox(
        "Select a country to see its most affected regions:",
        df_geo['Country'].dropna().unique()
    )

    df_country = df_geo[df_geo['Country'] == selected_country]
    top_regions = df_country['Region'].value_counts().head(5)

    fig2, ax2 = plt.subplots(figsize=(14, 6))
    sns.barplot(x=top_regions.values, y=top_regions.index, palette="Blues_r", ax=ax2)
    ax2.set_title(f"Top regions with the most attacks in {selected_country}", fontsize=16, fontweight='bold')
    ax2.set_xlabel("Number of attacks", fontsize=14)
    ax2.set_ylabel("Region", fontsize=14)
    ax2.grid(True, linestyle='--', alpha=0.3)

    st.pyplot(fig2)

# ------------------ Bloque 3: Localizaciones por región ------------------
center_col = st.columns([1, 2, 1])[1]

with center_col:
    st.subheader("📌 Locations with the highest incidence in the region")

    if df_country is not None:
        selected_region = st.selectbox(
            "Select a region to see specific locations:",
            df_country['Region'].dropna().unique()
        )

        df_region = df_country[df_country['Region'] == selected_region]
        top_locations = df_region['Location'].value_counts().head(5)

        fig3, ax3 = plt.subplots(figsize=(14, 6))
        sns.barplot(x=top_locations.values, y=top_locations.index, palette="Greens_r", ax=ax3)
        ax3.set_title(f"Top locations in {selected_region}, {selected_country}", fontsize=16, fontweight='bold')
        ax3.set_xlabel("Number of attacks", fontsize=14)
        ax3.set_ylabel("Location", fontsize=14)
        ax3.grid(True, linestyle='--', alpha=0.3)

        st.pyplot(fig3)



# import pandas as pd
import plotly.express as px
# import streamlit as st
# pip install pycountry geopy
from geopy.geocoders import Nominatim
from geopy.exc import GeocoderTimedOut
import time

# Configuración de la página
#st.set_page_config(page_title="Mapa de Ataques", layout="wide")
#st.title("🌍 Mapa Interactivo: Incidencia de Ataques de Tiburón")

# Cargar CSV
@st.cache_data
def load_data():
    df = pd.read_csv("data/Shark_attacks_copy_recortado_copia.csv")
    return df

# Geolocalización con caché
@st.cache_data
def get_coordinates_batch(locations):
    geolocator = Nominatim(user_agent="shark-attack-app")
    coords_dict = {}
    for loc in locations:
        try:
            location = geolocator.geocode(loc, timeout=10)
            if location:
                coords_dict[loc] = (location.latitude, location.longitude)
            else:
                coords_dict[loc] = (None, None)
            time.sleep(1)  # Para evitar saturar Nominatim
        except GeocoderTimedOut:
            coords_dict[loc] = (None, None)
    return coords_dict

# Cargar datos
df = load_data()
df = df[['Country', 'Region', 'Location']].dropna()

# Obtener Top 10 países con más ataques
top_10_countries = df['Country'].value_counts().head(10).index.tolist()

# Filtrar el DataFrame solo a esos 10 países
df = df[df['Country'].isin(top_10_countries)]

# Selector de nivel de agrupación
nivel = st.radio("Select the level of geographic detail:", ["Country", "Region", "Location"], horizontal=True)

# Agrupación según el nivel
if nivel == "Country":
    df_group = df.groupby('Country').size().reset_index(name='Attacks')
    df_group = df_group.sort_values('Attacks', ascending=False).head(10)
    df_group['Label'] = df_group['Country']

else:
    # Selector de país
    country_options = df['Country'].value_counts().index.tolist()
    selected_country = st.selectbox("Select a country", country_options)

    # Checkbox para mostrar todas las entradas o solo Top 10
    mostrar_todo = st.checkbox("Show all entries", value=False)

    # Filtrar solo por el país seleccionado
    df_filtered = df[df['Country'] == selected_country]

    if nivel == "Region":
        df_filtered['Region_full'] = df_filtered['Region'] + ", " + df_filtered['Country']
        df_group = df_filtered.groupby('Region_full').size().reset_index(name='Attacks')
        df_group = df_group.sort_values('Attacks', ascending=False)

        if not mostrar_todo:
            df_group = df_group.head(10)

        df_group['Label'] = df_group['Region_full']

    elif nivel == "Location":
        df_filtered['Location_full'] = df_filtered['Location'] + ", " + df_filtered['Region'] + ", " + df_filtered['Country']
        df_group = df_filtered.groupby('Location_full').size().reset_index(name='Attacks')
        df_group = df_group.sort_values('Attacks', ascending=False)

        if not mostrar_todo:
            df_group = df_group.head(10)

        df_group['Label'] = df_group['Location_full']


# Geocodificar según el campo agrupado
locations = df_group['Label'].unique().tolist()
coords_dict = get_coordinates_batch(locations)

# Añadir coordenadas
df_group['Lat'] = df_group['Label'].map(lambda x: coords_dict.get(x, (None, None))[0])
df_group['Lon'] = df_group['Label'].map(lambda x: coords_dict.get(x, (None, None))[1])

# Limpiar datos sin coordenadas
df_group = df_group.dropna(subset=['Lat', 'Lon'])

# Crear mapa
fig = px.scatter_geo(
    df_group,
    lat='Lat',
    lon='Lon',
    text=None if nivel == "Location" else 'Label',
    size='Attacks',
    size_max=30,
    title=f"🌊 Shark attacks grouped by {nivel}",
    projection='natural earth',
    color='Attacks',
    color_continuous_scale='Blues_r',
    hover_name='Label',
    hover_data={'Attacks': True, 'Lat': False, 'Lon': False}
)

# Estética del mapa
fig.update_geos(
    bgcolor='rgb(35, 35, 35)',
    showland=True,
    landcolor='rgb(23, 23, 23)',
    showlakes=True,
    lakecolor='rgb(13, 13, 13)',
    projection_scale=5,
)

fig.update_layout(
    margin={"r": 0, "t": 50, "l": 0, "b": 0},
    font=dict(color="white")
)

# Mostrar el gráfico centrado
center_col = st.columns([1, 2, 1])[1]
with center_col:
    st.plotly_chart(fig, use_container_width=True)