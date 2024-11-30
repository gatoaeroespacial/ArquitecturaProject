from Model.SimuladorComputador import SimuladorComputador

# Programa de prueba
program = [
    "MOV 5",  # Cargar el valor 5 en el primer registro
    "ADD 3",  # Sumar 3 al primer registro
    "AND 7",  # Realizar AND con 7
    "HALT",   # Fin del programa
]

# Crear el simulador y ejecutar el programa
simulador = SimuladorComputador()
simulador.run(program)
