from Model.SimuladorComputador import SimuladorComputador

# Programa de prueba
program = [
    "MOV AL, 5", #Cargar el valor inmediato 5 en el registro AL
    "ADD AL, 3", #Sumar el valor inmediato 3 al contenido de AL
    "MOV [10], AL", #Guardar el contenido de AL en la dirección de memoria 10
    "MOV BL, [10]", #Recuperar el valor de la memoria 10 en el registro BL
]

# Crear el simulador y ejecutar el programa
simulador = SimuladorComputador()
simulador.run(program)
