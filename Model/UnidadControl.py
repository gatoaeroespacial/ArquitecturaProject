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