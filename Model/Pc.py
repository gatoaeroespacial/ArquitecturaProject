class Pc:
    def __init__(self):
        self.contador = "" + bin(0)[2:].zfill(32)

    def sumarContador(self):
        self.contador = "" + bin(int(self.contador, 2) + 1)[2:].zfill(32)