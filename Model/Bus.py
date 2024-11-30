class Bus:
    def __init__(self):
        self.data = 0  # Datos que pasan por el bus

    def transfer(self, source, destination):
        destination.write(self.data)  # Transferir datos de `source` a `destination`