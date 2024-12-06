class UnidadControl:
    def __init__(self):
        self.señal = ""
        self.direccion = ""
        self.dato = ""

    def moverDatoMBR(self, destino, origen):
        destino.dato = origen.dato
        origen.dato = ""

    def transferirDireccion(self, direccion, destino):
        destino.direccion = direccion

    def tranferirSeñal(self, señal, destino):
        destino.señal = señal

    def transferirDato(self, dato, destino):
        destino.dato = dato

    def decode(self):
        instruccion = [self.dato[:8]]
        instruccion.append(self.dato[8:20])
        instruccion.append(self.dato[20:])
        nuevaInstruccion = []
        for i in instruccion:
            if i == "00000000": nuevaInstruccion.append("MOV")
            if i == "00000001": nuevaInstruccion.append("ADD")
            if i == "00000010": nuevaInstruccion.append("HLT")
            if i == "00000011": nuevaInstruccion.append("JMP")
            if i == "00000100": nuevaInstruccion.append("STORE")
            if len(i) == 12:
                if i[:2] == "00": nuevaInstruccion.append("Registro")
                if i[:2] == "01": nuevaInstruccion.append("Memoria")
                if i[:2] == "11": nuevaInstruccion.append("Inmediato")
                nuevaInstruccion.append(i[2:])
        return nuevaInstruccion