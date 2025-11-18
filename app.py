import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px

# ----------------------------------------------------------
# Título
# ----------------------------------------------------------
st.title("Dashboard interactivo: Odómetro, Histograma y Dispersión")

# ----------------------------------------------------------
# Cargar datos
# ----------------------------------------------------------
df = pd.read_csv("vehicles_us.csv")

# Columnas a usar
col_odometer = "odometer"
col_price = "price"       # cámbiala si tu dataset usa otro nombre
col_fuel = "fuel"         # si no existe esta columna, puedes borrar 'color' en el scatter

st.subheader("Vista previa de los datos")
st.write(df.head())

# ----------------------------------------------------------
# Filtros
# ----------------------------------------------------------
st.sidebar.header("Filtros del odómetro")

min_value = int(df[col_odometer].min())
max_value = int(df[col_odometer].max())

rango = st.sidebar.slider(
    "Selecciona el rango del odómetro",
    min_value=min_value,
    max_value=max_value,
    value=(min_value, max_value)
)

df_filtrado = df[(df[col_odometer] >= rango[0]) & (df[col_odometer] <= rango[1])]

st.write(f"Mostrando {len(df_filtrado)} vehículos en el rango seleccionado.")

# ----------------------------------------------------------
# 1. Gráfico de Odómetro (Gauge)
# ----------------------------------------------------------
st.subheader("Odómetro promedio")

valor_promedio = df_filtrado[col_odometer].mean()

fig_gauge = go.Figure(
    go.Indicator(
        mode="gauge+number",
        value=valor_promedio,
        title={'text': "Odómetro promedio (millas)"},
        gauge={
            'axis': {'range': [0, max_value]},
            'bar': {'color': "blue"},
            'steps': [
                {'range': [0, df[col_odometer].quantile(0.33)], 'color': "#cce6ff"},
                {'range': [df[col_odometer].quantile(0.33), df[col_odometer].quantile(0.66)], 'color': "#99ccff"},
                {'range': [df[col_odometer].quantile(0.66), max_value], 'color': "#66b3ff"}
            ]
        }
    )
)

st.plotly_chart(fig_gauge)

# ----------------------------------------------------------
# 2. Histograma
# ----------------------------------------------------------
hist_button = st.button('Construir Histograma')

if hist_button:
    st.subheader("Histograma del odómetro")
    
    fig_hist = px.histogram(
    df_filtrado,
    x=col_odometer,
    nbins=40,
    title="Histograma del odómetro (filtrado)",
    labels={col_odometer: "Odómetro (millas)"}) 
    
    st.plotly_chart(fig_hist)

# ----------------------------------------------------------
# 3. Gráfico de dispersión (scatter plot)
# ----------------------------------------------------------
disp_button = st.button('Construir Grafico de dispersion')

if hist_button:
    st.subheader("Gráfico de dispersión: Odómetro vs Precio")
    
    fig_scatter = px.scatter(
    df_filtrado,
    x=col_odometer,
    y=col_price,
    color=col_fuel if col_fuel in df.columns else None,
    title="Dispersión entre Odómetro y Precio",
    labels={
        col_odometer: "Odómetro (millas)",
        col_price: "Precio ($)"
    },
    opacity=0.7)
    fig_scatter.update_traces(marker=dict(size=6))
    st.plotly_chart(fig_scatter)

