from Model.SimuladorComputador import SimuladorComputador

'''
program = []
while True:
    valor = input("Escribe una instruccion: ")
    if valor == "x": 
        break
    program.append(valor)
'''

# Programa de prueba
program = [
    "MOV AL, 5", # Cargar el valor inmediato 5 en el registro AL
    #"JMP AL",
    "ADD AL, 3", # Sumar el valor inmediato 3 al contenido del registro AL
    "MOV [52], 10", # Guardar el contenido de AL en la dirección de memoria 10
    "MOV BL, [52]", # Cargar el valor de la dirección de memoria 10 en el registro BL
    "MOV CL, AL",
    "MOV [51], [52]",
    "MOV [54], AL",
    "ADD AL, [51]",
    #"JMP 12",
    "ADD BL, AL",
    "ADD [54], 5",
    #"JMP [14]",
    "ADD [51], [51]",
    "ADD [51], CL",
    "STORE [53], CL",
    "LOAD DL, [52]",
    "AND AL, 10",
    "AND BL, [51]",
    "AND DL, BL",
    "AND [54], 53",
    "AND [52], [54]",
    "AND [51], CL",
    "OR AL, 352",
    "OR DL, [54]",
    "OR BL, AL",
    "OR [54], 255",
    "OR [53], [54]",
    "OR [51], BL",
    "SKIP",
    "NOT BL",
    "SKIP",
    "NOT [54]",
    "SUB [54], [51]",
    "SUB [53], AL",
    "SUB [52], 10",
    "SUB AL, [51]",
    "SUB BL, AL",
    "SUB CL, 10",
    "MUL AL, BL",
    "MUL CL, 30",
    "MUL AL, [51]",
    "MUL [51], 32",
    "MUL [52], CL",
    "MUL [54], [51]",
    "HLT"
]

for i in program:
    print(i)

print()

# Crear el simulador y ejecutar el programa
simulador = SimuladorComputador()
simulador.run(program)