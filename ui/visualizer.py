import streamlit as st
from Model.SimuladorComputador import SimuladorComputador

def render_system_state():
    simulador = st.session_state.simulador
    
    col1, col2 = st.columns([1, 2])  # Proporción ajustada para entrada y estado
    
    with col1:
        st.markdown("### Editor de Código")
        code = st.text_area("Escribe tu programa aquí", height=400)
        if st.button("Ejecutar"):
            simulador.run(code.splitlines())
            st.success("Programa ejecutado con éxito.")
    
        if st.button("Paso"):
            simulador.step()
            # st.experimental_rerun()
        if st.button("Reset"):
            st.session_state.simulador = SimuladorComputador()
            st.success("Simulador reiniciado.")
            st.rerun()
    
    with col2:
        st.markdown("### Estado del Sistema")
            # Registros MAR, MBR, IR
        st.subheader("Registros Principales")
        st.table([
            {"Registro": "MAR", "Valor": simulador.mar.direccion},
            {"Registro": "MBR", "Valor": simulador.mbr.dato},
            {"Registro": "IR", "Valor": simulador.ir.dato},
        ])

        # Banco de Registros
        st.subheader("Banco de Registros Generales")
        st.table([
            {"Registro": "AL", "Valor": simulador.registros.AL},
            {"Registro": "BL", "Valor": simulador.registros.BL},
            {"Registro": "CL", "Valor": simulador.registros.CL},
            {"Registro": "DL", "Valor": simulador.registros.DL},
        ])

        # Memoria Principal
        st.subheader("Memoria Principal")
        memoria = simulador.memory.memory
        memoria_mostrada = [{"Posición": i, "Valor": memoria[i]} for i in range(len(memoria)) if memoria[i] != 0]
        st.table(memoria_mostrada)

    # ALU
    st.subheader("ALU")
    st.write("Operaciones Lógicas y Aritméticas")
    st.table([{"Dato 1": simulador.alu.dato1, "Dato 2": simulador.alu.dato2, "Resultado": simulador.alu.result, **simulador.alu.flags}])

    # Unidad de Control
    st.subheader("Unidad de Control")
    st.write("Señales Activas")
    st.table([{"Señal": simulador.control.señal, "Instrucción": simulador.control.dato}])

    # Contador de Programa
    st.subheader("Contador de Programa (PC)")
    st.write(simulador.pc.contador)



    # Dispositivos de I/O
    st.subheader("Dispositivos de I/O")
    st.write("Por implementar: Representación de datos de entrada/salida.")

    # Bus del Sistema
    st.subheader("Bus del Sistema")
    st.write("Transferencias entre componentes")
    st.table([
        {"Origen": "Unidad de Control", "Destino": "ALU", "Estado": "Inactivo"},
        {"Origen": "Memoria", "Destino": "MBR", "Estado": "Activo"},
    ])
