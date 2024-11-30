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