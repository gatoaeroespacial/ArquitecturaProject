class Ensamblador:
    def __init__(self):
        pass

    def codificarInstruccion(self, instruccion):
        instruccion = instruccion.split()
        instruccion[1] = instruccion[1].strip(',')
        nuevaInstruccion = ""
        for i in instruccion:
            if i == "MOV":
                nuevaInstruccion += "00000000"
            if i == "ADD":
                nuevaInstruccion += "00000001"
            if i == "AL":
                nuevaInstruccion += "000000000000"
            if i == "BL":
                nuevaInstruccion += "000000000001"
            if self.es_numero(i) == True:
                nuevaInstruccion += "11" + bin(int(i))[2:].zfill(10)
            if i[0] == "[":
                i = i.strip('[')
                i = i.strip(']')
                nuevaInstruccion += '01' + bin(int(i))[2:].zfill(10)
        return nuevaInstruccion

    def es_numero(self, numero):
        try:
            int(numero)  # Intentamos convertir a float
            return True
        except ValueError:
            return False