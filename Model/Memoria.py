class Memoria:
    def __init__(self, size):
        self.memory = [""] * size  # Iniciar memoria de tamaño `size`
        self.direccion = "" # Direccion que necesita la memoria
        self.señal = "" # Accion a realizar dada por el bus de control
        self.dato = "" # Dato que se encontraba en la direccion

    def write(self):
        self.memory[int(self.direccion, 2)] = self.dato

    def escribirInstruccion(self, address, value):
        self.memory[address] = str(value)

    def read(self):
        self.dato = self.memory[int(self.direccion, 2)]