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
        dato_str = str(self.dato)
        instruccion = [dato_str[:8]]
        instruccion.append(dato_str[8:20])
        instruccion.append(dato_str[20:])
        nuevaInstruccion = []
        for i in instruccion:
            if i == "00000000": nuevaInstruccion.append("MOV")
            if i == "00000001": nuevaInstruccion.append("ADD")
            if i == "00000010": nuevaInstruccion.append("HLT")
            if i == "00000011": nuevaInstruccion.append("JMP")
            if i == "00000100": nuevaInstruccion.append("STORE")
            if i == "00000101": nuevaInstruccion.append("LOAD")
            if i == "00000110": nuevaInstruccion.append("AND")
            if i == "00000111": nuevaInstruccion.append("OR")
            if i == "00001000": nuevaInstruccion.append("NOT")
            if i == "00001001": nuevaInstruccion.append("SKIP")
            if i == "00001010": nuevaInstruccion.append("SUB")
            if i == "00001011": nuevaInstruccion.append("MUL")
            if i == "00001100": nuevaInstruccion.append("DIV")
            if len(i) == 12:
                if i[:2] == "00": nuevaInstruccion.append("Registro")
                if i[:2] == "01": nuevaInstruccion.append("Memoria")
                if i[:2] == "11": nuevaInstruccion.append("Inmediato")
                nuevaInstruccion.append(i[2:])
        return nuevaInstruccion