class UnidadControl:
    def __init__(self):
        self.instruction_register = "",
        self.señal = ""

    # La UC toma la direccion del PC y la pone en el MAR
    def moverDireccionMAR(self, destino, direccion):
        destino.direccion = direccion

    def moverDatoMBR(self, destino, origen):
        destino.dato = origen.dato
        origen.dato = ""

    def decode(self):
        instruccion = [self.instruction_register[:8]]
        instruccion.append(self.instruction_register[8:20])
        instruccion.append(self.instruction_register[20:])
        nuevaInstruccion = []
        for i in instruccion:
            if i == "00000000": nuevaInstruccion.append("MOV")
            if i == "00000001": nuevaInstruccion.append("ADD")
            if i == "00000010": nuevaInstruccion.append("HLT")
            if len(i) == 12:
                if i[:2] == "00": nuevaInstruccion.append("Registro")
                if i[:2] == "01": nuevaInstruccion.append("Memoria")
                if i[:2] == "11": nuevaInstruccion.append("Inmediato")
                nuevaInstruccion.append(i[2:])
        return nuevaInstruccion