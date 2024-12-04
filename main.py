from Model.SimuladorComputador import SimuladorComputador

# Programa de prueba
program = [
    "MOV AL, 5", # Cargar el valor inmediato 5 en el registro AL
    "ADD AL, 3", # Sumar el valor inmediato 3 al contenido del registro AL
    "MOV [10], 10", # Guardar el contenido de AL en la dirección de memoria 10
    "MOV BL, [10]", # Cargar el valor de la dirección de memoria 10 en el registro BL
    "MOV CL, AL",
    "HLT"
]

# Crear el simulador y ejecutar el programa
simulador = SimuladorComputador()
simulador.run(program)
