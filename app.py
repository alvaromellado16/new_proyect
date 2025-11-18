import pandas as pd
import streamlit as st
import plotly.graph_objects as go  
car_data = pd.read_csv('vehicles_us.csv')

car_data = pd.read_csv('vehicles_us.csv')

st.header("Vehiculos Us")

hist_button = st.button('Hacer Histograma')

if hist_button:
    st.write('Haciendo un histograma para el conjunto de datos de anuncios de venta de coches.')


    fig = go.Figure(data=[go.Histogram(x=car_data['odometer'])])

    fig.update_layout(tittle_text='Distribucion del Odometro')
    
    st.plotly_chart(fig, use_container_width=True)

if st.button("Mostrar Graficode Dispersion"):
    fig_scatter = go.scatter(df, x="sepal_width", y="sepal_length", color="species",
                             title="Gráfico de dispersión (Iris)")
    st.write("Gráfico de dispersión generado:")
    st.plotly_chart(fig_scatter)