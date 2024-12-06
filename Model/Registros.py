class Registros:
    def __init__(self):
        self.AL = ""
        self.BL = ""
        self.CL = ""
        self.DL = ""
        self.señal = ""
        self.dato = ""
        self.direccion = ""

    def write(self):
        if self.direccion == "0000000000": self.AL = self.dato
        if self.direccion == "0000000001": self.BL = self.dato
        if self.direccion == "0000000010": self.CL = self.dato
        if self.direccion == "0000000011": self.DL = self.dato

    def read(self):
        if self.direccion == "0000000000": self.dato = self.AL
        if self.direccion == "0000000001": self.dato = self.BL
        if self.direccion == "0000000010": self.dato = self.CL
        if self.direccion == "0000000011": self.dato = self.DL