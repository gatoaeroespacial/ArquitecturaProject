from Model.SimuladorComputador import SimuladorComputador

'''
program = []
while True:
    valor = input("Escribe una instruccion: ")
    if valor == "x": 
        break
    program.append(valor)
'''
demora = 0

# Programa de prueba
program = [
    "MOV AL, 5", # Cargar el valor inmediato 5 en el registro AL
    #"JMP AL",
    "ADD AL, 3", # Sumar el valor inmediato 3 al contenido del registro AL
    "MOV [42], 10", # Guardar el contenido de AL en la dirección de memoria 10
    "MOV BL, [42]", # Cargar el valor de la dirección de memoria 10 en el registro BL
    "MOV CL, AL",
    "MOV [41], [42]",
    "MOV [44], AL",
    "ADD AL, [41]",
    #"JMP 12",
    "ADD BL, AL",
    "ADD [44], 5",
    #"JMP [14]",
    "ADD [41], [41]",
    "ADD [41], CL",
    "STORE [43], CL",
    "LOAD DL, [42]",
    "AND AL, 10",
    "AND BL, [41]",
    "AND DL, BL",
    "AND [44], 43",
    "AND [42], [44]",
    "AND [41], CL",
    "OR AL, 352",
    "OR DL, [44]",
    "OR BL, AL",
    "OR [44], 255",
    "OR [43], [44]",
    "OR [41], BL",
    "SKIP",
    "NOT BL",
    "SKIP",
    "NOT [44]",
    "HLT"
]

for i in program:
    print(i)

# Crear el simulador y ejecutar el programa
simulador = SimuladorComputador()
simulador.run(program, demora)