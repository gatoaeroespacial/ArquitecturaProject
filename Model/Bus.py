import time
import streamlit as st
class Bus:
    def __init__(self):
        pass

    # El bus de direccion toma la señal dada por un origen y la lleva al destino
    def transferirDireccion(self, origen, destino):
        destino.direccion = origen.direccion
        origen.direccion = ""

    # El bus de control toma la señal dada por un origen y la lleva al destino
    def transferirControl(self, origen, destino):
        destino.señal = origen.señal
        origen.señal = ""

    #El bus de datos toma la señal dada por un origen y la lleva al destino
    def transferirDato(self, origen, destino):
        destino.dato = origen.dato
        print("aqui")
        st.info(f"Dato transferido pon la variable {destino.dato}")
        st.session_state.registrosPrin.loc[st.session_state.registrosPrin["Registro"] == "MAR", "Valor"] = str("hola")
        
        time.sleep(0.5)
         
    
        

        origen.dato = ""
    
    def transferirContador(self, contador, destino):
        destino.direccion = contador