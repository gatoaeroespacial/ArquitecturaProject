class Alu:
    def __init__(self):
        self.result = ""
        self.dato1 = "00"
        self.dato2 = "00"
        self.flags = {"zero": 0, "carry": 0}  # Flags para carry y zero

    def add(self):
        if self.dato1 == "":
           return 2
        if self.dato2 == "":
            return 3
        self.result = int(self.dato1, 2) + int(self.dato2, 2)
        if self.result > 2147483647 or self.result < -2147483648:
            return 1
        self.result = bin(self.result)[2:].zfill(32)
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
        print(self.dato1)
        for i in self.dato1:
            if i == "1":
                self.result += "0"
            else:
                self.result += "1"
            n += 1
        self.dato1 = ""
        return 0