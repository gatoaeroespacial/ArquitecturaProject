class Alu:
    def __init__(self):
        self.result = 0
        self.flags = {"zero": 0, "carry": 0}  # Flags para carry y zero

    def add(self, operand1, operand2):
        self.result = operand1 + operand2
        self.flags["zero"] = 1 if self.result == 0 else 0
        self.flags["carry"] = 1 if self.result > 255 else 0  # Suponiendo 8 bits
        return self.result

    def and_operation(self, operand1, operand2):
        self.result = operand1 & operand2
        self.flags["zero"] = 1 if self.result == 0 else 0
        return self.result

    def or_operation(self, operand1, operand2):
        self.result = operand1 | operand2
        self.flags["zero"] = 1 if self.result == 0 else 0
        return self.result