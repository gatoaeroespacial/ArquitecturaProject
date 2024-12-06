class Ensamblador:
    def __init__(self):
        pass

    def codificarInstruccion(self, instruccion):
        instruccion = instruccion.split()
        nuevaInstruccion = ""
        for i in instruccion:
            i = i.strip(",")
            if i == "MOV": nuevaInstruccion += "00000000"
            if i == "ADD": nuevaInstruccion += "00000001"
            if i == "HLT": nuevaInstruccion += "00000010" + bin(0)[2:].zfill(24)
            if i == "JMP": nuevaInstruccion += "00000011"
            if i == "STORE": nuevaInstruccion += "00000100"
            if i == "LOAD": nuevaInstruccion += "00000101"
            if i == "AND": nuevaInstruccion += "00000110"
            if i == "OR": nuevaInstruccion += "00000111"
            if i == "NOT": nuevaInstruccion += "00001000"
            if i == "SKIP": nuevaInstruccion += "00001001"
            if i == "AL": nuevaInstruccion += "000000000000"
            if i == "BL": nuevaInstruccion += "000000000001"
            if i == "CL": nuevaInstruccion += "000000000010"
            if i == "DL": nuevaInstruccion += "000000000011"
            if self.es_numero(i) == True: 
                if int(i) < 0:
                    return "No se pueden escribir numeros negativos"
                if int(i) > 511:
                    return "Excede el tamaño posible de numero en instrucción"
                nuevaInstruccion += "11" + bin(int(i))[2:].zfill(10)
            if i[0] == "[":
                i = i.replace('[', '').replace(']', '').strip()
                if int(i) > 1023:
                    return "Excede el tamaño de la memoria"
                nuevaInstruccion += '01' + bin(int(i))[2:].zfill(10)
        if len(nuevaInstruccion) != 32:
            n = 32 - len(nuevaInstruccion)
            nuevaInstruccion += bin(0)[2:].zfill(n)
        return nuevaInstruccion

    def es_numero(self, numero):
        try:
            int(numero)  # Intentamos convertir a float
            return True
        except ValueError:
            return False