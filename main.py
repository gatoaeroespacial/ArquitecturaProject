class ALU:
    def __init__(self):
        self.result = 0
        self.flags = {"zero": 0, "carry": 0}  # Flags para carry y zero

    def add(self, operand1, operand2):
        self.result = operand1 + operand2
        self.flags["zero"] = 1 if self.result == 0 else 0
        self.flags["carry"] = 1 if self.result > 255 else 0  # Suponiendo 8 bits
        return self.result

    def and_operation(self, operand1, operand2):
        self.result = operand1 & operand2
        self.flags["zero"] = 1 if self.result == 0 else 0
        return self.result

    def or_operation(self, operand1, operand2):
        self.result = operand1 | operand2
        self.flags["zero"] = 1 if self.result == 0 else 0
        return self.result


class UnidadControl:
    def __init__(self):
        self.instruction_register = ""
        self.program_counter = 0  # Contador de programa

    def fetch(self, memory):
        # Recuperar la instrucción de la memoria utilizando el contador de programa
        instruction = memory.read(self.program_counter)
        self.instruction_register = instruction
        self.program_counter += 1  # Incrementar el contador de programa
        return instruction


    def decode(self, instruction):
        # Decodificar la instrucción en opcode y operando
        parts = instruction.split(" ")
        if len(parts) == 1:
            op_code = parts[0]
            operand = 0
        elif len(parts) == 2:
            op_code, operand = parts
            operand = int(operand)
        else:
            raise ValueError(f"Formato de instrucción inválido: {instruction}")

        return op_code, operand
class Memoria:
    def __init__(self, size):
        self.memory = [0] * size  # Iniciar memoria de tamaño `size`

    def write(self, address, value):
        self.memory[address] = value

    def read(self, address):
        return self.memory[address]

class Registros:
    def __init__(self):
        self.MAR = 0  # Memory Address Register
        self.IR = ""  # Instruction Register
        self.MBR = 0  # Memory Buffer Register
        self.PC = 0   # Program Counter
        self.GPR = [0] * 4  # Banco de Registros de Propósito General (4 registros)
    
    def read_GPR(self, index):
        return self.GPR[index]

    def write_GPR(self, index, value):
        self.GPR[index] = value

class Bus:
    def __init__(self):
        self.data = 0  # Datos que pasan por el bus

    def transfer(self, source, destination):
        destination.write(self.data)  # Transferir datos de `source` a `destination`
class SimuladorComputador:
    def __init__(self, memory_size=256):
        self.alu = ALU()
        self.control = UnidadControl()
        self.memory = Memoria(memory_size)
        self.registros = Registros()
        self.bus = Bus()

    def run(self, program):
        # Cargar programa en la memoria
        for i, instruction in enumerate(program):
            self.memory.write(i, instruction)

        # Ejecutar ciclo de instrucciones
        while True:
            instruction = self.control.fetch(self.memory)
            if instruction == "HALT":  # Detener si se encuentra HALT
                print("Ejecución finalizada.")
                break
            try:
                op_code, operand = self.control.decode(instruction)
            except ValueError as e:
                print(f"Error en la instrucción: {e}")
                break

            if op_code == "ADD":
                self.alu.add(self.registros.read_GPR(0), operand)
                self.registros.write_GPR(0, self.alu.result)
            elif op_code == "AND":
                self.alu.and_operation(self.registros.read_GPR(0), operand)
                self.registros.write_GPR(0, self.alu.result)
            elif op_code == "MOV":
                self.registros.write_GPR(0, operand)

            # Imprimir estado de la simulación
            print(f"PC: {self.registros.PC}, IR: {self.registros.IR}, GPR: {self.registros.GPR}")

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
