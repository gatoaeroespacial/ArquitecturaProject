from Model.Alu import Alu
from Model.UnidadControl import UnidadControl
from Model.Memoria import Memoria
from Model.Registros import Registros
from Model.Bus import Bus
from Model.Ensamblador import Ensamblador

class SimuladorComputador:
    def __init__(self, memory_size=256):
        self.alu = Alu()
        self.control = UnidadControl()
        self.memory = Memoria(memory_size)
        self.registros = Registros()
        self.bus = Bus()
        self.ensamblador = Ensamblador()

    def run(self, program):
        # Cargar programa en la memoria
        for i, instruccion in enumerate(program):
            instruccion = self.ensamblador.codificarInstruccion(instruccion)
            print(instruccion)
            self.memory.write(i, instruccion)
'''
        # Ejecutar ciclo de instrucciones
        while True:
            instruction = self.control.fetch(self.memory)
            if instruction == "HALT":  # Detener si se encuentra HALT
                print("Ejecución finalizada.")
                break
            try:
                op_code, operand = self.control.decode(instruction)
            except ValueError as e:
                print(f"Error en la instrucción: {e}")
                break

            if op_code == "ADD":
                self.alu.add(self.registros.read_GPR(0), operand)
                self.registros.write_GPR(0, self.alu.result)
            elif op_code == "AND":
                self.alu.and_operation(self.registros.read_GPR(0), operand)
                self.registros.write_GPR(0, self.alu.result)
            elif op_code == "MOV":
                self.registros.write_GPR(0, operand)

            # Imprimir estado de la simulación
            print(f"PC: {self.registros.PC}, IR: {self.registros.IR}, GPR: {self.registros.GPR}")
'''
