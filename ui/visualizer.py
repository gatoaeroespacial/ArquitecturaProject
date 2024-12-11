import streamlit as st
from Model.SimuladorComputador import SimuladorComputador

def render_system_state():


    simulador = st.session_state.simulador
    
    # División principal en columnas superiores
    col1, col2, col3 = st.columns([1, 1, 1])

    with col1:
        st.markdown("### Editor de Código")
        code = st.text_area("Escribe tu programa aquí", height=400)
        if st.button("Ejecutar"):
            simulador.run(code.splitlines())
            st.success("Programa ejecutado con éxito.")

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

        # Contador de Programa
        st.subheader("Contador de Programa (PC)")
        st.write(simulador.pc.contador)

    with col3:
        # Memoria Principal
        st.subheader("Memoria Principal")
        memoria = simulador.memory.memory
        memoria_mostrada = [
            {"Posición": i, "Valor": memoria[i]} 
            for i in range(len(memoria)) if memoria[i] != 0
        ]
        st.dataframe(memoria_mostrada, width=500, height=250)  # Limita la altura con scroll si es necesario

        # Unidad de Control
        st.subheader("Unidad de Control")
        st.write("Señales Activas")
        st.table([{"Señal": simulador.control.señal, "Instrucción": simulador.control.dato}])

        st.text_area("Salida de la ejecución del programa", simulador.salida, disabled=True, height=100)

    # División inferior en columnas
    col4, col5 = st.columns([1, 1])

    with col4:
        # ALU
        st.subheader("ALU")
        st.write("Operaciones Lógicas y Aritméticas")
        st.table([
            {"Dato 1": simulador.alu.dato1, "Dato 2": simulador.alu.dato2, "Resultado": simulador.alu.result, **simulador.alu.flags}
        ])

    with col5:
        # Bus del Sistema
        st.subheader("Bus del Sistema")
        st.write("Transferencias entre componentes")
        st.table([
            {"Origen": "Unidad de Control", "Destino": "ALU", "Estado": "Inactivo"},
            {"Origen": "Memoria", "Destino": "MBR", "Estado": "Activo"},#hacer que se active cuando se lea o escriba en memoria
        ])

    # Dispositivos de I/O
    st.subheader("Dispositivos de I/O")
    st.write("Por implementar: Representación de datos de entrada/salida.")