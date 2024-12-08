import streamlit as st

def render_state_viewer():
    simulador = st.session_state.simulador

    # Obtener registros y flags
    registros = simulador.registros.__dict__
    banderas = simulador.get_flags()

    st.subheader("Registros")
    for registro, valor in registros.items():
        st.text(f"{registro}: {valor}")

    st.subheader("Banderas")
    for bandera, estado in banderas.items():
        st.text(f"{bandera}: {estado}")
    if st.button("Reiniciar banderas"):
        simulador.reset_flags()
        st.success("Banderas reiniciadas.")
