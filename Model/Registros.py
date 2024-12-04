class Registros:
    def __init__(self):
        self.AL = ""
        self.BL = ""
        self.CL = ""
        self.DL = ""
        self.señal = ""
        self.dato = ""
        self.direccion = ""

    def write(self, address, value):
        if address == "0000000000": self.AL = value
        if address == "0000000001": self.BL = value
        if address == "0000000011": self.CL = value
        if address == "0000000010": self.DL = value

    def read(self, address):
        if address == "0000000000": return self.AL
        if address == "0000000001": return self.BL
        if address == "0000000010": return self.CL
        if address == "0000000011": return self.DL