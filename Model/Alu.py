class Alu:
    def __init__(self):
        self.result = ""
        self.dato1 = "00"
        self.dato2 = "00"
        self.flags = {"zero": 0, "carry": 0}  # Flags para carry y zero

    def add(self):
        if self.dato1 == "":
            self.dato1 = "00"
        if self.dato2 == "":
            self.dato2 = "00"
        self.result = int(self.dato1, 2) + int(self.dato2, 2)
        self.result = bin(self.result)[2:].zfill(32)
        self.dato1 = ""
        self.dato2 = ""

    def and_operation(self, operand1, operand2):
        self.result = operand1 & operand2
        self.flags["zero"] = 1 if self.result == 0 else 0
        return self.result

    def or_operation(self, operand1, operand2):
        self.result = operand1 | operand2
        self.flags["zero"] = 1 if self.result == 0 else 0
        return self.result