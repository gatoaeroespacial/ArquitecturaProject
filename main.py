import streamlit as st
from Model.SimuladorComputador import SimuladorComputador
from ui.visualizer import render_state_viewer
from ui.forms import render_code_editor

if "simulador" not in st.session_state:
    # Crear una instancia del simulador
    st.session_state.simulador = SimuladorComputador()
    
st.title("Simulador de Computador")
st.sidebar.title("Opciones")
opcion = st.sidebar.selectbox("Selecciona una vista", ["Estado", "Ejecutar Programa"])

if opcion == "Estado":
    render_code_editor()
    render_state_viewer()
# Agregar más funcionalidades según se requieran


# program = []
# while True:
#     valor = input("Escribe una instruccion: ")
#     if valor == "x": 
#         break
#     program.append(valor)

# '''
# # Programa de prueba
# program = [
#     "MOV AL, 5", # Cargar el valor inmediato 5 en el registro AL
#     #"JMP AL",
#     "ADD AL, 3", # Sumar el valor inmediato 3 al contenido del registro AL
#     "MOV [32], 10", # Guardar el contenido de AL en la dirección de memoria 10
#     "MOV BL, [32]", # Cargar el valor de la dirección de memoria 10 en el registro BL
#     "MOV CL, AL",
#     "MOV [31], [32]",
#     "MOV [34], AL",
#     "ADD AL, [31]",
#     #"JMP 12",
#     "ADD BL, AL",
#     "ADD [34], 5",
#     #"JMP [14]",
#     "ADD [31], [31]",
#     "ADD [31], CL",
#     "STORE [33], CL",
#     "LOAD DL, [32]",
#     "AND AL, 10",
#     "AND BL, [31]",
#     "AND DL, BL",
#     "AND [34], 33",
#     "AND [32], [34]",
#     "AND [31], CL",
#     "OR AL, 352",
#     "OR DL, [34]",
#     "OR BL, AL",
#     "OR [34], 255",
#     "OR [33], [34]",
#     "OR [31], BL",
#     "SKIP",
#     "NOT BL",
#     "SKIP",
#     "NOT [34]",
#     "HLT"
# ]
# '''

# for i in program:
#     print(i)

# # Crear el simulador y ejecutar el programa
# simulador = SimuladorComputador()
# simulador.run(program)
