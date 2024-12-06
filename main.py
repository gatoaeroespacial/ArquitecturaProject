from Model.SimuladorComputador import SimuladorComputador

# Programa de prueba
program = [
    "MOV AL, 5", # Cargar el valor inmediato 5 en el registro AL
    "JMP AL",
    "ADD AL, 3", # Sumar el valor inmediato 3 al contenido del registro AL
    "MOV [19], 10", # Guardar el contenido de AL en la dirección de memoria 10
    "MOV BL, [19]", # Cargar el valor de la dirección de memoria 10 en el registro BL
    "MOV CL, AL",
    "MOV [18], [19]",
    "MOV [17], AL",
    "ADD AL, [18]",
    "JMP 12",
    "ADD BL, AL",
    "ADD [17], 5",
    "JMP [14]",
    "ADD [18], [18]",
    "ADD [18], CL",
    "HLT"
]

for i in program:
    print(i)

# Crear el simulador y ejecutar el programa
simulador = SimuladorComputador()
simulador.run(program)
