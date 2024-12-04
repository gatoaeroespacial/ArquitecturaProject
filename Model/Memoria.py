class Memoria:
    def __init__(self, size):
        self.memory = [0] * size  # Iniciar memoria de tamaño `size`
        self.direccion = "" # Direccion que necesita la memoria
        self.señal = "" # Accion a realizar dada por el bus de control
        self.dato = "" # Dato que se encontraba en la direccion

    def write(self, address, value):
        self.memory[address] = value

    def read(self, address):
        return self.memory[address]