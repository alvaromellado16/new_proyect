import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px

# ----------------------------------------------------------
# Título
# ----------------------------------------------------------
st.title("Dashboard interactivo: Odómetro y Histograma con Plotly")

# ----------------------------------------------------------
# Cargar datos
# ----------------------------------------------------------
df = pd.read_csv("vehicles_us.csv")

# Asegúrate de que la columna sea correcta
col = "odometer"

st.subheader("Vista previa de los datos")
st.write(df.head())

# ----------------------------------------------------------
# Filtros
# ----------------------------------------------------------
st.sidebar.header("Filtros del odómetro")

min_value = int(df[col].min())
max_value = int(df[col].max())

# Slider interactivo
rango = st.sidebar.slider(
    "Selecciona el rango del odómetro",
    min_value=min_value,
    max_value=max_value,
    value=(min_value, max_value)
)

# Filtrar datos según el slider
df_filtrado = df[(df[col] >= rango[0]) & (df[col] <= rango[1])]

st.write(f"Mostrando {len(df_filtrado)} vehículos en el rango seleccionado.")

# ----------------------------------------------------------
# 1. Gráfico de Odómetro (Gauge)
# ----------------------------------------------------------
st.subheader("Odómetro promedio")

valor_promedio = df_filtrado[col].mean()

fig_gauge = go.Figure(
    go.Indicator(
        mode="gauge+number",
        value=valor_promedio,
        title={'text': "Odómetro promedio (millas)"},
        gauge={
            'axis': {'range': [0, max_value]},
            'bar': {'color': "blue"},
            'steps': [
                {'range': [0, df[col].quantile(0.33)], 'color': "#cce6ff"},
                {'range': [df[col].quantile(0.33), df[col].quantile(0.66)], 'color': "#99ccff"},
                {'range': [df[col].quantile(0.66), max_value], 'color': "#66b3ff"}
            ]
        }
    )
)

st.plotly_chart(fig_gauge)

# ----------------------------------------------------------
# 2. Histograma interactivo
# ----------------------------------------------------------
st.subheader("Histograma del odómetro")

fig_hist = px.histogram(
    df_filtrado,
    x=col,
    nbins=40,
    title="Histograma del odómetro filtrado",
    labels={col: "Odómetro (millas)"}
)

st.plotly_chart(fig_hist)

# ----------------------------------------------------------
# Fin
# ----------------------------------------------------------
st.write("Dashboard interactivo completado ✔")
