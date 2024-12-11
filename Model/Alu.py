class Alu:
    def __init__(self):
        self.result = ""
        self.dato1 = "00"
        self.dato2 = "00"
        self.overflow = 0  # Banderas para carry y zero
        self.carry = 0

    def add(self):
        if self.dato1 == "":
            return 1
        if self.dato2 == "":
            return 2
        dato1 = 0
        dato2 = 0
        signoDato1 = ""
        signoDato2 = ""
        if self.dato1[0] == "1":
            signoDato1 == "Negativo"
            self.dato1 = self.dato1[1:]
            dato1 = -int(self.dato1, 2)
        else: 
            signoDato1 = "Positivo"
            self.dato1 = self.dato1[1:]
            dato1 = int(self.dato1, 2)
        if self.dato2[0] == "1": 
            signoDato2 = "Negativo"
            self.dato2 = self.dato2[1:]
            dato2 = -int(self.dato2, 2)
        else: 
            signoDato2 = "Positivo"
            self.dato2 = self.dato2[1:]
            dato2 = int(self.dato2, 2)
            
        self.result = dato1 + dato2
        
        # Verificar si hay desbordamiento o no
        if self.result > 2147483647 or self.result < -2147483648:
            if signoDato1 == "Positivo" and signoDato2 == "Positivo": self.carry = 1
            else: self.overflow = 1
            if self.result > 0: self.result = "0" + bin(self.result)[-31:].zfill(32)
            elif self.result < 0: self.result = "1" + bin(self.result)[-31:].zfill(32)
        else:
            if self.result > 0: self.result = "0" + bin(self.result)[2:].zfill(32)
            elif self.result < 0: self.result = "1" + bin(self.result)[2:].zfill(32)
            else: bin(self.result)[2:].zfill(32)
        
        self.dato1 = ""
        self.dato2 = ""
        return 0

    def operacionAnd(self):
        if self.dato1 == "":
            return 1
        if self.dato2 == "":
            return 2
        self.result = ""
        n = 0
        for i in self.dato1:
            if i == "1" and self.dato2[n] == "1":
                self.result += "1"
            else:
                self.result += "0"
            n += 1
        
        self.dato1 = ""
        self.dato2 = ""
        return 0

    def operacionOr(self):
        if self.dato1 == "":
            return 1
        if self.dato2 == "":
            return 2
        self.result = ""
        n = 0
        for i in self.dato1:
            if i == "1" or self.dato2[n] == "1":
                self.result += "1"
            else:
                self.result += "0"
            n += 1
        
        self.dato1 = ""
        self.dato2 = ""
        return 0

    def operacionNot(self):
        if self.dato1 == "":
            return 1
        self.result = ""
        n = 0
        for i in self.dato1:
            if i == "1":
                self.result += "0"
            else:
                self.result += "1"
            n += 1
        
        self.dato1 = ""
        return 0




