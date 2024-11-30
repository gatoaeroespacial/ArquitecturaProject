class Memoria:
    def __init__(self, size):
        self.memory = [0] * size  # Iniciar memoria de tamaño `size`

    def write(self, address, value):
        self.memory[address] = value

    def read(self, address):
        return self.memory[address]