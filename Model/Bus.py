import streamlit as st
import time
class Bus:
    def __init__(self):
        pass

    # El bus de direccion toma la señal dada por un origen y la lleva al destino
    def transferirDireccion(self, origen, destino):
        destino.direccion = origen.direccion
        
        mensaje1= st.empty()
        mensaje1.info(f"Se transfirio por el bus de direccion:{origen.direccion} ")
        time.sleep(0.1)
        origen.direccion = ""
        mensaje1.empty()
        
        

    # El bus de control toma la señal dada por un origen y la lleva al destino
    def transferirControl(self, origen, destino):
      
        destino.señal = origen.señal
    
        mensaje2= st.empty()
     
        mensaje2.info(f"Se transfirio por el bus de control: {origen.señal}")
        time.sleep(0.1)
        origen.señal = ""
        mensaje2.empty()

    #El bus de datos toma la señal dada por un origen y la lleva al destino
    def transferirDato(self, origen, destino):
        destino.dato = origen.dato
        mensaje= st.empty()

        mensaje.info(f"Se transfirio por el bus de datos: {origen.dato}")
        time.sleep(0.1)
        origen.dato = ""
        mensaje.empty()
    
    def transferirContador(self, contador, destino):
        destino.direccion = contador