import streamlit as st
from Model.SimuladorComputador import SimuladorComputador
from ui.visualizer import render_system_state

st.set_page_config(page_title="Simulador de Computador", layout="wide")

if "simulador" not in st.session_state:
    st.session_state.simulador = SimuladorComputador()

st.title("Simulador de Computador")
render_system_state()



