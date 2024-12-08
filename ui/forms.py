import streamlit as st

def render_code_editor():
    st.header("Editor de Código")
    code = st.text_area("Escriba su código en ensamblador aquí:", height=300)
    if st.button("Assemble"):
        st.session_state.simulador.load_program(code.split("\n"))
        st.success("Código ensamblado exitosamente.")

    col1, col2, col3 = st.columns(3)
    with col1:
        if st.button("Run"):
            st.session_state.simulador.run()
            st.success("Ejecución completada.")
    with col2:
        if st.button("Step"):
            st.session_state.simulador.step()
            st.info("Instrucción ejecutada.")
    with col3:
        if st.button("Reset"):
            st.session_state.simulador.reset()
            st.info("Estado reiniciado.")
