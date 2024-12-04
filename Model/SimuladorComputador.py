from Model.Alu import Alu
from Model.UnidadControl import UnidadControl
from Model.Memoria import Memoria
from Model.Registros import Registros
from Model.Bus import Bus
from Model.Ensamblador import Ensamblador
from Model.Pc import Pc
from Model.Mar import Mar
from Model.Mbr import Mbr
from Model.Ir import Ir

class SimuladorComputador:
    def __init__(self, memory_size=256):
        self.alu = Alu()
        self.control = UnidadControl()
        self.memory = Memoria(memory_size)
        self.registros = Registros()
        self.bus = Bus()
        self.ensamblador = Ensamblador()
        self.pc = Pc()
        self.mar = Mar()
        self.mbr = Mbr()
        self.ir = Ir()

    def run(self, program):

        # Cargar programa en la memoria
        for i, instruccion in enumerate(program):
            # Se codifica la memoria de texto a binario de 32 bits
            instruccion = self.ensamblador.codificarInstruccion(instruccion)
            print(instruccion)
            self.memory.write(i, instruccion)

        while True:
            self.control.señal = "00"
            self.transferenciasMemoria(self.pc.contador)
            if self.memory.señal == "00":
                self.datoMemoriaMBR()
                self.bus.transferirDato(self.mbr, self.ir)
                self.control.instruction_register = self.ir.dato
                self.ir.dato = ""
                instruccion = self.control.decode()

                if instruccion[0] == "MOV":
                    self.mov(instruccion)

                if instruccion[0] == "ADD":
                   self.add(instruccion)

                if instruccion[0] == "HLT":
                    break

                self.pc.contador = self.alu.add(self.pc.contador, 1)
                print("AL: " + self.registros.AL)
                print("MEMORY 10: " + str(self.memory.memory[10]))
                print("BL: " + self.registros.BL)
    
    def mov(self, instruccion):
        if instruccion[1] == "Registro" and instruccion[3] == "Inmediato":
            self.control.señal = "01"
            self.bus.transferirControl(self.control, self.registros)
            if self.registros.señal == "01": 
                if instruccion[2] == "0000000000": self.registros.AL += instruccion[4].zfill(32)
        if instruccion[1] == "Registro" and instruccion[3] == "Memoria":
            self.control.señal = "01"
            self.bus.transferirControl(self.control, self.registros)
            self.control.señal = "00"
            self.transferenciasMemoria(instruccion[4])
            self.datoMemoriaMBR()
            if instruccion[2] == "0000000001": self.registros.BL = self.mbr.dato
        if instruccion[1] == "Memoria" and instruccion[3] == "Registro":
            self.control.señal = "01"
            self.transferenciasMemoria(instruccion[2])
            if self.memory.señal == "01": self.memory.write(int(self.memory.direccion, 2), self.registros.AL)

    def add(self, instruccion):
         if instruccion[1] == "Registro" and instruccion[3] == "Inmediato":
            self.control.señal = "00"
            self.bus.transferirControl(self.control, self.registros)
            if self.registros.señal == "00":
                if instruccion[2] == "0000000000": self.registros.AL = self.alu.add(self.registros.AL, int(instruccion[4], 2))
    
    def transferenciasMemoria(self, direccion):
        self.control.moverPCaMAR(self.mar, direccion)
        self.bus.transferirControl(self.control, self.memory)
        self.bus.transferirDireccion(self.mar, self.memory)

    def datoMemoriaMBR(self):
        self.memory.dato = self.memory.read(int(self.memory.direccion, 2))
        self.memory.direccion = ""
        self.bus.transferirDato(self.memory, self.mbr)

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
