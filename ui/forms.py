import streamlit as st
from Model.SimuladorComputador import SimuladorComputador
def render_code_editor():
    st.header("Editor de Código")
    program_input = st.text_area("Escriba su código en ensamblador", height=200)

    if st.button("Cargar Programa"):
        simulador = st.session_state.simulador
        program = program_input.splitlines()
        simulador.run(program)
        st.success("Programa cargado y listo para ejecución.")

    if st.button("Ejecutar Paso"):
        simulador = st.session_state.simulador
        simulador.step()
        st.info("Ejecutado un paso.")

    if st.button("Reiniciar"):
        st.session_state.simulador = SimuladorComputador()
        st.success("Simulador reiniciado.")
