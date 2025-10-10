# -*- coding: utf-8 -*-
"""institucional_grupo10.py"""

# =============================
# IMPORTACIÓN DE LIBRERÍAS
# =============================
import streamlit as st
import pandas as pd
import yfinance as yf
import plotly.express as px
import matplotlib.pyplot as plt

# =============================
# CONFIGURACIÓN DE LA PÁGINA
# =============================
st.set_page_config(
    page_title="Mi APP",
    page_icon="🧠",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# =============================
# FUNCIÓN PRINCIPAL
# =============================
def main():
    st.title("Bienvenidos a Código Espinoza 🧠")
    st.sidebar.header("Navegación")

    # =============================
    # SECCIÓN: ANÁLISIS FINANCIERO
    # =============================
    st.markdown(
        """
        <h2 style='color: #1E90FF;'>
            BIENVENIDOS AL GRUPO 10 💼
        </h2>
        """,
        unsafe_allow_html=True
    )

    st.header("Análisis de Rentabilidad y Riesgo 📊")
    st.write("""
    Este proyecto analiza el comportamiento financiero de tres grandes empresas tecnológicas.
    A través de indicadores como la rentabilidad esperada, la volatilidad y el Ratio de Sharpe,
    evaluamos la relación entre riesgo y retorno para identificar el portafolio más eficiente. 💼
    """)

    # Lista de tickers
    lista_tickers = ["AAPL", "MSFT", "NVDA", "META"]

    # Multiselect para elegir empresas
    ticker = st.multiselect("Elija una o más empresas para analizar:", lista_tickers)

    # Imagen decorativa
    st.image(
        "https://cdn.pixabay.com/photo/2017/06/16/07/37/stock-exchange-2408858_1280.jpg",
        use_container_width=True
    )

    # Botón para ejecutar análisis
    if st.button("Calcular Rentabilidad y Riesgo"):
        if not ticker:
            st.warning("⚠️ Selecciona al menos una empresa para continuar.")
        else:
            # Descargar datos históricos
            data = yf.download(tickers=ticker, period="6mo")["Close"]

            # Calcular rentabilidades diarias
            rent_diaria = data.pct_change().dropna()

            # Calcular métricas financieras
            rent_promedio = rent_diaria.mean() * 252  # anualizada
            riesgo = rent_diaria.std() * (252 ** 0.5)  # desviación estándar anualizada
            sharpe = rent_promedio / riesgo

            # Crear DataFrame resumen
            resumen = pd.DataFrame({
                "Rentabilidad esperada (%)": rent_promedio * 100,
                "Riesgo (Volatilidad %)": riesgo * 100,
                "Ratio Sharpe": sharpe
            })

            # Mostrar tabla de resultados
            st.subheader("📋 Resultados Comparativos de Empresas")
            st.dataframe(resumen.style.format("{:.2f}"))

            # =============================
            # GRÁFICO DE TORTA (PLOTLY)
            # =============================
            st.subheader("📊 Gráfico de Torta - Rentabilidad Esperada (%)")
            fig_pie = px.pie(
                resumen,
                names=resumen.index,
                values="Rentabilidad esperada (%)",
                title="Distribución de la Rentabilidad Esperada entre Empresas",
                hole=0.3,
                color_discrete_sequence=px.colors.qualitative.Safe
            )
            st.plotly_chart(fig_pie, use_container_width=True)

    # =============================
    # SECCIÓN EXTRA: DATAFRAME LOCAL
    # =============================
    st.header("📁 Análisis de Encuesta de Empleados (Ejemplo Local)")
    try:
        df = pd.read_csv("employee_survey.csv")
        df_count = df.groupby("Gender").count().reset_index()

        fig_local = px.pie(
            df_count,
            values=df_count.columns[1],  # Primera columna de conteo
            names="Gender",
            title="Distribución de Género en la Encuesta"
        )
        st.plotly_chart(fig_local, use_container_width=True)
    except FileNotFoundError:
        st.info("📂 No se encontró el archivo 'employee_survey.csv'. Sube el archivo para visualizar el gráfico.")


# =============================
# EJECUCIÓN PRINCIPAL
# =============================
if __name__ == "__main__":
    main()
