class Ensamblador:
    def __init__(self):
        pass

    def codificarInstruccion(self, instruccion):
        instruccion = instruccion.split()
        nuevaInstruccion = ""
        for i in instruccion:
            i = i.strip(",")
            if i == "MOV":
                nuevaInstruccion += "00000000"
            if i == "ADD":
                nuevaInstruccion += "00000001"
            if i == "HLT":
                nuevaInstruccion += "00000010" + bin(0)[2:].zfill(24)
            if i == "AL":
                nuevaInstruccion += "000000000000"
            if i == "BL":
                nuevaInstruccion += "000000000001"
            if self.es_numero(i) == True:
                nuevaInstruccion += "11" + bin(int(i))[2:].zfill(10)
            if i[0] == "[":
                i = i.replace('[', '').replace(']', '').strip()
                nuevaInstruccion += '01' + bin(int(i))[2:].zfill(10)
        return nuevaInstruccion

    def es_numero(self, numero):
        try:
            int(numero)  # Intentamos convertir a float
            return True
        except ValueError:
            return False